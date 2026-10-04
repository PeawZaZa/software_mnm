# Changelog

บันทึกการเปลี่ยนแปลงทั้งหมดของโครงการ — รูปแบบตาม [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
และเลขเวอร์ชันตาม [Semantic Versioning 2.0.0](https://semver.org/)

## [2.0.1-evolution] — 2026-10-05 · Deployment & Recoverability

Maintenance release หลัง Scope Freeze — **ไม่มีฟีเจอร์ใหม่ที่ผู้ใช้เห็น** เป็นงาน Adaptive (ติดตั้ง/ตั้งค่า)
และ Preventive (กู้ข้อมูล) ตามใบงานสัปดาห์ที่ 13–14 จึงขึ้นเฉพาะเลข PATCH

### Added
- `.env` / environment variables: `INVENTORY_DB_PATH`, `REPORT_EXPORT_DIR` (ไม่ตั้ง = ทำงานแบบ 2.0.0 ทุกประการ)
- พิมพ์แค่ชื่อไฟล์ในเมนู 7 → บันทึก CSV ลงโฟลเดอร์ `REPORT_EXPORT_DIR`
- สำรองไฟล์ข้อมูลอัตโนมัติเป็น `<ชื่อไฟล์>.bak` ก่อนบันทึกทุกครั้ง และกู้คืนอัตโนมัติเมื่อไฟล์หลักเสียหรือหาย
- `setup.sh` / `setup.ps1` ติดตั้งด้วยคำสั่งเดียว · `requirements.txt` · `.env.example`
- แพ็กเกจ `pyproject.toml` (wheel + sdist) พร้อมคำสั่ง `mini-inventory` · `Dockerfile`
- Smoke tests (`pytest -m smoke`) และ disaster-recovery tests — รวม **195 tests** coverage 99%

### Changed
- `ConsoleUI` รับ `input_fn`/`print_fn` ค่า default ตอนสร้าง object (ทดสอบ `main()` ได้)
- `requirements*.txt` เป็น ASCII ล้วน (pip-audit บน Windows อ่าน cp1252)

### Fixed
- Known issue KI-03: ไฟล์ข้อมูลเสียทั้งไฟล์แล้วการบันทึกครั้งถัดไปทับข้อมูลเดิม — กู้จาก `.bak` แทน
- `setup.sh` เลือก `python3` ที่เป็นทางลัด Microsoft Store บน Windows แล้วหยุดทำงานเงียบ ๆ
- `load_env_file()` complexity 9 → 5 (แยก `_parse_env_line()`)

### Security
- pip-audit: 0 CVEs (runtime 0 แพ็กเกจ · dev 17 แพ็กเกจ) · Bandit 0 issues · Docker image รันด้วยผู้ใช้ที่ไม่ใช่ root

## [2.0.0-evolution] — 2026-10-05 · Production Baseline

เวอร์ชันส่งมอบทางการ รวมทุกอย่างตั้งแต่ `v1.0.0-baseline` — Sprint 1 (v1.1) · Sprint 2 (v2.0) ·
CR-01/CR-02 (v2.1) · System Hardening สัปดาห์ที่ 11 · การแก้ข้อบกพร่องจาก UAT สัปดาห์ที่ 12

> **ทำไมเป็น 2.0.0 ทั้งที่เคยมีแท็ก `v2.1`** — แท็ก `v2.0` และ `v2.1` คือจุดบันทึกภายในระหว่างพัฒนา (pre-release)
> ที่ไม่ได้ผ่าน UAT `2.0.0-evolution` คือ**เวอร์ชันแรกที่ผ่าน UAT และถูกรวมเข้า `main`** ตามรูปแบบชื่อที่ใบงานกำหนด
> ขึ้นเลขหลัก (major) จาก 1 เป็น 2 เพราะเปลี่ยนสถาปัตยกรรมทั้งระบบและเพิ่ม data model ทางธุรกิจใหม่

### Added
- **CR-01** บาร์โค้ด (`barcode`) และจุดสั่งซื้อซ้ำรายชิ้น (`reorder_point`) ใน `Product`
- **CR-01** ค้นสินค้าด้วยบาร์โค้ด `find_by_barcode()` และเมนู **6. Reorder List**
- **CR-02** เมนู **7. Export CSV** — `utf-8-sig` ให้ Excel อ่านภาษาไทยได้ · `newline=""` กันบรรทัดว่างบน Windows
- **UAT-DEF-01** ข้อความ `REORDER POINT REACHED` ทันทีที่ตัดสต๊อกจนถึงจุดสั่งซื้อของสินค้าชิ้นนั้น
- ชุดทดสอบอัตโนมัติ **173 เคส** coverage **99%** (`test_app.py` · `test_app_v2.py` · `test_hardening.py`)
- CI ตรวจ flake8 · bandit · coverage ≥ 90% บน Python 3.10 และ 3.12 ทุก push/PR ไป `develop` และ `main`
- [`tools/run_uat.py`](tools/run_uat.py) รัน UAT 8 สถานการณ์ผ่านหน้าจอ CLI จริง

### Changed
- สถาปัตยกรรมแยกชั้น `Product` → `InventoryRepository` → `InventoryService` → `ConsoleUI` (+ `CsvReportExporter`)
- เมนู 4 เปลี่ยนชื่อจาก "Check Check" เป็น **Inventory Summary**
- การบันทึกไฟล์เป็น atomic เต็มรูปแบบ — `tempfile` ในโฟลเดอร์เดียวกัน + `fsync` + `os.replace()`
- `data.json` ถูกเขียนแบบ UTF-8 อ่านภาษาไทยได้ตรง ๆ และจัดย่อหน้า (key และโครงสร้างเดิม — อ่านไฟล์เก่าได้ทันที)
- เมนูใช้ตารางแทน if/elif 8 ชั้น (Cyclomatic Complexity ของ `run()` 9 → 5)

### Removed
- ตัวแปร global `x` ที่ถูกแก้ไขจากทุกฟังก์ชัน
- if/else ที่ทำงานเหมือนกันทั้งสองทางในเมนู Add/Update (INV-8)
- ข้อมูลตั้งต้นที่เขียนซ้ำ 2 ที่ใน `load()` — เหลือ `DEFAULT_DATA` ที่เดียว
- คอมเมนต์ประวัติการแก้ 111 จุดใน `test_app.py` (ประวัติอยู่ใน git แล้ว)

### Fixed
- **INV-5/6/7/9/10** ชื่อตัวแปรชนกัน · พิมพ์ตัวอักษรในช่องตัวเลขแล้วโปรแกรมตาย · ตัดสต๊อกติดลบได้ · เกณฑ์สต๊อกต่ำไม่ตรงกัน · ไฟล์เสียแล้วเปิดไม่ได้
- **DEF-01 (#20)** บาร์โค้ดซ้ำกันได้ · **DEF-02 (#21)** reorder point ติดลบถูกบันทึก · **DEF-03 (#22)** ข้อมูลเสียแถวเดียวทำให้ทั้งระบบเปิดไม่ได้
- ดิสก์เขียนไม่ได้แต่ระบบตอบ `Done.` — ตอนนี้แจ้ง error และย้อนข้อมูลในหน่วยความจำ (พบระหว่าง Hardening)
- `data.json` ที่เป็น JSON array ทำให้โปรแกรมตายตั้งแต่เปิด (พบระหว่าง Hardening)
- **UAT-DEF-01** ตัดสต๊อกสินค้าที่ reorder point สูงกว่า 10 แล้วไม่มีคำเตือน

### Security
- Bandit 0 issues · ไม่มี `eval`/`exec`/`pickle`/`subprocess` ในโค้ดโปรแกรม · ไฟล์ชั่วคราวใช้ชื่อที่คาดเดาไม่ได้

---

ประวัติรายรอบด้านล่างเก็บไว้ตามที่บันทึกระหว่างพัฒนา

## [v2.1] — CR-01 + CR-02 (Change Requests)

### Added
- **CR-01** `Product` เพิ่มฟิลด์ `barcode` และ `reorder_point` (มีค่า default จึงอ่าน `data.json` เดิมได้ทันที)
- **CR-01** `InventoryService.find_by_barcode()` — ค้นสินค้าจากบาร์โค้ด
- **CR-01** `InventoryService.get_reorder_list()` — รายการสินค้าที่ถึงจุดสั่งซื้อซ้ำ
  (เกณฑ์รายชิ้น แยกจาก `LOW_STOCK` ที่เป็นเกณฑ์รวมทั้งระบบ)
- **CR-01** เมนู **6. Reorder List**
- **CR-02** `CsvReportExporter` — ส่งออกรายงานสต๊อกเป็น CSV
  (`newline=""` กันบรรทัดว่างบน Windows · `utf-8-sig` ให้ Excel อ่านภาษาไทยได้)
- **CR-02** เมนู **7. Export CSV**

### Changed
- รูปแบบ `data.json` เพิ่ม key ย่อ `b` (barcode) และ `r` (reorder point)
  ไฟล์เก่าที่ไม่มี 2 key นี้ยังอ่านได้ ไม่ต้อง migrate

## [v2.0] — Sprint 2 (Class-Based Architecture)

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
- **SAM1-34** `validate()` ปฏิเสธ `qty` และ `price` ที่ติดลบตอนเพิ่ม/แก้ไขสินค้า (v1.1 ยังบันทึกได้)
- **SAM1-29 / 33 / 35 / 39 / 40** `test_app_v2.py` — 67 tests ครอบทั้ง 4 คลาส
  รวม integration test ที่รันครบตั้งแต่ UI ถึงไฟล์ (รวมทั้งโปรเจกต์ 104 tests)

### Compatibility
- `load(inventory)` / `save(inventory)` / `LOW_STOCK` ระดับโมดูลยังอยู่ในฐานะ wrapper
  ทำให้ `test_app.py` (regression suite ของ Sprint 1) ทั้ง 37 tests ยังผ่านโดยไม่ต้องแก้

---

## [v1.1] — Sprint 1

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
