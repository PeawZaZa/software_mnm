# Changelog

## [v2.1] — Sprint 2 (Class-Based Architecture)

### Changed
- **SAM1-28** เพิ่ม `Product` dataclass (`id`, `name`, `qty`, `price`, `category`) พร้อม `to_dict()` / `from_dict()`
  — รูปแบบไฟล์ `data.json` ยังเป็น key ย่อ `n/q/p/c` เหมือนเดิม ไม่ต้อง migrate ข้อมูล
- **SAM1-31** แยก `InventoryRepository` รับผิดชอบอ่าน/เขียนไฟล์อย่างเดียว
  และรวม default data ที่เคยเขียนซ้ำ 2 ที่ให้เหลือ `DEFAULT_DATA` ที่เดียว
- **SAM1-34** แยก `InventoryService` เก็บ business logic ทั้งหมด
  (`validate()`, `add_update()`, `stock_out()`, `get_summary()`)
- **SAM1-37** แยก `ConsoleUI` รับผิดชอบเมนูและ I/O — `main()` เหลือแค่ประกอบร่าง 3 คลาสเข้าด้วยกัน
- **SAM1-41** ปรับ `ARCHITECTURE.md` เป็นเวอร์ชัน class-based

### Added
- **SAM1-34** `validate()` ปฏิเสธ `qty` และ `price` ที่ติดลบตอนเพิ่ม/แก้ไขสินค้า (v2.0 ยังบันทึกได้)
- **SAM1-29 / 33 / 35 / 39 / 40** `test_app_v2.py` — 67 tests ครอบทั้ง 4 คลาส
  รวม integration test ที่รันครบตั้งแต่ UI ถึงไฟล์ (รวมทั้งโปรเจกต์ 104 tests)

### Compatibility
- `load(inventory)` / `save(inventory)` / `LOW_STOCK` ระดับโมดูลยังอยู่ในฐานะ wrapper
  ทำให้ `test_app.py` (regression suite ของ Sprint 1) ทั้ง 37 tests ยังผ่านโดยไม่ต้องแก้

---

## [v2.0] — Sprint 1

### Fixed
- **INV-4** ลบ `global x` ออก — ส่ง `inventory` เป็น parameter แทน
- **INV-5** เปลี่ยนชื่อตัวแปร `c` (qty) เป็น `qty` ป้องกันชนกับคีย์ `"c"` (category)
- **INV-6** เพิ่ม `try/except ValueError` สำหรับ Qty และ Price ทุกจุด
- **INV-7** เพิ่มเงื่อนไข `amt <= 0` — ปฏิเสธจำนวนที่เป็นลบหรือศูนย์
- **INV-8** ลบ `if/else` ที่ทำงานซ้ำซ้อน — เหลือพฤติกรรมเดียวคือเขียนทับ (overwrite)
- **INV-9** รวม threshold เป็นค่าคงที่ `LOW_STOCK = 10` ใช้ร่วมกันทั้งเมนู 3 และ 4
- **INV-10** เพิ่ม `try/except` สำหรับ `load()` — ถ้าไฟล์เสียหายโหลด default แทน
- **INV-11** เปลี่ยน `save()` เป็น atomic write ผ่าน `.tmp` file แล้ว `os.replace()`
- **INV-12** เปลี่ยนชื่อเมนู 4 จาก "Check Check" เป็น "Inventory Summary"

### Added
- **INV-13** Test Plan และ Test Cases ครอบคลุมทุกเมนู
- **INV-14** Unit Tests (`test_app.py`) — 37 tests ผ่านทั้งหมด
- **INV-15** System Architecture Document (`ARCHITECTURE.md`)
- **INV-16** Changelog และ README

---

## [v1.0] — Baseline (อาจารย์ให้มา)

- ระบบ CLI จัดการสินค้า 5 เมนู: Show All, Add/Update, Out, Check Check, Exit
- เก็บข้อมูลใน `data.json`
- พบจุดเสี่ยง 9 จุด (ดูรายละเอียดใน System Understanding Report)
