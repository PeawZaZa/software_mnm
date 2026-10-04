# test_disaster_recovery.py
# Disaster Recovery Drill Tests (สัปดาห์ที่ 14 — ISO/IEC 25010 Recoverability)
# ════════════════════════════════════════
# รันด้วย: pytest test_disaster_recovery.py -v
#
# กลไกที่ทดสอบ
#   1. Rolling Auto-Backup — ก่อนบันทึกทุกครั้ง สำเนาไฟล์เดิมเป็น <ชื่อไฟล์>.bak
#   2. Automated Fallback — ไฟล์หลักเสีย/หาย → โหลดจาก .bak อัตโนมัติ ไม่ crash

import json

import pytest

from app_v2 import InventoryRepository, InventoryService, Product


@pytest.fixture
def repo(tmp_path):
    return InventoryRepository(tmp_path / "inventory.json")


def write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


ITEM_A = {"P01": {"n": "Item A", "q": 10, "p": 100.0, "c": "T"}}


# ══════════════════════════════════════════════════
# 1. Rolling Auto-Backup
# ══════════════════════════════════════════════════

class TestRollingBackup:

    def test_first_save_has_nothing_to_back_up(self, repo):
        repo.save({"A": Product("A", "A", 1, 1.0, "T")})
        assert not repo.backup_path.exists()

    def test_second_save_keeps_previous_version_in_bak(self, repo):
        repo.save({"A": Product("A", "Old", 1, 1.0, "T")})
        repo.save({"A": Product("A", "New", 2, 1.0, "T")})
        backup = json.loads(repo.backup_path.read_text(encoding="utf-8"))
        current = json.loads(repo.path.read_text(encoding="utf-8"))
        assert backup["A"]["n"] == "Old"
        assert current["A"]["n"] == "New"

    def test_corrupted_main_never_overwrites_good_backup(self, repo):
        """ถ้าไฟล์หลักเสียอยู่แล้ว ห้ามสำเนาไฟล์เสียไปทับ .bak ที่ยังดี"""
        write(repo.backup_path, ITEM_A)
        repo.path.write_text("{ broken", encoding="utf-8")
        assert repo.save({"B": Product("B", "B", 1, 1.0, "T")}) is True
        assert json.loads(repo.backup_path.read_text(encoding="utf-8")) == ITEM_A


# ══════════════════════════════════════════════════
# 2. Automated Fallback
# ══════════════════════════════════════════════════

def test_repository_disaster_recovery_fallback(repo):
    """โจทย์ในใบงาน: ไฟล์หลักพัง + ไฟล์สำรองดี → ต้องกู้คืนจาก .bak สำเร็จ"""
    # 1. Arrange: ไฟล์สำรองดี และไฟล์หลักพัง
    write(repo.backup_path, ITEM_A)
    repo.path.write_text("{ INVALID CORRUPTED JSON DATA... }", encoding="utf-8")
    # 2. Act
    inventory = repo.load()
    # 3. Assert
    assert "P01" in inventory
    assert inventory["P01"].name == "Item A"


class TestFallback:

    def test_warns_that_backup_was_used(self, repo, capsys):
        write(repo.backup_path, ITEM_A)
        repo.path.write_text("{ broken", encoding="utf-8")
        repo.load()
        out = capsys.readouterr().out
        assert "corrupted" in out
        assert "Restored data from backup inventory.json.bak" in out

    def test_deleted_main_file_is_restored_from_backup(self, repo, capsys):
        write(repo.backup_path, ITEM_A)
        assert set(repo.load()) == {"P01"}
        assert "is missing" in capsys.readouterr().out

    def test_both_files_broken_falls_back_to_defaults(self, repo, capsys):
        repo.path.write_text("{ broken", encoding="utf-8")
        repo.backup_path.write_text("also broken", encoding="utf-8")
        assert set(repo.load()) == {"101", "102", "103"}
        assert "Loading default data" in capsys.readouterr().out

    def test_first_run_uses_defaults_silently(self, repo, capsys):
        assert set(repo.load()) == {"101", "102", "103"}
        assert capsys.readouterr().out == ""


# ══════════════════════════════════════════════════
# 3. Drill ครบวงจร — จำลองสถานการณ์จริงในใบงาน
# ══════════════════════════════════════════════════

def test_drill_truncated_file_recovers_last_saved_state(tmp_path):
    """
    ร้านค้าบันทึกข้อมูลตามปกติ → ไฟล์ถูกตัดปีกกาปิดท้าย (ไฟดับ/แก้มือ)
    → เปิดโปรแกรมใหม่ต้องได้ข้อมูลก่อนการบันทึกครั้งล่าสุด และใช้งานต่อได้
    """
    path = tmp_path / "inventory_db.json"
    service = InventoryService(InventoryRepository(path))
    service.add_update("P1", "Milk", 10, 20.0, "Dairy", "885", 5)
    service.stock_out("P1", 3)  # บันทึกครั้งที่ 2 → .bak มีสถานะหลังเพิ่ม Milk

    damaged = path.read_text(encoding="utf-8").rstrip()[:-1]  # ลบปีกกาปิดท้าย
    path.write_text(damaged, encoding="utf-8")

    reopened = InventoryService(InventoryRepository(path))
    assert reopened.find_by_barcode("885").qty == 10  # ย้อนไป 1 ก้าว — ก่อนตัดสต๊อก
    ok, _ = reopened.stock_out("P1", 3)
    assert ok is True
    assert json.loads(path.read_text(encoding="utf-8"))["P1"]["q"] == 7
