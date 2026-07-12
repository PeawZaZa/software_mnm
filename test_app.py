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