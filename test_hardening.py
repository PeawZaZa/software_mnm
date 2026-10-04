# test_hardening.py
# Unit Tests สำหรับงาน System Hardening สัปดาห์ที่ 11
# ════════════════════════════════════════
# รันด้วย: pytest test_hardening.py -v
#
# ครอบคลุม
#   1. Code smell refactor — Feature Envy (Product.stock_value / needs_reorder)
#                           Duplicate Code (_products_with_barcode)
#   2. Atomic File Writing — ไฟล์เดิมต้องไม่เสียเมื่อบันทึกล้มเหลว
#   3. Robust Exception Handling — save() ต้องไม่กลืน error เงียบ ๆ
#   4. End-to-End integration flow ตั้งแต่เพิ่มสินค้าจนถึงไฟล์ CSV

import csv
import json
import os

import pytest

import app_v2
from app_v2 import (
    SAVE_FAILED_MESSAGE,
    ConsoleUI,
    CsvReportExporter,
    InventoryRepository,
    InventoryService,
    Product,
)


@pytest.fixture
def repo(tmp_path):
    return InventoryRepository(str(tmp_path / "data_test.json"))


@pytest.fixture
def service(repo):
    return InventoryService(repo)


@pytest.fixture
def broken_disk(monkeypatch):
    """จำลองดิสก์เขียนไม่ได้ ณ จังหวะสลับไฟล์ (เช่น ดิสก์เต็ม / ไม่มีสิทธิ์เขียน)"""
    def fail_replace(src, dst):
        raise OSError("simulated disk failure")
    monkeypatch.setattr(app_v2.os, "replace", fail_replace)


# ══════════════════════════════════════════════════
# Code Smell: Feature Envy → ย้ายการคำนวณเข้า Product
# ══════════════════════════════════════════════════

class TestProductOwnsItsCalculations:

    def test_stock_value_is_qty_times_price(self):
        assert Product("A", "A", 7, 25.0, "T").stock_value == pytest.approx(175.0)

    def test_needs_reorder_when_qty_equals_reorder_point(self):
        assert Product("A", "A", 5, 1.0, "T", reorder_point=5).needs_reorder() is True

    def test_does_not_need_reorder_above_point(self):
        assert Product("A", "A", 6, 1.0, "T", reorder_point=5).needs_reorder() is False

    def test_reorder_point_zero_means_not_configured(self):
        """reorder_point = 0 คือยังไม่ได้ตั้ง ไม่ใช่ 'สั่งเมื่อหมด'"""
        assert Product("A", "A", 0, 1.0, "T", reorder_point=0).needs_reorder() is False


# ══════════════════════════════════════════════════
# Code Smell: Duplicate Code → รวมการค้นบาร์โค้ดไว้จุดเดียว
# ══════════════════════════════════════════════════

class TestSingleBarcodeLookup:

    def test_find_and_duplicate_check_agree(self, service):
        service.add_update("P1", "Pen", 10, 5.0, "T", barcode="885")
        assert service.find_by_barcode("885").id == "P1"
        ok, msg = service.add_update("P2", "Pencil", 10, 5.0, "T", barcode="885")
        assert ok is False
        assert "P1" in msg

    def test_owner_skips_itself_even_with_legacy_duplicates(self, repo):
        """
        data.json เก่าอาจมีบาร์โค้ดซ้ำก่อนมีการตรวจ (#20)
        การแก้ไขสินค้าตัวเองต้องยังเจอเจ้าของตัวอื่น ไม่ใช่หยุดที่ตัวเองแล้วบอกว่าว่าง
        """
        repo.path.write_text(json.dumps({
            "A": {"n": "A", "q": 1, "p": 1.0, "c": "T", "b": "DUP"},
            "B": {"n": "B", "q": 1, "p": 1.0, "c": "T", "b": "DUP"},
        }))
        service = InventoryService(repo)
        assert service._barcode_owner("DUP", exclude_id="A") == "B"


# ══════════════════════════════════════════════════
# Atomic File Writing + Robust Exception Handling
# ══════════════════════════════════════════════════

class TestAtomicSave:

    def test_save_returns_true_on_success(self, repo):
        assert repo.save({"A": Product("A", "A", 1, 1.0, "T")}) is True

    def test_failed_save_keeps_original_file_intact(self, repo, broken_disk):
        """หัวใจของ atomic write: ล้มเหลวกลางทาง ไฟล์เดิมต้องอยู่ครบ ไม่กลายเป็นไฟล์ 0 ไบต์"""
        original = json.dumps({"OLD": {"n": "Old", "q": 1, "p": 1.0, "c": "T"}})
        repo.path.write_text(original, encoding="utf-8")
        assert repo.save({"NEW": Product("NEW", "New", 2, 2.0, "T")}) is False
        assert repo.path.read_text(encoding="utf-8") == original

    def test_failed_save_leaves_no_temp_file(self, repo, tmp_path, broken_disk):
        repo.save({"A": Product("A", "A", 1, 1.0, "T")})
        assert list(tmp_path.glob("*.tmp")) == []

    def test_failed_save_reports_error(self, repo, broken_disk, capsys):
        repo.save({"A": Product("A", "A", 1, 1.0, "T")})
        assert "error saving data" in capsys.readouterr().out.lower()

    def test_unwritable_directory_returns_false(self, tmp_path):
        repo = InventoryRepository(str(tmp_path / "no-such-dir" / "data.json"))
        assert repo.save({}) is False

    def test_thai_text_is_saved_readable(self, repo):
        """ensure_ascii=False — ไฟล์ข้อมูลเปิดอ่านภาษาไทยได้ตรง ๆ ไม่เป็น \\u0e21"""
        repo.save({"P1": Product("P1", "มาม่า", 1, 6.0, "อาหาร")})
        assert "มาม่า" in repo.path.read_text(encoding="utf-8")


