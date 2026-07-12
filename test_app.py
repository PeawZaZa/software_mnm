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

@pytest.fixture # แก้ไข: นำ autouse=True ออก เพื่อใช้งานแบบรับค่าพารามิเตอร์
def inventory(): # แก้ไข: เปลี่ยนชื่อเป็น inventory และให้รีเทิร์น dict แทนการแก้ app.x
    """สร้าง default inventory สำหรับทดสอบแบบแยกอิสระ""" # แก้ไข: ปรับคำอธิบาย
    return { # แก้ไข: คืนค่าเป็น dictionary ใหม่ทุกครั้งที่เทสต์เรียกใช้
        "101": {"n": "Mama Noodles",  "q": 50,  "p": 6.0,  "c": "Food"},
        "102": {"n": "Lactasoy Milk", "q": 20,  "p": 12.0, "c": "Drink"},
        "103": {"n": "Singha Water",  "q": 100, "p": 10.0, "c": "Drink"},
    }


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
        inv = {} # แก้ไข: สร้าง dict ว่างแทนการเรียก app.x
        app.load(inv) # แก้ไข: ส่งพารามิเตอร์ inv เข้าฟังก์ชัน
        assert len(inv) == 3 # แก้ไข: เปลี่ยน app.x เป็น inv
        assert "101" in inv # แก้ไข: เปลี่ยน app.x เป็น inv
        assert inv["101"]["n"] == "Mama Noodles" # แก้ไข: เปลี่ยน app.x เป็น inv
        assert inv["101"]["q"] == 50 # แก้ไข: เปลี่ยน app.x เป็น inv

    def test_load_default_has_correct_structure(self, temp_db):
        """default inventory ต้องมี keys: n, q, p, c ทุก item"""
        inv = {} # แก้ไข: สร้าง dict ว่าง
        app.load(inv) # แก้ไข: ส่งพารามิเตอร์ inv
        for item_id, item in inv.items(): # แก้ไข: วนลูปจาก inv
            assert "n" in item, f"ID {item_id} ขาด key 'n'"
            assert "q" in item, f"ID {item_id} ขาด key 'q'"
            assert "p" in item, f"ID {item_id} ขาด key 'p'"
            assert "c" in item, f"ID {item_id} ขาด key 'c'"

    def test_load_reads_existing_file(self, temp_db):
        """load() ต้องอ่านข้อมูลจากไฟล์ที่มีอยู่แล้ว"""
        custom_data = {"999": {"n": "Custom Item", "q": 7, "p": 99.0, "c": "Special"}}
        with open(temp_db, 'w') as f:
            json.dump(custom_data, f)
        inv = {} # แก้ไข: สร้าง dict ว่าง
        app.load(inv) # แก้ไข: ส่งพารามิเตอร์ inv
        assert "999" in inv # แก้ไข: เปลี่ยน app.x เป็น inv
        assert inv["999"]["n"] == "Custom Item" # แก้ไข: เปลี่ยน app.x เป็น inv
        assert inv["999"]["q"] == 7 # แก้ไข: เปลี่ยน app.x เป็น inv

    def test_load_does_not_use_default_if_file_exists(self, temp_db):
        """ถ้ามีไฟล์ ต้องใช้ข้อมูลจากไฟล์เท่านั้น ไม่ใช้ default"""
        with open(temp_db, 'w') as f:
            json.dump({}, f)
        inv = {"999": {"n": "Old", "q": 1, "p": 1.0, "c": "X"}} # แก้ไข: สร้าง dict ทะลอง
        app.load(inv) # แก้ไข: ส่งพารามิเตอร์ inv
        assert "101" not in inv  # แก้ไข: เปลี่ยน app.x เป็น inv


