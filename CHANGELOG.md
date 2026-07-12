# Changelog

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
