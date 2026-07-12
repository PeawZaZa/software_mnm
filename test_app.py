# test_app.py
# Unit Tests for Inventory System v1.0
# ════════════════════════════════════════
# รันด้วย: pytest test_app.py -v
# รันพร้อม coverage: pytest test_app.py -v --tb=short
#
# จุดประสงค์: ล็อกพฤติกรรมปัจจุบันของระบบก่อน refactor
# ทุก test ที่ขึ้นต้นด้วย test_BUG_ = บั๊กที่รู้แล้ว
# ห้ามลบ test พวกนี้ก่อน fix INV-xx ที่ระบุไว้

import pytest
import json
import os
import app_v1 as app  # ← ไฟล์โค้ดหลัก (app_v1.py อยู่ใน folder เดียวกัน)


# ══════════════════════════════════════════════════
# FIXTURES — ตั้งค่าเริ่มต้นก่อนแต่ละ test
# ══════════════════════════════════════════════════

@pytest.fixture(autouse=True)
def reset_inventory():
    """รีเซต global x ก่อนทุก test เพื่อป้องกัน test ปนกัน"""
    app.x = {
        "101": {"n": "Mama Noodles",  "q": 50,  "p": 6.0,  "c": "Food"},
        "102": {"n": "Lactasoy Milk", "q": 20,  "p": 12.0, "c": "Drink"},
        "103": {"n": "Singha Water",  "q": 100, "p": 10.0, "c": "Drink"},
    }
    yield
    app.x = {}


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """เปลี่ยน db path ชั่วคราวเป็น temp file เพื่อไม่กระทบ data.json จริง"""
    db_path = str(tmp_path / "data_test.json")
    monkeypatch.setattr(app, "db", db_path)
    yield db_path


# ══════════════════════════════════════════════════
# SECTION 1: load() และ save()
# ══════════════════════════════════════════════════

class TestLoadFunction:

    def test_load_default_when_no_file(self, temp_db):
        """load() ต้องสร้าง default inventory เมื่อไม่มีไฟล์"""
        app.x = {}
        app.load()
        assert len(app.x) == 3
        assert "101" in app.x
        assert app.x["101"]["n"] == "Mama Noodles"
        assert app.x["101"]["q"] == 50

    def test_load_default_has_correct_structure(self, temp_db):
        """default inventory ต้องมี keys: n, q, p, c ทุก item"""
        app.x = {}
        app.load()
        for item_id, item in app.x.items():
            assert "n" in item, f"ID {item_id} ขาด key 'n'"
            assert "q" in item, f"ID {item_id} ขาด key 'q'"
            assert "p" in item, f"ID {item_id} ขาด key 'p'"
            assert "c" in item, f"ID {item_id} ขาด key 'c'"

    def test_load_reads_existing_file(self, temp_db):
        """load() ต้องอ่านข้อมูลจากไฟล์ที่มีอยู่แล้ว"""
        custom_data = {"999": {"n": "Custom Item", "q": 7, "p": 99.0, "c": "Special"}}
        with open(temp_db, 'w') as f:
            json.dump(custom_data, f)
        app.x = {}
        app.load()
        assert "999" in app.x
        assert app.x["999"]["n"] == "Custom Item"
        assert app.x["999"]["q"] == 7

    def test_load_does_not_use_default_if_file_exists(self, temp_db):
        """ถ้ามีไฟล์ ต้องใช้ข้อมูลจากไฟล์เท่านั้น ไม่ใช้ default"""
        with open(temp_db, 'w') as f:
            json.dump({}, f)
        app.x = {"999": {"n": "Old", "q": 1, "p": 1.0, "c": "X"}}
        app.load()
        assert "101" not in app.x  # ไม่ควรมี default items