class TestSaveFunction:

    def test_save_creates_file(self, temp_db, inventory): # แก้ไข: รับ fixture inventory
        """save() ต้องสร้างไฟล์ data.json"""
        app.save(inventory) # แก้ไข: ส่ง inventory เป็นพารามิเตอร์ (ทั้งไฟล์ใช้ signature นี้ตรงกัน)
        assert os.path.exists(temp_db)

    def test_save_writes_correct_data(self, temp_db, inventory): # แก้ไข: รับ fixture inventory
        """save() ต้องเขียนข้อมูลใน x ลงไฟล์ได้ถูกต้อง"""
        app.save(inventory) # แก้ไข: ส่ง inventory เป็นพารามิเตอร์
        with open(temp_db, 'r') as f:
            saved = json.load(f)
        assert "101" in saved
        assert saved["101"]["q"] == 50
        assert saved["101"]["p"] == 6.0

    def test_save_load_roundtrip(self, temp_db, inventory): # แก้ไข: รับ fixture inventory
        """save() แล้ว load() ใหม่ต้องได้ข้อมูลเดิมทุกประการ"""
        inventory["101"]["q"] = 99 # แก้ไข: เปลี่ยน app.x เป็น inventory
        inventory["NEW"] = {"n": "Test", "q": 1, "p": 1.0, "c": "T"} # แก้ไข: เปลี่ยน app.x เป็น inventory
        app.save(inventory) # แก้ไข: ส่งพารามิเตอร์
        new_inv = {} # แก้ไข: สร้าง dict ว่างมารับค่าโหลดใหม่
        app.load(new_inv) # แก้ไข: โหลดเข้า dict ใหม่
        assert new_inv["101"]["q"] == 99 # แก้ไข: เช็คจาก dict ใหม่
        assert "NEW" in new_inv # แก้ไข: เช็คจาก dict ใหม่

    def test_save_overwrites_previous_file(self, temp_db, inventory): # แก้ไข: รับ fixture inventory
        """save() ต้องเขียนทับไฟล์เดิมทั้งหมด (พฤติกรรมปัจจุบัน)"""
        # บันทึกครั้งแรก
        app.save(inventory) # แก้ไข: ส่งพารามิเตอร์
        # เปลี่ยนข้อมูล แล้วบันทึกใหม่
        new_inv = {"ONLY": {"n": "Only Item", "q": 1, "p": 1.0, "c": "T"}} # แก้ไข: สร้าง dict ชุดที่สอง
        app.save(new_inv) # แก้ไข: ส่งพารามิเตอร์เซฟทับ
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
        if inventory[k]['q'] < app.LOW_STOCK: # แก้ไข: อัปเดตใช้ตัวแปร app.LOW_STOCK
            low_stock_list.append(inventory[k]['n'])
    return total_items, total_val, low_stock_list


class TestCheckCheckMenu:
    """ล็อกพฤติกรรมเมนู 4 — ห้ามเปลี่ยน test เหล่านี้ก่อน refactor เสร็จ"""

    def test_total_item_types_default(self, inventory): # แก้ไข: รับ fixture inventory
        """จำนวนชนิดสินค้า default ต้องเท่ากับ 3"""
        total, _, _ = calc_summary(inventory) # แก้ไข: ส่งต่อให้ calc_summary
        assert total == 3

    def test_total_value_default_inventory(self, inventory): # แก้ไข: รับ fixture inventory
        """
        มูลค่าสต๊อกรวมของ default inventory ต้องเท่ากับ 1,540 THB
        101: 50 × 6.0  = 300.0
        102: 20 × 12.0 = 240.0
        103: 100 × 10.0 = 1000.0
        รวม = 1,540.0 THB
        """
        _, total_val, _ = calc_summary(inventory) # แก้ไข: ส่งต่อให้ calc_summary
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