class TestLoadRejectsWrongShape:

    def test_json_list_is_treated_as_corrupted(self, repo, capsys):
        """JSON ถูกไวยากรณ์แต่ผิดรูปแบบ (list แทน object) เคยทำให้ .items() พัง"""
        repo.path.write_text("[1, 2, 3]")
        assert set(repo.load()) == {"101", "102", "103"}
        assert "corrupted" in capsys.readouterr().out.lower()


class TestServiceDoesNotLieAboutSaving:
    """
    ก่อนสัปดาห์ที่ 11 save() กลืน exception แล้วคืน None
    service จึงตอบ "Done." ทั้งที่ไฟล์ไม่ได้ถูกบันทึก — ข้อมูลหายเมื่อปิดโปรแกรม
    """

    def test_add_reports_failure_and_rolls_back_new_item(self, service, broken_disk):
        ok, msg = service.add_update("NEW", "New", 1, 1.0, "T")
        assert ok is False
        assert msg == SAVE_FAILED_MESSAGE
        assert "NEW" not in service.inventory

    def test_update_rolls_back_to_previous_item(self, service, broken_disk):
        before = service.inventory["101"]
        ok, _ = service.add_update("101", "Renamed", 1, 1.0, "T")
        assert ok is False
        assert service.inventory["101"] == before

    def test_stock_out_rolls_back_qty(self, service, broken_disk):
        ok, msg = service.stock_out("101", 10)
        assert ok is False
        assert msg == SAVE_FAILED_MESSAGE
        assert service.inventory["101"].qty == 50


# ══════════════════════════════════════════════════
# ConsoleUI: ตารางเมนูแทน if/elif
# ══════════════════════════════════════════════════

class TestMenuTable:

    def test_menu_lists_all_seven_choices_in_order(self, service):
        ui = ConsoleUI(service, input_fn=lambda p="": "5", print_fn=lambda *a: None)
        assert list(ui.menu()) == ["1", "2", "3", "4", "5", "6", "7"]

    def test_every_choice_except_exit_has_a_handler(self, service):
        ui = ConsoleUI(service, input_fn=lambda p="": "5", print_fn=lambda *a: None)
        for key, (_, handler) in ui.menu().items():
            assert (handler is None) == (key == ConsoleUI.EXIT_CHOICE)


# ══════════════════════════════════════════════════
# End-to-End: CR-01 + CR-02 ทำงานร่วมกันตั้งแต่ต้นจนจบ
# ══════════════════════════════════════════════════

def test_full_system_integration_flow(tmp_path):
    """
    1. เพิ่มสินค้าใหม่พร้อม Barcode และ Reorder Point (CR-01)
    2. ตัดสต๊อกจนต่ำกว่าจุดสั่งซื้อ
    3. ตรวจรายการที่ต้องสั่งซื้อซ้ำ
    4. ส่งออก CSV (CR-02)
    5. ปิดแล้วเปิดโปรแกรมใหม่ ข้อมูลและ CSV ต้องตรงกัน
    """
    db_path = tmp_path / "db.json"
    csv_path = tmp_path / "out.csv"

    service = InventoryService(InventoryRepository(str(db_path)))
    assert service.add_update("P1", "Pen", 10, 10.0, "Stationery",
                              barcode="885", reorder_point=5) == (True, "Done.")
    ok, _ = service.stock_out("P1", 6)
    assert ok is True

    assert [p.id for p in service.get_reorder_list()] == ["P1"]
    assert service.find_by_barcode("885").qty == 4

    rows = CsvReportExporter().export(service.inventory, str(csv_path))
    assert rows == 4  # default 3 รายการ + Pen

    # เปิดโปรแกรมใหม่จากไฟล์บนดิสก์ — ต้องได้สถานะเดิม
    reopened = InventoryService(InventoryRepository(str(db_path)))
    assert reopened.find_by_barcode("885").qty == 4

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        exported = {row["id"]: row for row in csv.DictReader(f)}
    assert exported["P1"]["barcode"] == "885"
    assert exported["P1"]["qty"] == "4"
    assert exported["P1"]["reorder_point"] == "5"
    assert not os.path.exists(str(db_path) + ".tmp")