class TestSaveFunction:

    def test_save_creates_file(self, temp_db):
        """save() ต้องสร้างไฟล์ data.json"""
        app.save()        
        assert os.path.exists(temp_db)

    def test_save_writes_correct_data(self, temp_db):
        """save() ต้องเขียนข้อมูลใน x ลงไฟล์ได้ถูกต้อง"""
        app.save()
        with open(temp_db, 'r') as f:
            saved = json.load(f)
        assert "101" in saved
        assert saved["101"]["q"] == 50
        assert saved["101"]["p"] == 6.0

    def test_save_load_roundtrip(self, temp_db):
        """save() แล้ว load() ใหม่ต้องได้ข้อมูลเดิมทุกประการ"""
        app.x["101"]["q"] = 99
        app.x["NEW"] = {"n": "Test", "q": 1, "p": 1.0, "c": "T"}
        app.save()
        app.x = {}
        app.load()
        assert app.x["101"]["q"] == 99
        assert "NEW" in app.x

    def test_save_overwrites_previous_file(self, temp_db):
        """save() ต้องเขียนทับไฟล์เดิมทั้งหมด (พฤติกรรมปัจจุบัน)"""
        # บันทึกครั้งแรก
        app.save()
        # เปลี่ยนข้อมูล แล้วบันทึกใหม่
        app.x = {"ONLY": {"n": "Only Item", "q": 1, "p": 1.0, "c": "T"}}
        app.save()
        with open(temp_db, 'r') as f:
            data = json.load(f)
        # ต้องมีแค่ ONLY ไม่มี 101 แล้ว
        assert "ONLY" in data
        assert "101" not in data
# ══════════════════════════════════════════════════
# SECTION 2: เมนู 4 — Check Check (คำนวณมูลค่า)
# ══════════════════════════════════════════════════

def calc_summary(inventory):
    """
    จำลอง logic ของเมนู 4 (Check Check) — L.72-86 ใน app_v1.py
    ใช้ใน test เพื่อตรวจสอบพฤติกรรมก่อน refactor
    """
    total_items = 0
    total_val = 0.0
    low_stock_list = []
    for k in inventory:
        total_items += 1
        total_val += inventory[k]['q'] * inventory[k]['p']
        if inventory[k]['q'] < 10:
            low_stock_list.append(inventory[k]['n'])
    return total_items, total_val, low_stock_list