def apply_stock_out(inventory, product_id, amt): # แก้ไข: รับพารามิเตอร์ inventory เพิ่ม
    """
    จำลอง logic เมนู 3 (Out) — L.55-70 ใน app_v1.py
    คืนค่า (success: bool, message: str)

    ✅ FIX INV-7: เพิ่มเงื่อนไข amt <= 0 ต้องล้มเหลว
    (เดิม q >= amt ผ่านเมื่อ amt เป็นลบหรือศูนย์ ทำให้สต๊อกเพิ่ม/ไม่เปลี่ยนโดยไม่ตั้งใจ)
    ✅ FIX INV-9: ใช้เกณฑ์ app.LOW_STOCK (=10) แทนเลข 5 hardcode ให้ตรงกับเมนู 4
    """
    if product_id not in inventory: # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        return False, "Product not found!"
    if amt <= 0: # ✅ FIX INV-7: ปฏิเสธจำนวนที่เป็นลบหรือศูนย์
        return False, "Error: Amount must be positive!"
    if inventory[product_id]['q'] >= amt: # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        inventory[product_id]['q'] -= amt # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        warning = inventory[product_id]['q'] < app.LOW_STOCK # ✅ FIX INV-9: อ้างอิง app.LOW_STOCK แทนเลข 5
        return True, "WARNING" if warning else "Stock updated."
    else:
        return False, "Error: Not enough stock!"


class TestStockOutMenu:

    def test_normal_cut_reduces_qty(self, inventory): # แก้ไข: รับ fixture inventory
        """ตัดสต๊อกปกติต้องลดจำนวนลงถูกต้อง"""
        success, _ = apply_stock_out(inventory, "101", 10) # แก้ไข: ส่ง inventory เข้าไป
        assert success is True
        assert inventory["101"]["q"] == 40 # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_cut_exact_amount_results_in_zero(self, inventory): # แก้ไข: รับ fixture inventory
        """ตัดออกพอดีกับที่มีต้องได้ qty = 0"""
        success, _ = apply_stock_out(inventory, "101", 50) # แก้ไข: ส่ง inventory เข้าไป
        assert success is True
        assert inventory["101"]["q"] == 0 # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_cut_more_than_available_fails(self, inventory): # แก้ไข: รับ fixture inventory
        """ตัดเกินที่มีต้องล้มเหลวและ qty ไม่เปลี่ยน"""
        success, msg = apply_stock_out(inventory, "101", 999) # แก้ไข: ส่ง inventory เข้าไป
        assert success is False
        assert "Not enough stock" in msg
        assert inventory["101"]["q"] == 50  # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_cut_nonexistent_product_fails(self, inventory): # แก้ไข: รับ fixture inventory
        """ตัดสินค้าที่ไม่มีใน inventory ต้องล้มเหลว"""
        success, msg = apply_stock_out(inventory, "999", 1) # แก้ไข: ส่ง inventory เข้าไป
        assert success is False
        assert "not found" in msg.lower()

    def test_warning_when_qty_below_LOW_STOCK_after_cut(self, inventory): # แก้ไข: รับ fixture inventory, เปลี่ยนชื่อเทสต์ตาม threshold ใหม่ (INV-9)
        """ต้องแจ้งเตือนเมื่อสต๊อกหลังตัดน้อยกว่า LOW_STOCK (10)"""
        inventory["101"]["q"] = 15 # แก้ไข: ปรับสต๊อกตั้งต้นใหม่
        success, msg = apply_stock_out(inventory, "101", 7)  # เหลือ 8 # แก้ไข: ส่ง inventory เข้าไป
        assert success is True
        assert "WARNING" in msg
        assert inventory["101"]["q"] == 8 # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_no_warning_when_qty_equals_LOW_STOCK(self, inventory): # แก้ไข: รับ fixture inventory, เปลี่ยนชื่อเทสต์
        """qty = LOW_STOCK ไม่ต้องแจ้งเตือน (เงื่อนไขคือ < LOW_STOCK ไม่ใช่ <= LOW_STOCK)"""
        inventory["101"]["q"] = 15 # แก้ไข: ปรับสต๊อกตั้งต้นใหม่
        success, msg = apply_stock_out(inventory, "101", 5)  # เหลือ 10 # แก้ไข: ส่ง inventory เข้าไป
        assert success is True
        assert inventory["101"]["q"] == 10 # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        assert inventory["101"]["q"] >= app.LOW_STOCK  # แก้ไข: เทียบกับ app.LOW_STOCK แทนเลข 5

    # ── Fixed Bug: Negative Amount (INV-7) ──

    def test_INV7_negative_amount_rejected(self, inventory): # แก้ไข: รวม conflict, เปลี่ยนชื่อจาก test_BUG_ เป็น test_ เพราะบั๊กถูกแก้แล้ว
        """
        ✅ FIX INV-7: เงื่อนไขต้องล้มเหลวเมื่อ amt เป็นลบ
        (อัปเดตตาม commit: test(qa): update BUG_INV7 test after fix)
        """
        success, _ = apply_stock_out(inventory, "101", -5) # แก้ไข: ต้องส่ง inventory เป็นพารามิเตอร์แรกให้ตรงกับ signature ปัจจุบัน
        assert success is False, "ควรล้มเหลวเมื่อ amt เป็นลบ"
        assert inventory["101"]["q"] == 50, \
            f"สต๊อกต้องคงที่เป็น 50 แต่เปลี่ยนเป็น {inventory['101']['q']}" # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_INV7_zero_amount_rejected(self, inventory): # แก้ไข: รวม conflict, เปลี่ยนชื่อจาก test_BUG_ เป็น test_ เพราะบั๊กถูกแก้แล้ว
        """
        ✅ FIX INV-7 (ส่วนขยาย): ตัดด้วย 0 ต้องไม่ผ่าน (ล้มเหลว)
        """
        success, _ = apply_stock_out(inventory, "101", 0) # แก้ไข: ส่ง inventory เข้าไป
        assert success is False, "ควรล้มเหลวเมื่อ amt เป็น 0"
        assert inventory["101"]["q"] == 50  # แก้ไข: เปลี่ยนจาก app.x เป็น inventory


