# Clean Environment Installation Report
## ENGSE225 สัปดาห์ที่ 13 — Deployment Readiness & Verification · ชิ้นงานที่ 1, 2, 4

| | |
|---|---|
| มาตรฐาน | ISO/IEC/IEEE 12207:2017 Clause 6.4.9 — Software Installation Process |
| ผู้ทดสอบ | ตรัยรัตน์ วงษ์สิทธิ์ (QA) |
| วันที่ | 2026-10-05 |
| Commit ที่ติดตั้ง | `ab5d167` (สาขา `chore/week13-deployment-readiness`) |
| Log ดิบ | [`evidence/clean_install_log.txt`](evidence/clean_install_log.txt) · [`evidence/post_maintenance_test.log`](evidence/post_maintenance_test.log) · [`evidence/live_feature_check.txt`](evidence/live_feature_check.txt) |

---

## 1. ปัญหา "It Works on My Machine" ที่ตรวจพบก่อนทำงานสัปดาห์นี้

| ความเสี่ยงตามใบงาน | สถานะก่อนสัปดาห์ที่ 13 | หลังแก้ |
|---|---|---|
| Missing dependencies | ไม่มี `requirements.txt` · `pytest` ต้องรู้เองว่าต้องลง | `requirements.txt` (runtime: ไม่มี) + `requirements-dev.txt` |
| Hardcoded paths | ✅ ไม่มี absolute path ในโค้ด — ค้น `C:\` · `C:/` · `/Users/` · `/home/` ใน `app_v2.py` ไม่พบ | ใช้ `pathlib.Path` ทุกจุด |
| Missing configs | path ไฟล์ข้อมูลฝังในโค้ด (`db = "data.json"`) | `.env.example` + `Settings.from_env()` |
| ไม่มีขั้นตอนติดตั้งที่ทำซ้ำได้ | README บอกแค่ `pip install pytest` | `setup.sh` + `setup.ps1` คำสั่งเดียว |

## 2. Installation Planning

| Prerequisite | ค่า |
|---|---|
| Python | ≥ 3.10 (ใช้ syntax `Path \| None`) — สคริปต์ตรวจให้อัตโนมัติ |
| สิทธิ์ | เขียนไฟล์ในโฟลเดอร์โปรเจกต์ได้ |
| เครือข่าย | เฉพาะตอน `pip install` เครื่องมือทดสอบ |

**ขั้นตอนที่ทำซ้ำได้ (Reproducible)**

```bash
git clone https://github.com/PeawZaZa/software_mnm.git && cd software_mnm
./setup.sh                 # Windows PowerShell: powershell -ExecutionPolicy Bypass -File setup.ps1
```

| ไฟล์ใหม่ | หน้าที่ |
|---|---|
| [`setup.sh`](../../setup.sh) | macOS / Linux / Git Bash — ตรวจ Python → สร้าง `.venv` → ติดตั้ง → สร้าง `.env` → smoke test |
| [`setup.ps1`](../../setup.ps1) | ขั้นตอนเดียวกันสำหรับ Windows PowerShell |
| [`requirements.txt`](../../requirements.txt) | Runtime dependencies — **ว่าง** ตั้งใจใช้แค่ standard library |
| [`requirements-dev.txt`](../../requirements-dev.txt) | pytest · pytest-cov · flake8 · bandit |
| [`.env.example`](../../.env.example) | แม่แบบ `INVENTORY_DB_PATH` · `REPORT_EXPORT_DIR` |
| [`pytest.ini`](../../pytest.ini) | ลงทะเบียน marker `smoke` |
| [`.gitattributes`](../../.gitattributes) | บังคับ `*.sh` เป็น LF ไม่งั้น bash อ่าน `\r` ผิด |

## 3. Installation Verification — ผลจริง

### 3.1 สภาพแวดล้อมทดสอบ

| | |
|---|---|
| เครื่อง | Windows 11 · Git Bash · Python 3.13.7 |
| ความ "สะอาด" | `git clone` ลงโฟลเดอร์ว่าง — ไม่มี `.venv` · `.env` · `data.json` · ไม่ได้ใช้ไลบรารีที่ลงไว้ในเครื่องเดิม (venv ใหม่ติดตั้งทุกอย่างเอง) |
| ข้อจำกัด | ทดสอบบนเครื่องเดิมของทีม ไม่ใช่เครื่องใหม่จริง — **รอบสาธิตสัปดาห์ที่ 15 ต้องทำบนเครื่องอื่น** |

### 3.2 ผลการติดตั้ง

```
$ ./setup.sh
--- Starting Clean Environment Setup ---
[1/5] Python: Python 3.13.7
[2/5] Virtual environment: .venv
[3/5] Dependencies installed
[4/5] Created .env from .env.example
...                                                                      [100%]
3 passed, 183 deselected in 0.24s
[5/5] Smoke test passed
--- Installation Completed Successfully ---
exit code: 0

