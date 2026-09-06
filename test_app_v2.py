# test_app_v2.py
# Unit Tests สำหรับสถาปัตยกรรม class-based (Sprint 2)
# ════════════════════════════════════════
# รันด้วย: pytest test_app_v2.py -v
#
# ต่างจาก test_app.py ตรงที่ไฟล์นี้เรียกคลาส "ของจริง" ใน app_v2.py
# ไม่ใช่ฟังก์ชันจำลอง (calc_summary / apply_stock_out) แบบไฟล์เดิม

import json

import pytest

from app_v2 import ConsoleUI, InventoryRepository, InventoryService, Product


# ══════════════════════════════════════════════════
# SAM1-29: Product dataclass
# ══════════════════════════════════════════════════

@pytest.fixture
def noodles():
    """สินค้าตัวอย่างที่ตรงกับ default data รายการแรก"""
    return Product(id="101", name="Mama Noodles", qty=50, price=6.0, category="Food")


class TestProductStructure:

    def test_has_all_five_attributes(self, noodles):
        """Product ต้องมีครบ 5 attribute ตามที่ระบุใน SAM1-28"""
        assert noodles.id == "101"
        assert noodles.name == "Mama Noodles"
        assert noodles.qty == 50
        assert noodles.price == pytest.approx(6.0)
        assert noodles.category == "Food"

    def test_attribute_types(self, noodles):
        """ล็อกชนิดข้อมูล: id=str, qty=int, price=float, category=str"""
        assert isinstance(noodles.id, str)
        assert isinstance(noodles.name, str)
        assert isinstance(noodles.qty, int)
        assert isinstance(noodles.price, float)
        assert isinstance(noodles.category, str)

    def test_qty_is_mutable(self, noodles):
        """stock_out() ต้องแก้ qty ได้ → dataclass ห้าม frozen"""
        noodles.qty -= 10
        assert noodles.qty == 40

    def test_equality_by_value(self):
        """dataclass ต้องเทียบเท่ากันด้วยค่า ไม่ใช่ตัวตน (ช่วยให้เขียน assert ง่าย)"""
        a = Product("X", "Item", 1, 2.0, "T")
        b = Product("X", "Item", 1, 2.0, "T")
        assert a == b


class TestProductToDict:

    def test_to_dict_uses_legacy_short_keys(self, noodles):
        """
        to_dict() ต้องคืน key ย่อ n/q/p/c เท่านั้น
        เพื่อให้ data.json เดิมยังใช้ได้ ไม่ต้อง migrate ข้อมูล
        """
        d = noodles.to_dict()
        assert d == {"n": "Mama Noodles", "q": 50, "p": 6.0, "c": "Food"}

    def test_to_dict_excludes_id(self, noodles):
        """id เป็น key ของ dict ชั้นนอก จึงต้องไม่ซ้ำอยู่ข้างใน"""
        assert "id" not in noodles.to_dict()


class TestProductFromDict:

    def test_from_dict_reads_legacy_shape(self):
        """from_dict() ต้องอ่านโครงสร้างเดิมจาก data.json ได้"""
        p = Product.from_dict("102", {"n": "Lactasoy Milk", "q": 20, "p": 12.0, "c": "Drink"})
        assert p == Product("102", "Lactasoy Milk", 20, 12.0, "Drink")

    def test_roundtrip_preserves_all_fields(self, noodles):
        """from_dict(to_dict()) ต้องได้ของเดิมทุก field"""
        assert Product.from_dict(noodles.id, noodles.to_dict()) == noodles

    def test_from_dict_coerces_types(self):
        """
        Legacy data บางแถวเก็บ qty/price เป็น string — ต้องแปลงให้ถูกชนิด
        ไม่งั้น get_summary() จะคำนวณมูลค่าผิด
        """
        p = Product.from_dict("X", {"n": "Legacy", "q": "7", "p": "25", "c": "T"})
        assert p.qty == 7
        assert isinstance(p.qty, int)
        assert p.price == pytest.approx(25.0)
        assert isinstance(p.price, float)

    def test_from_dict_fills_missing_keys_with_defaults(self):
        """แถวที่ขาด key ต้องไม่ทำให้ทั้งระบบพัง (KeyError)"""
        p = Product.from_dict("X", {"n": "Broken"})
        assert p.name == "Broken"
        assert p.qty == 0
        assert p.price == pytest.approx(0.0)
        assert p.category == ""

    def test_from_dict_raises_on_uncoercible_value(self):
        """ค่าที่แปลงเป็นตัวเลขไม่ได้เลย ต้องโยน ValueError ให้ชั้นบนจัดการ"""
        with pytest.raises(ValueError):
            Product.from_dict("X", {"n": "Bad", "q": "abc", "p": 1.0, "c": "T"})


