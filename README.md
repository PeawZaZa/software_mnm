# Inventory System v2.0.1-evolution

ระบบจัดการคลังสินค้าเบื้องต้น — พัฒนาต่อยอดจาก v1.0 โดยทีม ENGSE225

โค้ดแยกเป็นชั้นตามความรับผิดชอบ (`Product` → `InventoryRepository` → `InventoryService` → `ConsoleUI`)
พร้อม `CsvReportExporter` และ `Settings` — Class diagram ฉบับล่าสุดอยู่ใน
[คู่มือบทที่ 2](docs/System_Operations_and_Maintenance_Manual.md#บทที่-2--as-built-architecture) ·
ประวัติการออกแบบอยู่ใน [ARCHITECTURE.md](ARCHITECTURE.md)

เมนูทั้งหมด: 1 Show all · 2 Add/Update · 3 Out · 4 Inventory Summary · 5 Exit
· **6 Reorder List** (CR-01) · **7 Export CSV** (CR-02)

> 📊 **รายงานรายสัปดาห์** — [สัปดาห์ที่ 9–10](docs/Weekly_Presentation_W9-W10.md) ·
> [11](docs/week11/README.md) · [12](docs/week12/README.md) · [13](docs/week13/README.md) · [14](docs/week14/README.md) · [15](docs/week15/README.md)
>
> 📘 **คู่มือ:** [Operations & Maintenance Manual](docs/System_Operations_and_Maintenance_Manual.md) · [Maintenance Dossier](docs/Final_System_Maintenance_Dossier.md)

## ติดตั้งและรัน

```bash
git clone https://github.com/PeawZaZa/software_mnm.git
cd software_mnm
./setup.sh                 # Windows PowerShell: powershell -ExecutionPolicy Bypass -File setup.ps1
python app_v2.py           # (activate .venv ก่อน)
```

| ช่องทางอื่น | คำสั่ง |
|---|---|
| รันตรงไม่ติดตั้งอะไร | `python app_v2.py` — Python ≥ 3.10 ไม่มี dependency ภายนอก |
| Wheel | `pip install mini_inventory_system-2.0.1-py3-none-any.whl` → `mini-inventory` |
| Docker | `docker build -t mini-inventory:v2.0.1 .` → `docker run -it --rm -v inventory-data:/app/data mini-inventory:v2.0.1` |

ตั้งค่าผ่าน `.env` (คัดลอกจาก [`.env.example`](.env.example)): `INVENTORY_DB_PATH` · `REPORT_EXPORT_DIR`
ระบบสำรองไฟล์ข้อมูลเป็น `.bak` และกู้คืนเองเมื่อไฟล์เสีย — รายละเอียดใน [คู่มือบทที่ 5](docs/System_Operations_and_Maintenance_Manual.md#บทที่-5--operations--backup--recovery)

## วิธีรัน Tests และตรวจคุณภาพ

```bash
pip install -r requirements-dev.txt
pytest -m smoke -q                                 # 3 passed — ตรวจหลังติดตั้ง
pytest -v --cov=app_v2 --cov-report=term-missing   # 195 passed · coverage 99%
flake8 . --count --statistics                      # 0
bandit -r . -x ./test_app.py,./test_app_v2.py,./test_hardening.py,./test_deployment.py,./test_disaster_recovery.py
pip install pip-audit && pip-audit -r requirements.txt -r requirements-dev.txt   # 0 CVEs
python tools/run_uat.py                            # UAT 8/8 ผ่านหน้าจอ CLI จริง
```

| ไฟล์ | จำนวน | ครอบคลุม |
|---|---|---|
| `test_app.py` | 37 | regression suite ของ Sprint 1 (เรียก API ระดับโมดูล) |
| `test_app_v2.py` | 117 | คลาสทั้ง 5 + CR-01 + CR-02 + bug fixes + UAT-DEF-01 + integration |
| `test_hardening.py` | 19 | System Hardening สัปดาห์ที่ 11 + End-to-End flow |
| `test_deployment.py` | 13 | Smoke tests + การตั้งค่าผ่าน `.env` (สัปดาห์ที่ 13) |
| `test_disaster_recovery.py` | 9 | Auto-backup + กู้ข้อมูลอัตโนมัติ (สัปดาห์ที่ 14) |
| **รวม** | **195** | |

## โครงสร้างไฟล์

```
├── app_v1.py             # โค้ดต้นฉบับ v1.0.0 (อาจารย์ให้มา) — เก็บไว้เทียบ metrics ไม่ได้ใช้งาน
├── app_v2.py             # โค้ดหลัก (class-based)
├── test_app.py           # Unit Tests — regression suite ของ Sprint 1
├── test_app_v2.py        # Unit Tests — คลาสทั้ง 5 + integration
├── test_hardening.py     # Unit Tests — System Hardening สัปดาห์ที่ 11
├── test_deployment.py    # Smoke + config (สัปดาห์ที่ 13)
├── test_disaster_recovery.py  # Backup/recovery drills (สัปดาห์ที่ 14)
├── requirements.txt      # Runtime deps (ไม่มี — ใช้ standard library)
├── requirements-dev.txt  # เครื่องมือทดสอบ/สแกน
├── setup.sh · setup.ps1  # ติดตั้งด้วยคำสั่งเดียว
├── .env.example          # แม่แบบการตั้งค่า
├── pyproject.toml · MANIFEST.in   # สร้างแพ็กเกจ wheel / sdist
├── Dockerfile            # container image
├── pytest.ini · .flake8  # ตั้งค่าเครื่องมือ
├── tools/
│   ├── pm_metrics.py     # คำนวณ EVM · Reserve · ROI · กราฟ จาก docs/data/
│   └── run_uat.py        # รัน UAT ผ่านหน้าจอ CLI จริง
├── project_archives/     # OPAs — แม่แบบและสินทรัพย์กระบวนการสำหรับโครงการถัดไป
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