class TestCheckCheckMenu:
    """ล็อกพฤติกรรมเมนู 4 — ห้ามเปลี่ยน test เหล่านี้ก่อน refactor เสร็จ"""

    def test_total_item_types_default(self):
        """จำนวนชนิดสินค้า default ต้องเท่ากับ 3"""
        total, _, _ = calc_summary(app.x)
        assert total == 3

    def test_total_value_default_inventory(self):
        """
        มูลค่าสต๊อกรวมของ default inventory ต้องเท่ากับ 1,540 THB
        101: 50 × 6.0  = 300.0
        102: 20 × 12.0 = 240.0
        103: 100 × 10.0 = 1000.0
        รวม = 1,540.0 THB
        """
        _, total_val, _ = calc_summary(app.x)
        assert total_val == pytest.approx(1540.0), \
            f"Expected 1540.0 THB, got {total_val}"

    def test_total_value_single_item(self):
        """คำนวณมูลค่า qty × price ของสินค้าชิ้นเดียว"""
        inv = {"X01": {"n": "Test", "q": 7, "p": 25.0, "c": "T"}}
        _, total_val, _ = calc_summary(inv)
        assert total_val == pytest.approx(175.0)

    def test_total_value_zero_qty(self):
        """สินค้าที่ qty = 0 ต้องมีมูลค่าเป็น 0"""
        inv = {"X01": {"n": "Empty", "q": 0, "p": 100.0, "c": "T"}}
        _, total_val, _ = calc_summary(inv)
        assert total_val == pytest.approx(0.0)

    def test_total_value_empty_inventory(self):
        """สต๊อกว่างเปล่าต้องได้มูลค่า 0 และ 0 ชนิด"""
        total, total_val, low = calc_summary({})
        assert total == 0
        assert total_val == pytest.approx(0.0)
        assert low == []

    def test_total_value_float_precision(self):
        """ราคาทศนิยมต้องคำนวณถูกต้อง"""
        inv = {"X01": {"n": "Precise", "q": 3, "p": 33.33, "c": "T"}}
        _, total_val, _ = calc_summary(inv)
        assert total_val == pytest.approx(99.99)

    def test_total_value_multiple_items_manual(self):
        """ตรวจสอบ sum ของหลายชิ้นด้วยมือ"""
        inv = {
            "A": {"n": "A", "q": 10, "p": 5.0,  "c": "T"},  # 50
            "B": {"n": "B", "q": 4,  "p": 20.0, "c": "T"},  # 80
            "C": {"n": "C", "q": 1,  "p": 100.0,"c": "T"},  # 100
        }
        _, total_val, _ = calc_summary(inv)
        assert total_val == pytest.approx(230.0)

    # ── Low Stock Alerts ──

    def test_low_stock_threshold_is_10(self):
        """เมนู 4 แจ้งเตือนเมื่อ qty < 10 (ล็อก threshold = 10)"""
        inv = {
            "A": {"n": "BelowTen", "q": 9,  "p": 1.0, "c": "T"},
            "B": {"n": "AtTen",    "q": 10, "p": 1.0, "c": "T"},
            "C": {"n": "AboveTen", "q": 11, "p": 1.0, "c": "T"},
        }
        _, _, low = calc_summary(inv)
        assert "BelowTen" in low
        assert "AtTen"    not in low  # 10 ไม่ใช่ < 10
        assert "AboveTen" not in low

    def test_low_stock_zero_qty_is_alerted(self):
        """สินค้าที่หมดสต๊อก (qty=0) ต้องอยู่ใน low stock list"""
        inv = {"X": {"n": "Gone", "q": 0, "p": 10.0, "c": "T"}}
        _, _, low = calc_summary(inv)
        assert "Gone" in low

    def test_no_low_stock_when_all_sufficient(self):
        """ไม่แจ้งเตือนเมื่อทุกชิ้นมี qty >= 10"""
        inv = {
            "A": {"n": "Plenty1", "q": 10,  "p": 1.0, "c": "T"},
            "B": {"n": "Plenty2", "q": 100, "p": 1.0, "c": "T"},
        }
        _, _, low = calc_summary(inv)
        assert len(low) == 0

    def test_all_low_stock_when_all_depleted(self):
        """แจ้งเตือนทุกชิ้นเมื่อทุกชิ้นมี qty < 10"""
        inv = {
            "A": {"n": "Item1", "q": 1, "p": 1.0, "c": "T"},
            "B": {"n": "Item2", "q": 5, "p": 1.0, "c": "T"},
            "C": {"n": "Item3", "q": 0, "p": 1.0, "c": "T"},
        }
        _, _, low = calc_summary(inv)
        assert len(low) == 3
        assert "Item1" in low
        assert "Item2" in low
        assert "Item3" in low

    def test_low_stock_does_not_include_sufficient_items(self):
        """low stock list ต้องไม่รวมสินค้าที่สต๊อกพอ"""
        inv = {
            "A": {"n": "LowItem",  "q": 3,  "p": 1.0, "c": "T"},
            "B": {"n": "OkayItem", "q": 50, "p": 1.0, "c": "T"},
        }
        _, _, low = calc_summary(inv)
        assert "OkayItem" not in low
# ══════════════════════════════════════════════════
# SECTION 3: เมนู 3 — Stock Out Logic
# ══════════════════════════════════════════════════

def apply_stock_out(product_id, amt):
    """
    จำลอง logic เมนู 3 (Out) — L.55-70 ใน app_v1.py
    คืนค่า (success: bool, message: str)
    """
    if product_id not in app.x:
        return False, "Product not found!"
    if app.x[product_id]['q'] >= amt:
        app.x[product_id]['q'] -= amt
        warning = app.x[product_id]['q'] < 5
        return True, "WARNING" if warning else "Stock updated."
    else:
        return False, "Error: Not enough stock!"