# ══════════════════════════════════════════════════
# SAM1-33: InventoryRepository — โหลด/บันทึกไฟล์
# ══════════════════════════════════════════════════

@pytest.fixture
def repo(tmp_path):
    """Repository ที่ชี้ไปยังไฟล์ชั่วคราว ไม่กระทบ data.json จริง"""
    return InventoryRepository(str(tmp_path / "data_test.json"))


class TestRepositoryLoad:

    def test_returns_default_when_file_missing(self, repo):
        """ไม่มีไฟล์ → ต้องได้ default 3 รายการ"""
        inv = repo.load()
        assert len(inv) == 3
        assert set(inv) == {"101", "102", "103"}

    def test_default_items_are_product_objects(self, repo):
        """ค่าที่คืนต้องเป็น Product ไม่ใช่ dict ดิบ"""
        inv = repo.load()
        assert inv["101"] == Product("101", "Mama Noodles", 50, 6.0, "Food")
        assert all(isinstance(p, Product) for p in inv.values())

    def test_reads_existing_file(self, repo):
        """มีไฟล์ → ต้องอ่านจากไฟล์"""
        repo.path.write_text(json.dumps({"999": {"n": "Custom", "q": 7, "p": 99.0, "c": "Special"}}))
        inv = repo.load()
        assert inv == {"999": Product("999", "Custom", 7, 99.0, "Special")}

    def test_empty_file_does_not_fall_back_to_default(self, repo):
        """ไฟล์ที่เก็บ {} ไว้ ถือว่าสต๊อกว่าง ไม่ใช่สัญญาณให้โหลด default"""
        repo.path.write_text("{}")
        assert repo.load() == {}

    def test_corrupted_file_falls_back_to_default(self, repo, capsys):
        """[INV-10] ไฟล์เสีย → เตือนแล้วโหลด default แทนที่จะ crash"""
        repo.path.write_text("{ this is not json")
        inv = repo.load()
        assert len(inv) == 3
        assert "corrupted" in capsys.readouterr().out.lower()

    def test_legacy_row_with_missing_keys_does_not_crash(self, repo):
        """แถวเก่าที่ key ไม่ครบ ต้องอ่านผ่านโดยเติมค่า default"""
        repo.path.write_text(json.dumps({"X": {"n": "Partial"}}))
        assert repo.load()["X"] == Product("X", "Partial", 0, 0.0, "")


class TestRepositorySave:

    def test_creates_file(self, repo):
        repo.save({"101": Product("101", "Mama Noodles", 50, 6.0, "Food")})
        assert repo.path.exists()

    def test_writes_legacy_short_keys(self, repo):
        """ไฟล์ที่เขียนออกต้องยังเป็นรูปแบบ n/q/p/c เดิม"""
        repo.save({"101": Product("101", "Mama Noodles", 50, 6.0, "Food")})
        assert json.loads(repo.path.read_text()) == {
            "101": {"n": "Mama Noodles", "q": 50, "p": 6.0, "c": "Food"}
        }

    def test_roundtrip_preserves_data(self, repo):
        original = {
            "101": Product("101", "Mama Noodles", 99, 6.0, "Food"),
            "NEW": Product("NEW", "Test", 1, 1.0, "T"),
        }
        repo.save(original)
        assert repo.load() == original

    def test_overwrites_previous_content(self, repo):
        repo.save({"101": Product("101", "Old", 1, 1.0, "T")})
        repo.save({"ONLY": Product("ONLY", "Only Item", 1, 1.0, "T")})
        assert set(repo.load()) == {"ONLY"}

    def test_atomic_write_leaves_no_tmp_file(self, repo, tmp_path):
        """[INV-11] เขียนผ่าน .tmp แล้ว replace — ห้ามเหลือไฟล์ .tmp ค้าง"""
        repo.save({"101": Product("101", "Mama Noodles", 50, 6.0, "Food")})
        assert list(tmp_path.glob("*.tmp")) == []


