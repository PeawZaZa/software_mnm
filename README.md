# Inventory System v2.1

ระบบจัดการคลังสินค้าเบื้องต้น — พัฒนาต่อยอดจาก v1.0 โดยทีม ENGSE225

ตั้งแต่ v2.0 โค้ดถูกแยกเป็น 4 คลาสตามชั้นความรับผิดชอบ
(`Product` → `InventoryRepository` → `InventoryService` → `ConsoleUI`)
รายละเอียดอยู่ใน [ARCHITECTURE.md](ARCHITECTURE.md)

เมนูทั้งหมด: 1 Show all · 2 Add/Update · 3 Out · 4 Inventory Summary · 5 Exit
· **6 Reorder List** (CR-01) · **7 Export CSV** (CR-02)

> 📊 **[รายงานนำเสนอผลงานสัปดาห์ที่ 9–10](docs/Weekly_Presentation_W9-W10.md)** — สรุปงานทั้งหมดพร้อมลิงก์ไปเอกสารประกอบทุกฉบับ

## วิธีรัน

```bash
python app_v2.py
```

## วิธีรัน Tests

```bash
pytest -v
```

| ไฟล์ | จำนวน | ครอบคลุม |
|---|---|---|
| `test_app.py` | 37 | regression suite ของ Sprint 1 (เรียก API ระดับโมดูล) |
| `test_app_v2.py` | 98 | คลาสทั้ง 4 + CR-01 + CR-02 + integration test |
| **รวม** | **135** | |

## โครงสร้างไฟล์

```
├── app_v1.py          # โค้ดต้นฉบับ (อาจารย์ให้มา) — เก็บไว้อ้างอิง ไม่ได้ใช้งานแล้ว
├── app_v2.py          # โค้ดหลัก (class-based ตั้งแต่ v2.0)
├── test_app.py        # Unit Tests — regression suite ของ Sprint 1
├── test_app_v2.py     # Unit Tests — คลาสทั้ง 4 + integration
├── ARCHITECTURE.md    # เอกสารสถาปัตยกรรมระบบ
├── CHANGELOG.md       # ประวัติการเปลี่ยนแปลง
├── docs/              # เอกสารบริหารโครงการ (ENGSE202) + รายงานนำเสนอสัปดาห์ที่ 9–10
├── .gitignore
└── README.md
```

> `data.json` ถูก gitignore ไว้ — โปรแกรมจะสร้างข้อมูลตั้งต้น 3 รายการให้เองเมื่อยังไม่มีไฟล์

## สมาชิกทีม

| # | ชื่อ | ตำแหน่ง |
|---|---|---|
| 1 | ปวริศ คูณศรี | Project Manager |
| 2 | พนาวุฒน์ อภิปสันติ| Tech Lead |
| 3 | ตรัยรัตน์ วงษ์สิทธิ์ | QA / Tester |
| 4 | ทวีชัย ทิใจ | Developer |

## Requirements

- Python ≥ 3.10
- pytest ≥ 7.0

```bash
pip install pytest
```