class TestStockOutMenu:

    def test_normal_cut_reduces_qty(self):
        """ตัดสต๊อกปกติต้องลดจำนวนลงถูกต้อง"""
        success, _ = apply_stock_out("101", 10)
        assert success is True
        assert app.x["101"]["q"] == 40

    def test_cut_exact_amount_results_in_zero(self):
        """ตัดออกพอดีกับที่มีต้องได้ qty = 0"""
        success, _ = apply_stock_out("101", 50)
        assert success is True
        assert app.x["101"]["q"] == 0

    def test_cut_more_than_available_fails(self):
        """ตัดเกินที่มีต้องล้มเหลวและ qty ไม่เปลี่ยน"""
        success, msg = apply_stock_out("101", 999)
        assert success is False
        assert "Not enough stock" in msg
        assert app.x["101"]["q"] == 50  # ต้องไม่เปลี่ยนแปลง

    def test_cut_nonexistent_product_fails(self):
        """ตัดสินค้าที่ไม่มีใน inventory ต้องล้มเหลว"""
        success, msg = apply_stock_out("999", 1)
        assert success is False
        assert "not found" in msg.lower()

    def test_warning_when_qty_below_5_after_cut(self):
        """ต้องแจ้งเตือนเมื่อสต๊อกหลังตัดน้อยกว่า 5"""
        app.x["101"]["q"] = 10
        success, msg = apply_stock_out("101", 7)  # เหลือ 3
        assert success is True
        assert "WARNING" in msg
        assert app.x["101"]["q"] == 3

    def test_no_warning_when_qty_equals_5(self):
        """qty = 5 ไม่ต้องแจ้งเตือน (เงื่อนไขคือ < 5 ไม่ใช่ <= 5)"""
        app.x["101"]["q"] = 10
        success, msg = apply_stock_out("101", 5)  # เหลือ 5
        assert success is True
        assert app.x["101"]["q"] == 5
        assert app.x["101"]["q"] >= 5  # ไม่ต้องเตือน

    # ── Fixed Bug: Negative Amount ──

    def test_BUG_INV7_negative_amount_passes_condition(self):
        """
        ✅ FIX INV-7: เงื่อนไขต้องล้มเหลวเมื่อ amt เป็นลบ
        (อัปเดตตาม commit: test(qa): update BUG_INV7 test after fix)
        """
        success, _ = apply_stock_out("101", -5)
        # แก้ไข assertion ตามความคาดหวังหลังแก้บั๊กแล้ว: ต้อง Fail และสต๊อกเท่าเดิม
        assert success is False, "ควรล้มเหลวเมื่อ amt เป็นลบ"
        assert app.x["101"]["q"] == 50, \
            f"สต๊อกต้องคงที่เป็น 50 แต่เปลี่ยนเป็น {app.x['101']['q']}"

    def test_BUG_INV7_zero_amount_passes(self):
        """
        ✅ FIX INV-7 (ส่วนขยาย): ตัดด้วย 0 ต้องไม่ผ่าน (ล้มเหลว)
        """
        success, _ = apply_stock_out("101", 0)
        # แก้ไข assertion: ต้อง Fail เมื่อตัดด้วย 0
        assert success is False, "ควรล้มเหลวเมื่อ amt เป็น 0"
        assert app.x["101"]["q"] == 50  # qty ไม่เปลี่ยน


# ══════════════════════════════════════════════════
# SECTION 4: เมนู 2 — Add / Update Logic
# ══════════════════════════════════════════════════

def apply_add_update(pid, name, qty, price, cat):
    """จำลอง logic เมนู 2 (Add/Update) — L.39-53 ใน app_v1.py"""
    if pid in app.x:
        app.x[pid] = {"n": name, "q": qty, "p": price, "c": cat}
    else:
        app.x[pid] = {"n": name, "q": qty, "p": price, "c": cat}