# ══════════════════════════════════════════════════
# SAM1-35: InventoryService — business logic
# ══════════════════════════════════════════════════

@pytest.fixture
def service(repo):
    """Service ที่เริ่มจาก default inventory 3 รายการ (101/102/103)"""
    return InventoryService(repo)


class TestServiceValidate:

    def test_accepts_valid_values(self, service):
        assert service.validate(10, 5.0) == (True, "")

    def test_accepts_zero(self, service):
        """qty=0 (ของหมด) และ price=0 (ของแถม) เป็นค่าที่ถูกต้อง"""
        assert service.validate(0, 0.0)[0] is True

    def test_rejects_negative_qty(self, service):
        ok, msg = service.validate(-1, 5.0)
        assert ok is False
        assert "qty" in msg.lower()

    def test_rejects_negative_price(self, service):
        ok, msg = service.validate(1, -5.0)
        assert ok is False
        assert "price" in msg.lower()


class TestServiceAddUpdate:

    def test_adds_new_product(self, service):
        ok, _ = service.add_update("NEW", "New Product", 30, 15.0, "Test")
        assert ok is True
        assert service.inventory["NEW"] == Product("NEW", "New Product", 30, 15.0, "Test")

    def test_update_overwrites_all_fields(self, service):
        """[INV-8] อัปเดตคือเขียนทับเสมอ ไม่ใช่บวกสะสม"""
        service.add_update("101", "Renamed Noodle", 99, 9.9, "NewCat")
        assert service.inventory["101"] == Product("101", "Renamed Noodle", 99, 9.9, "NewCat")

    def test_preserves_other_items(self, service):
        service.add_update("NEW", "Extra", 5, 5.0, "T")
        assert {"101", "102", "103"} <= set(service.inventory)

    def test_persists_to_file(self, service, repo):
        """เพิ่มสินค้าแล้วต้องบันทึกลงไฟล์ทันที"""
        service.add_update("NEW", "Extra", 5, 5.0, "T")
        assert "NEW" in repo.load()

    def test_rejects_invalid_and_does_not_persist(self, service, repo):
        ok, msg = service.add_update("BAD", "Bad", -1, 5.0, "T")
        assert ok is False
        assert "BAD" not in service.inventory
        assert "BAD" not in repo.load()


class TestServiceStockOut:

    def test_normal_cut_reduces_qty(self, service):
        ok, msg = service.stock_out("101", 10)
        assert ok is True
        assert "Stock updated" in msg
        assert service.inventory["101"].qty == 40

    def test_cut_exact_amount_results_in_zero(self, service):
        ok, _ = service.stock_out("101", 50)
        assert ok is True
        assert service.inventory["101"].qty == 0

    def test_cut_more_than_available_fails(self, service):
        ok, msg = service.stock_out("101", 999)
        assert ok is False
        assert "Not enough stock" in msg
        assert service.inventory["101"].qty == 50

    def test_nonexistent_product_fails(self, service):
        ok, msg = service.stock_out("999", 1)
        assert ok is False
        assert "not found" in msg.lower()

    def test_INV7_negative_amount_rejected(self, service):
        """[INV-7] จำนวนติดลบต้องไม่ผ่าน และสต๊อกต้องไม่เปลี่ยน"""
        ok, _ = service.stock_out("101", -5)
        assert ok is False
        assert service.inventory["101"].qty == 50

    def test_INV7_zero_amount_rejected(self, service):
        ok, _ = service.stock_out("101", 0)
        assert ok is False
        assert service.inventory["101"].qty == 50

    def test_warns_when_below_low_stock(self, service):
        """[INV-9] เหลือน้อยกว่า LOW_STOCK (10) ต้องเตือน"""
        ok, msg = service.stock_out("102", 12)  # 20 → 8
        assert ok is True
        assert "WARNING" in msg

    def test_no_warning_when_exactly_low_stock(self, service):
        """qty = 10 พอดี ยังไม่เตือน (เงื่อนไขคือ < ไม่ใช่ <=)"""
        ok, msg = service.stock_out("102", 10)  # 20 → 10
        assert ok is True
        assert "WARNING" not in msg

    def test_persists_to_file(self, service, repo):
        service.stock_out("101", 10)
        assert repo.load()["101"].qty == 40

    def test_failed_cut_does_not_persist(self, service, repo):
        service.stock_out("101", 999)
        assert repo.load()["101"].qty == 50


