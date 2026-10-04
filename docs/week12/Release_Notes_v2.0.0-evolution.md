# Mini Inventory System v2.0.0-evolution

**Production baseline** ฉบับแรกที่ผ่าน UAT — ปรับปรุงจากโค้ดต้นฉบับ `v1.0.0-baseline` ตลอด 3 Sprints

## ไฮไลต์

- 🏗️ **สถาปัตยกรรมใหม่** — แยกเป็น `Product` · `InventoryRepository` · `InventoryService` · `ConsoleUI` · `CsvReportExporter` ไม่มี global state
- 🏷️ **Barcode & Reorder Point (CR-01)** — ค้นสินค้าด้วยบาร์โค้ด · ตั้งจุดสั่งซื้อรายชิ้น · เมนู 6 Reorder List · เตือนทันทีตอนขายเมื่อถึงจุดสั่งซื้อ
- 📄 **CSV Export (CR-02)** — เมนู 7 ส่งออกรายงานที่เปิดใน Excel ได้ ภาษาไทยไม่เพี้ยน
- 🛡️ **ทนทาน** — บันทึกไฟล์แบบ atomic · ไฟล์ข้อมูลเสียทั้งไฟล์หรือรายแถวก็ยังเปิดโปรแกรมได้ · ไม่บอกว่าสำเร็จถ้าบันทึกไม่ได้

## คุณภาพ

| | v1.0.0-baseline | v2.0.0-evolution |
|---|---:|---:|
| Automated tests | 0 | **173** |
| Coverage | — | **99%** |
| Max Cyclomatic Complexity | 14 (`main`) | **7** |
| Global mutable variables | 1 (`x`) | **0** |
| Flake8 issues | — | **0** |
| Bandit issues | — | **0** |
| UAT | — | **8 / 8** |

## วิธีติดตั้ง

```bash
git clone https://github.com/PeawZaZa/software_mnm.git
cd software_mnm
git checkout v2.0.0-evolution
python app_v2.py        # Python ≥ 3.10 ไม่ต้องติดตั้งไลบรารีเพิ่ม
```

## ความเข้ากันได้

- อ่าน `data.json` จาก v1.x ได้ทันที ไม่ต้อง migrate (สินค้าเดิมจะมี barcode ว่าง และ reorder point = 0)
- ไฟล์ที่บันทึกโดย v2.0.0 ยังใช้ key ย่อเดิม `n/q/p/c` + `b/r`

## ข้อจำกัดที่ทราบ

- ใช้งานได้ทีละ 1 คน (CLI + ไฟล์ JSON) ยังไม่รองรับหลายคนพร้อมกัน
- CSV ส่งออกสินค้าทั้งหมด — ส่งออกเฉพาะสต๊อกต่ำอยู่ใน Future Backlog v3.0
- DEF-04 (Low): ถ้า `data.json` ถูกแก้ด้วยมือจนฟิลด์หายไป ระบบเติมค่า default ให้โดยไม่เตือน

รายละเอียดทั้งหมดดูใน [CHANGELOG.md](../../CHANGELOG.md#200-evolution--2026-10-05--production-baseline)