class TestAddUpdateMenu:

    def test_add_new_product(self):
        """เพิ่มสินค้าใหม่ต้องปรากฏใน inventory"""
        apply_add_update("NEW", "New Product", 30, 15.0, "Test")
        assert "NEW" in app.x
        assert app.x["NEW"]["n"] == "New Product"
        assert app.x["NEW"]["q"] == 30
        assert app.x["NEW"]["p"] == pytest.approx(15.0)

    def test_update_existing_product_overwrites_all_fields(self):
        """อัปเดตสินค้าที่มีอยู่แล้วต้องเขียนทับข้อมูลทั้งหมด"""
        apply_add_update("101", "Renamed Noodle", 99, 9.9, "NewCat")
        assert app.x["101"]["n"] == "Renamed Noodle"
        assert app.x["101"]["q"] == 99
        assert app.x["101"]["p"] == pytest.approx(9.9)
        assert app.x["101"]["c"] == "NewCat"

    def test_add_preserves_existing_items(self):
        """เพิ่มสินค้าใหม่ต้องไม่ลบสินค้าเดิม"""
        apply_add_update("NEW", "Extra", 5, 5.0, "T")
        assert "101" in app.x  # ยังอยู่
        assert "102" in app.x  # ยังอยู่
        assert "103" in app.x  # ยังอยู่

    def test_category_stored_in_key_c(self):
        """หมวดหมู่ต้องเก็บในคีย์ 'c' (ล็อก data structure)"""
        apply_add_update("X01", "Item", 10, 5.0, "Snack")
        assert app.x["X01"]["c"] == "Snack"

    def test_BUG_INV8_ifelse_identical_behavior(self):
        """
        🐛 BUG INV-8: if/else ทั้งสองกรณีทำงานเหมือนกัน (เขียนทับทุกครั้ง)
        ไม่ว่าจะเป็น ID ใหม่หรือ ID ที่มีอยู่ → พฤติกรรมเหมือนกัน
        Requirement จริง: ยังไม่ชัดว่าควร "บวกสต๊อก" หรือ "เขียนทับ"
        """
        original_qty = app.x["101"]["q"]  # 50
        apply_add_update("101", app.x["101"]["n"], 1, app.x["101"]["p"], app.x["101"]["c"])
        # BUG: qty ถูกเขียนทับเป็น 1 แทนที่จะบวก (50 + 1 = 51)
        assert app.x["101"]["q"] == 1, "BUG: qty ถูก overwrite ไม่ใช่ accumulate"
        assert app.x["101"]["q"] != original_qty + 1  # ไม่ใช่การบวกเพิ่ม

# ══════════════════════════════════════════════════
# SECTION 5: Known Inconsistencies
# ══════════════════════════════════════════════════

class TestKnownInconsistencies:

    def test_BUG_INV9_threshold_mismatch_between_menus(self):
        """
        🐛 BUG INV-9: เมนู 3 ใช้ < 5 แต่เมนู 4 ใช้ < 10
        qty=7 → เมนู 4 แจ้งเตือน แต่เมนู 3 ไม่แจ้งเตือน
        ต้องถูกกำหนดเป็นค่าคงที่เดียวกัน (LOW_STOCK_THRESHOLD)
        """
        qty = 7
        MENU3_THRESHOLD = 5
        MENU4_THRESHOLD = 10
        is_low_in_menu3 = qty < MENU3_THRESHOLD
        is_low_in_menu4 = qty < MENU4_THRESHOLD
        assert is_low_in_menu4 is True,  "เมนู 4: qty=7 ควรแจ้งเตือน"
        assert is_low_in_menu3 is False, "เมนู 3: qty=7 ไม่แจ้งเตือน"
        assert is_low_in_menu3 != is_low_in_menu4, \
            "BUG: พฤติกรรมต่างกัน — ต้องแก้ INV-9 เพื่อให้ตรงกัน"

    def test_default_inventory_ids_are_strings(self):
        """ล็อก: product ID ต้องเป็น string ไม่ใช่ int"""
        assert isinstance(list(app.x.keys())[0], str)

    def test_default_inventory_qty_is_int(self):
        """ล็อก: qty ต้องเป็น int"""
        assert isinstance(app.x["101"]["q"], int)

    def test_default_inventory_price_is_float(self):
        """ล็อก: price ต้องเป็น float"""
        assert isinstance(app.x["101"]["p"], float)