class TestServiceGetSummary:

    def test_default_inventory_totals(self, service):
        """101: 50×6 + 102: 20×12 + 103: 100×10 = 1,540 THB"""
        total_items, total_val, low = service.get_summary()
        assert total_items == 3
        assert total_val == pytest.approx(1540.0)
        assert low == []

    def test_empty_inventory(self, repo):
        repo.path.write_text("{}")
        total_items, total_val, low = InventoryService(repo).get_summary()
        assert (total_items, total_val, low) == (0, 0.0, [])

    def test_lists_low_stock_names(self, service):
        service.add_update("A", "BelowTen", 9, 1.0, "T")
        service.add_update("B", "AtTen", 10, 1.0, "T")
        _, _, low = service.get_summary()
        assert "BelowTen" in low
        assert "AtTen" not in low

    def test_zero_qty_counts_as_low_stock(self, service):
        service.add_update("A", "Gone", 0, 10.0, "T")
        assert "Gone" in service.get_summary()[2]

    def test_float_precision(self, repo):
        repo.path.write_text(json.dumps({"X": {"n": "Precise", "q": 3, "p": 33.33, "c": "T"}}))
        assert InventoryService(repo).get_summary()[1] == pytest.approx(99.99)

    def test_low_stock_threshold_is_ten(self):
        """ล็อกค่าเกณฑ์ให้ตรงกับ LOW_STOCK เดิม"""
        assert InventoryService.LOW_STOCK == 10


# ══════════════════════════════════════════════════
# SAM1-39: ConsoleUI — menu routing & input handling
# ══════════════════════════════════════════════════

@pytest.fixture
def make_ui(service):
    """
    สร้าง ConsoleUI ที่ป้อน input จากลิสต์และเก็บ output ไว้ตรวจ
    คืน (ui, outputs) โดย outputs เป็นข้อความทุกบรรทัดที่ถูกพิมพ์
    """
    def _make(inputs):
        queue = list(inputs)
        outputs = []
        ui = ConsoleUI(
            service,
            input_fn=lambda prompt="": queue.pop(0),
            print_fn=lambda *args: outputs.append(" ".join(str(a) for a in args)),
        )
        return ui, outputs
    return _make


def joined(outputs):
    return "\n".join(outputs)


class TestConsoleUIRouting:

    def test_exit_stops_the_loop(self, make_ui):
        ui, outputs = make_ui(["5"])
        ui.run()
        assert "Bye" in joined(outputs)

    def test_invalid_choice_reprompts_then_exits(self, make_ui):
        ui, outputs = make_ui(["9", "5"])
        ui.run()
        assert "Invalid choice" in joined(outputs)

    @pytest.mark.parametrize("choice, handler", [
        ("1", "handle_show"),
        ("2", "handle_add"),
        ("3", "handle_out"),
        ("4", "handle_summary"),
    ])
    def test_each_menu_routes_to_its_handler(self, make_ui, choice, handler):
        ui, _ = make_ui([choice, "5"])
        called = []
        setattr(ui, handler, lambda: called.append(handler))
        ui.run()
        assert called == [handler]


class TestConsoleUIShow:

    def test_lists_every_product(self, make_ui):
        ui, outputs = make_ui([])
        ui.handle_show()
        text = joined(outputs)
        for name in ("Mama Noodles", "Lactasoy Milk", "Singha Water"):
            assert name in text

    def test_shows_id_and_stock(self, make_ui):
        ui, outputs = make_ui([])
        ui.handle_show()
        assert "101" in joined(outputs)
        assert "50" in joined(outputs)


