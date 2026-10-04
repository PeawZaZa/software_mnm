# Inventory System v2.0.0-evolution

ระบบจัดการคลังสินค้าเบื้องต้น — พัฒนาต่อยอดจาก v1.0 โดยทีม ENGSE225

ตั้งแต่ v2.0 โค้ดถูกแยกเป็น 4 คลาสตามชั้นความรับผิดชอบ
(`Product` → `InventoryRepository` → `InventoryService` → `ConsoleUI`)
รายละเอียดอยู่ใน [ARCHITECTURE.md](ARCHITECTURE.md)

เมนูทั้งหมด: 1 Show all · 2 Add/Update · 3 Out · 4 Inventory Summary · 5 Exit
· **6 Reorder List** (CR-01) · **7 Export CSV** (CR-02)

> 📊 **รายงานรายสัปดาห์** — [สัปดาห์ที่ 9–10](docs/Weekly_Presentation_W9-W10.md) ·
> [11](docs/week11/README.md) · [12](docs/week12/README.md)

## วิธีรัน

```bash
python app_v2.py
```

## วิธีรัน Tests และตรวจคุณภาพ

```bash
pip install -r requirements-dev.txt
pytest -v --cov=app_v2 --cov-report=term-missing   # 173 passed · coverage 99%
flake8 . --count --statistics                      # 0
bandit -r . -x ./test_app.py,./test_app_v2.py,./test_hardening.py
python tools/run_uat.py                            # UAT 8/8 ผ่านหน้าจอ CLI จริง
```

| ไฟล์ | จำนวน | ครอบคลุม |
|---|---|---|
| `test_app.py` | 37 | regression suite ของ Sprint 1 (เรียก API ระดับโมดูล) |
| `test_app_v2.py` | 117 | คลาสทั้ง 5 + CR-01 + CR-02 + bug fixes + UAT-DEF-01 + integration |
| `test_hardening.py` | 19 | System Hardening สัปดาห์ที่ 11 + End-to-End flow |
| **รวม** | **173** | |

## โครงสร้างไฟล์

```
├── app_v1.py             # โค้ดต้นฉบับ v1.0.0 (อาจารย์ให้มา) — เก็บไว้เทียบ metrics ไม่ได้ใช้งาน
├── app_v2.py             # โค้ดหลัก (class-based)
├── test_app.py           # Unit Tests — regression suite ของ Sprint 1
├── test_app_v2.py        # Unit Tests — คลาสทั้ง 5 + integration
├── test_hardening.py     # Unit Tests — System Hardening สัปดาห์ที่ 11
├── requirements-dev.txt  # เครื่องมือทดสอบ/สแกน (ตัวโปรแกรมใช้แค่ standard library)
├── .flake8               # เกณฑ์ PEP 8 ของทีม
├── tools/
│   ├── pm_metrics.py     # คำนวณ EVM · Reserve · ROI · กราฟ จาก docs/data/
│   └── run_uat.py        # รัน UAT ผ่านหน้าจอ CLI จริง
├── ARCHITECTURE.md       # เอกสารสถาปัตยกรรมระบบ
├── CHANGELOG.md          # ประวัติการเปลี่ยนแปลง (Keep a Changelog)
├── docs/                 # เอกสาร ENGSE202/225 แยกตามสัปดาห์ (week11/, week12/, ...)
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
