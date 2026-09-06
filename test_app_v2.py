# test_app_v2.py
# Unit Tests สำหรับสถาปัตยกรรม class-based (Sprint 2)
# ════════════════════════════════════════
# รันด้วย: pytest test_app_v2.py -v
#
# ต่างจาก test_app.py ตรงที่ไฟล์นี้เรียกคลาส "ของจริง" ใน app_v2.py
# ไม่ใช่ฟังก์ชันจำลอง (calc_summary / apply_stock_out) แบบไฟล์เดิม

import pytest

from app_v2 import Product


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