class TestConsoleUIAdd:

    def test_adds_product_from_input(self, make_ui, service):
        ui, _ = make_ui(["NEW", "New Product", "30", "15.0", "Test"])
        ui.handle_add()
        assert service.inventory["NEW"] == Product("NEW", "New Product", 30, 15.0, "Test")

    def test_INV6_non_numeric_qty_is_rejected(self, make_ui, service):
        """[INV-6] พิมพ์ตัวอักษรในช่อง Qty ต้องไม่ crash และต้องไม่บันทึก"""
        ui, outputs = make_ui(["BAD", "Bad Item", "abc"])
        ui.handle_add()
        assert "must be numbers" in joined(outputs)
        assert "BAD" not in service.inventory

    def test_INV6_non_numeric_price_is_rejected(self, make_ui, service):
        ui, outputs = make_ui(["BAD", "Bad Item", "10", "xyz"])
        ui.handle_add()
        assert "must be numbers" in joined(outputs)
        assert "BAD" not in service.inventory

    def test_negative_qty_is_rejected_by_service(self, make_ui, service):
        ui, outputs = make_ui(["BAD", "Bad Item", "-1", "5.0", "T"])
        ui.handle_add()
        assert "must not be negative" in joined(outputs)
        assert "BAD" not in service.inventory


class TestConsoleUIStockOut:

    def test_cuts_stock_from_input(self, make_ui, service):
        ui, outputs = make_ui(["101", "10"])
        ui.handle_out()
        assert service.inventory["101"].qty == 40
        assert "Stock updated" in joined(outputs)

    def test_INV6_non_numeric_amount_is_rejected(self, make_ui, service):
        ui, outputs = make_ui(["101", "abc"])
        ui.handle_out()
        assert "must be a number" in joined(outputs)
        assert service.inventory["101"].qty == 50

    def test_INV7_negative_amount_is_rejected(self, make_ui, service):
        ui, outputs = make_ui(["101", "-5"])
        ui.handle_out()
        assert "greater than zero" in joined(outputs)
        assert service.inventory["101"].qty == 50

    def test_unknown_product_reports_not_found(self, make_ui):
        ui, outputs = make_ui(["999", "1"])
        ui.handle_out()
        assert "not found" in joined(outputs).lower()

    def test_low_stock_warning_is_shown(self, make_ui):
        ui, outputs = make_ui(["102", "12"])  # 20 → 8
        ui.handle_out()
        assert "WARNING" in joined(outputs)


class TestConsoleUISummary:

    def test_prints_totals(self, make_ui):
        ui, outputs = make_ui([])
        ui.handle_summary()
        text = joined(outputs)
        assert "3" in text
        assert "1540" in text.replace(",", "")

    def test_prints_low_stock_alert(self, make_ui, service):
        service.add_update("A", "Almost Gone", 2, 1.0, "T")
        ui, outputs = make_ui([])
        ui.handle_summary()
        assert "Almost Gone" in joined(outputs)


# ══════════════════════════════════════════════════
# SAM1-40: Integration — ทั้ง 4 คลาสทำงานร่วมกัน
# ══════════════════════════════════════════════════

class TestIntegration:

    def test_full_flow_persists_across_restart(self, tmp_path):
        """
        เพิ่มสินค้า → ตัดสต๊อก → ปิดโปรแกรม → เปิดใหม่แล้วข้อมูลต้องยังอยู่
        ครอบทั้ง Repository → Service → ConsoleUI
        """
        path = str(tmp_path / "data_test.json")
        inputs = iter([
            "2", "P01", "Widget", "25", "4.0", "Tools",   # เพิ่มสินค้าใหม่
            "3", "P01", "20",                              # ตัดออก 20 เหลือ 5
            "4",                                           # ดูสรุป
            "5",                                           # ออก
        ])
        outputs = []
        service = InventoryService(InventoryRepository(path))
        ConsoleUI(
            service,
            input_fn=lambda prompt="": next(inputs),
            print_fn=lambda *args: outputs.append(" ".join(str(a) for a in args)),
        ).run()

        # เตือนสต๊อกต่ำตอนตัด และโชว์ในสรุป
        text = joined(outputs)
        assert "WARNING" in text
        assert "Widget" in text

        # เปิดโปรแกรมใหม่ด้วย instance ชุดใหม่ ข้อมูลต้องตรง
        reloaded = InventoryService(InventoryRepository(path))
        assert reloaded.inventory["P01"] == Product("P01", "Widget", 5, 4.0, "Tools")
        assert reloaded.get_summary()[0] == 4  # default 3 + Widget