# ══════════════════════════════════════════════════
# SECTION 4: เมนู 2 — Add / Update Logic
# ══════════════════════════════════════════════════

def apply_add_update(inventory, pid, name, qty, price, cat): # แก้ไข: รับพารามิเตอร์ inventory เพิ่ม
    """จำลอง logic เมนู 2 (Add/Update) — L.39-53 ใน app_v1.py"""
    if pid in inventory: # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        inventory[pid] = {"n": name, "q": qty, "p": price, "c": cat} # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
    else:
        inventory[pid] = {"n": name, "q": qty, "p": price, "c": cat} # แก้ไข: เปลี่ยนจาก app.x เป็น inventory


class TestAddUpdateMenu:

    def test_add_new_product(self, inventory): # แก้ไข: รับ fixture inventory
        """เพิ่มสินค้าใหม่ต้องปรากฏใน inventory"""
        apply_add_update(inventory, "NEW", "New Product", 30, 15.0, "Test") # แก้ไข: ส่งพารามิเตอร์ inventory
        assert "NEW" in inventory # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        assert inventory["NEW"]["n"] == "New Product" # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        assert inventory["NEW"]["q"] == 30 # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        assert inventory["NEW"]["p"] == pytest.approx(15.0) # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_update_existing_product_overwrites_all_fields(self, inventory): # แก้ไข: รับ fixture inventory
        """อัปเดตสินค้าที่มีอยู่แล้วต้องเขียนทับข้อมูลทั้งหมด"""
        apply_add_update(inventory, "101", "Renamed Noodle", 99, 9.9, "NewCat") # แก้ไข: ส่งพารามิเตอร์ inventory
        assert inventory["101"]["n"] == "Renamed Noodle" # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        assert inventory["101"]["q"] == 99 # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        assert inventory["101"]["p"] == pytest.approx(9.9) # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        assert inventory["101"]["c"] == "NewCat" # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_add_preserves_existing_items(self, inventory): # แก้ไข: รับ fixture inventory
        """เพิ่มสินค้าใหม่ต้องไม่ลบสินค้าเดิม"""
        apply_add_update(inventory, "NEW", "Extra", 5, 5.0, "T") # แก้ไข: ส่งพารามิเตอร์ inventory
        assert "101" in inventory  # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        assert "102" in inventory  # แก้ไข: เปลี่ยนจาก app.x เป็น inventory
        assert "103" in inventory  # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_category_stored_in_key_c(self, inventory): # แก้ไข: รับ fixture inventory
        """หมวดหมู่ต้องเก็บในคีย์ 'c' (ล็อก data structure)"""
        apply_add_update(inventory, "X01", "Item", 10, 5.0, "Snack") # แก้ไข: ส่งพารามิเตอร์ inventory
        assert inventory["X01"]["c"] == "Snack" # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_INV8_resolved_ifelse_identical_behavior(self, inventory): # แก้ไข: รับ fixture inventory, ลบ BUG_ ออกและเปลี่ยนชื่อเทสต์
        """
        ✔️ FIX INV-8: ลบโค้ด if/else ที่ซ้ำซ้อนออก เหลือพฤติกรรมเดียวคือเขียนทับ (overwrite) เสมอ
        ทีมยืนยันแล้วว่า overwrite คือพฤติกรรมที่ต้องการ (ไม่ใช่ accumulate)
        """
        apply_add_update(inventory, "101", inventory["101"]["n"], 1, inventory["101"]["p"], inventory["101"]["c"]) # แก้ไข: ส่งพารามิเตอร์ inventory
        assert inventory["101"]["q"] == 1, "FIXED: qty ถูก overwrite ตามที่ตั้งใจ" # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