# elapsed: 25 seconds
```

| เกณฑ์ | ผล |
|---|---|
| ติดตั้งผ่านโดยไม่มี error | ✅ exit code 0 |
| Zero missing packages | ✅ `pip list` มีครบ 19 แพ็กเกจ ไม่มี warning |
| เวลาติดตั้ง ≤ 2 นาที (เกณฑ์สัปดาห์ที่ 15) | ✅ **25 วินาที** |
| Smoke test | ✅ 3/3 |

**ทดสอบซ้ำด้วย `setup.ps1` บน Windows PowerShell 5.1** (clone ใหม่อีกโฟลเดอร์) — ผ่านทั้ง 5 ขั้น
exit code 0 ใช้เวลา **19 วินาที** · log: [`evidence/clean_install_setup_ps1_log.txt`](evidence/clean_install_setup_ps1_log.txt)

### 3.3 ข้อบกพร่องที่พบจากการติดตั้งจริง — และแก้แล้ว

รอบแรก `setup.sh` **หยุดทันทีหลังพิมพ์บรรทัดแรก** โดยไม่มีข้อความ error

| | |
|---|---|
| สาเหตุ | บน Windows คำสั่ง `python3` เป็นทางลัดไป Microsoft Store — มีอยู่ใน PATH แต่รันไม่ได้ สคริปต์เลือกมันเพราะเช็กแค่ `command -v` |
| แก้ | วนหา interpreter ตัวแรกที่**รันได้จริง** (`python3` → `python` → `py`) และแจ้ง error ชัดเจนถ้าไม่เจอ — commit `ab5d167` |
| พบปัญหาเพิ่ม | executable bit ของ `setup.sh` หายระหว่าง commit (mode 100644) — คืนเป็น 100755 |

> นี่คือเหตุผลที่ต้องทดสอบติดตั้งบนสภาพแวดล้อมสะอาด — บนเครื่องผู้พัฒนาที่ใช้ `python` ตลอด ปัญหานี้ไม่เคยโผล่

## 4. Smoke Test vs Sanity Test

| ประเภท | เคส | คำถามที่ตอบ |
|---|---|---|
| 💨 Smoke | `test_system_boots_and_loads_database` | อ่านไฟล์ข้อมูลได้ไหม |
| 💨 Smoke | `test_main_menu_opens_and_exits` | `main()` จริงเปิดเมนูได้และออกได้ไหม |
| 🎯 Sanity | `test_new_features_work_after_install` | Barcode · Reorder alert · CSV ลงโฟลเดอร์ `exports/` ทำงานบนการติดตั้งใหม่ไหม |

```bash
pytest -m smoke -v       # 3 passed in 0.24s
```

## 5. Final Regression บนสภาพแวดล้อมใหม่ — `post_maintenance_test.log`

```
$ pytest -v --cov=app_v2 --cov-report=term-missing
...
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
app_v2.py     266      1    99%   447
-----------------------------------------
TOTAL         266      1    99%
============================= 186 passed in 2.09s =============================

STATUS: SUCCESS - NO REGRESSION DETECTED
```

ไฟล์เต็ม: [`evidence/post_maintenance_test.log`](evidence/post_maintenance_test.log) (ทุกเคสพร้อมสถานะ PASSED)

| ไฟล์เทสต์ | จำนวน |
|---|---:|
| `test_app.py` | 37 |
| `test_app_v2.py` | 117 |
| `test_hardening.py` | 19 |
| `test_deployment.py` (ใหม่) | 13 |
| **รวม** | **186** |

## 6. ทดสอบการทำงานสดบนการติดตั้งใหม่ (Workshop ขั้นที่ 4)

ใช้ `.env` ที่ `setup.sh` สร้างให้ (`data/inventory_db.json`, `exports/`)

| ขั้น | การกระทำ | ผลบนหน้าจอ |
|---|---|---|
| 1 | เพิ่ม Milk บาร์โค้ด `885123456789` สต๊อก 10 จุดสั่งซื้อ 5 | `Done.` |
| 2 | ตัดสต๊อก 6 | `Stock updated. !!! WARNING: ITEM IS RUNNING VERY LOW IN STOCK !!! !!! REORDER POINT REACHED: 4 left (reorder point 5) !!!` |
| 3 | เมนู 6 | `ID: P885 \| Name: Milk \| Stock: 4 \| Reorder Point: 5` |
| 4 | เมนู 7 พิมพ์แค่ `low_stock.csv` | `Exported 4 products to exports\low_stock.csv` |
| 5 | ตรวจไฟล์ | `data/inventory_db.json` ถูกสร้าง · CSV ขึ้นต้นด้วย BOM `ef bb bf` · แถว `P885,Milk,4,20.0,Dairy,885123456789,5` |

> ⬜ **ต้องทำเอง:** เปิด `exports/low_stock.csv` ใน Microsoft Excel แคปหน้าจอเก็บที่ `evidence/excel_low_stock.png`

## 7. ส่งต่อ Technical KPIs ให้ PM (ENGSE202)

| KPI | ค่าจริง |
|---|---|
| Code coverage | **99%** |
| Regression | **186/186 passed** — 0 regression |
| Clean deployment success | **1/1 ครั้ง** (หลังแก้ `setup.sh`) · 25 วินาที |
| Max cyclomatic complexity | **7** |
| Flake8 / Bandit | **0 / 0** |
