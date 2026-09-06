# test_app_v2.py
# Unit Tests สำหรับสถาปัตยกรรม class-based (Sprint 2)
# ════════════════════════════════════════
# รันด้วย: pytest test_app_v2.py -v
#
# ต่างจาก test_app.py ตรงที่ไฟล์นี้เรียกคลาส "ของจริง" ใน app_v2.py
# ไม่ใช่ฟังก์ชันจำลอง (calc_summary / apply_stock_out) แบบไฟล์เดิม

import json

import pytest

from app_v2 import InventoryRepository, Product


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