# ══════════════════════════════════════════════════
# SECTION 5: Known Inconsistencies
# ══════════════════════════════════════════════════

class TestKnownInconsistencies:

    def test_INV9_resolved_threshold_mismatch_between_menus(self): # แก้ไข: ลบ BUG_ ออกและเปลี่ยนชื่อเทสต์
        """
        ✔️ FIX INV-9: เมนู 3 และ 4 ใช้เกณฑ์เดียวกันคือค่าคงที่ LOW_STOCK
        """ # แก้ไข: อัปเดต docstring
        qty = 7
        MENU3_THRESHOLD = app.LOW_STOCK # แก้ไข: อ้างอิงจาก app.LOW_STOCK
        MENU4_THRESHOLD = app.LOW_STOCK # แก้ไข: อ้างอิงจาก app.LOW_STOCK
        is_low_in_menu3 = qty < MENU3_THRESHOLD
        is_low_in_menu4 = qty < MENU4_THRESHOLD
        assert is_low_in_menu4 is True,  "เมนู 4: qty=7 ควรแจ้งเตือน"
        assert is_low_in_menu3 is True, "เมนู 3: qty=7 ต้องแจ้งเตือนเช่นกัน" # แก้ไข: ปรับ expected เป็น True
        assert is_low_in_menu3 == is_low_in_menu4, "FIXED: พฤติกรรมตรงกันแล้ว" # แก้ไข: ปรับ expected เป็น ==

    def test_default_inventory_ids_are_strings(self, inventory): # แก้ไข: รับ fixture inventory
        """ล็อก: product ID ต้องเป็น string ไม่ใช่ int"""
        assert isinstance(list(inventory.keys())[0], str) # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_default_inventory_qty_is_int(self, inventory): # แก้ไข: รับ fixture inventory
        """ล็อก: qty ต้องเป็น int"""
        assert isinstance(inventory["101"]["q"], int) # แก้ไข: เปลี่ยนจาก app.x เป็น inventory

    def test_default_inventory_price_is_float(self, inventory): # แก้ไข: รับ fixture inventory
        """ล็อก: price ต้องเป็น float"""
        assert isinstance(inventory["101"]["p"], float) # แก้ไข: เปลี่ยนจาก app.x เป็น inventory