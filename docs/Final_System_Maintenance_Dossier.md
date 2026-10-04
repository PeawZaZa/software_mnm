# Final System Maintenance Dossier
## Mini Inventory System · `v1.0.0-baseline` → `v2.0.1-evolution` · ISO/IEC 14764

| | |
|---|---|
| เวอร์ชันเอกสาร | 1.0 — Pre-Audit (สัปดาห์ที่ 14) · ใช้เป็นฉบับส่งมอบ Final Defense (สัปดาห์ที่ 15) |
| มาตรฐาน | ISO/IEC 14764 (Maintenance) · ISO/IEC/IEEE 12207 (Transition) · ISO/IEC 25010 (Quality) |
| ผู้จัดทำ | พนาวุฒน์ อภิปสันติ (Tech Lead) · ตรัยรัตน์ วงษ์สิทธิ์ (QA) · ทวีชัย ทิใจ (Developer) · ปวริศ คูณศรี (PM) |
| วันที่ | 2026-10-05 |

**โครงสร้างแฟ้ม** — สัปดาห์ที่ 14 กำหนด 3 ภาค · สัปดาห์ที่ 15 กำหนด 7 หมวด เล่มนี้ครอบทั้งสองแบบ

| หมวด (สัปดาห์ที่ 15) | เนื้อหา | ภาค (สัปดาห์ที่ 14) |
|---|---|---|
| [1 Overview](#หมวดที่-1--overview) | ภาพรวมและหนี้เดิม | |
| [2 Architecture](#หมวดที่-2--architecture-as-is-vs-as-built) | As-Is vs As-Built + **Metrics Audit** | **ภาค 1 Metrics Audit** |
| [3 Surgery Logs](#หมวดที่-3--refactoring-surgery-logs) | ประวัติ Refactoring | |
| [4 Changes (CR)](#หมวดที่-4--change-requests) | CR-01 · CR-02 | |
| [5 Defect Logs](#หมวดที่-5--defect-logs--root-cause-analysis) | Defect + 5 Whys RCA | |
| [6 Verification](#หมวดที่-6--verification) | Tests · Coverage · Scans · Drills + **Traceability** | **ภาค 2 Traceability** |
| [7 Handover](#หมวดที่-7--handover) | คู่มือผู้ดูแลระบบ | **ภาค 3 Admin Manual** |

---

## หมวดที่ 1 · Overview

**System Scope** — โปรแกรม CLI จัดการคลังสินค้าร้านค้าขนาดเล็ก ผู้ใช้ทีละ 1 คน เก็บข้อมูลเป็นไฟล์ JSON
7 เมนู: แสดง · เพิ่ม/แก้ · ตัดสต๊อก · สรุป · ออก · รายการต้องสั่งซื้อ · ส่งออก CSV

**หนี้ทางเทคนิคตั้งต้น** (จาก [Architectural Detective](../architectural%20detective.md) สัปดาห์ที่ 1–4)

| หนี้ | ใน `app_v1.py` |
|---|---|
| Global mutable state | `x = {}` ถูกแก้ผ่าน `global x` |
| God function | `main()` 72 บรรทัด ทำทุกอย่าง — v(G) 14 |
| ไม่มีเทสต์ | 0 เคส |
| ไม่ทนข้อผิดพลาด | พิมพ์ตัวอักษรในช่องตัวเลข / ไฟล์เสีย → โปรแกรมตาย |
| บันทึกไม่ปลอดภัย | `open(db, 'w')` ล้างไฟล์ก่อนเขียน ไฟดับกลางทาง = ข้อมูลหาย |
| ตรรกะผิด | ตัดสต๊อกติดลบได้ · เกณฑ์สต๊อกต่ำ 2 เมนูไม่ตรงกัน · if/else ซ้ำซ้อน |

---

## หมวดที่ 2 · Architecture (As-Is vs As-Built)

### 2.1 เปรียบเทียบโครงสร้าง

| As-Is (v1.0.0) | As-Built (v2.0.1) |
|---|---|
| 3 ฟังก์ชัน: `load()` `save()` `main()` | 6 คลาส · 32 เมธอด · 5 ฟังก์ชันระดับโมดูล (`load`/`save` เป็น wrapper เข้ากันได้กับ Sprint 1) |
| ตรรกะ · I/O · หน้าจอ ปนกันใน `main()` | แยกชั้น `ConsoleUI` → `InventoryService` → `InventoryRepository` → `Product` + `CsvReportExporter` + `Settings` |
| ข้อมูลเป็น dict ดิบ key ตัวเดียว `n/q/p/c` | `Product` dataclass — key ไฟล์เดิมยังใช้ได้ |
| path ฝังในโค้ด | `.env` / environment variables |
| เขียนไฟล์ทับตรง ๆ | Atomic write (`tempfile` + `fsync` + `os.replace`) + Auto-backup `.bak` |

Class diagram และ data schema: [O&M Manual บทที่ 2](System_Operations_and_Maintenance_Manual.md#บทที่-2--as-built-architecture)

### 2.2 ภาค 1 — Metrics Audit (วัดจริงด้วยเครื่องมือ)

| Code Metric | As-Is v1.0.0 | Target | Actual v2.0.1 | เครื่องมือ | ISO 25010 |
|---|---:|---:|---:|---|---|
| Max Cyclomatic Complexity v(G) | **14** (`main`) | ≤ 8 | **7** (`stock_out`) | `radon cc` | Maintainability — Analysability 🟢 |
| ฟังก์ชันยาวสุด (บรรทัดโค้ด) | 58 | ≤ 20 | 20 | AST | Modifiability 🟢 |
| Nesting ลึกสุด | 5 | ≤ 3 | 3 | AST | Analysability 🟢 |
| Coupling Between Objects (CBO) | N/A (ไม่มีคลาส · ทุกอย่างผูกกับ `x`) | ≤ 4 | **2** (`ConsoleUI`, `InventoryService`) | นับด้วยมือ ข้อ 2.3 | Modularity 🟢 |
| Depth of Inheritance (DIT) | — | ≤ 2 | 1 (สืบทอดจาก `object` เท่านั้น) | นับด้วยมือ | Analysability 🟢 |
| Global mutable variables | **1** (`x`) + ค่าคงที่ 1 (`db`) | 0 | **0** (เหลือแต่ค่าคงที่) | อ่านโค้ด | Reliability 🟢 |
| Automated tests | 0 | — | **195** | pytest | Testability 🟢 |
| Test coverage | 0% | ≥ 90% | **99%** | pytest-cov | Testability 🏆 |
| Flake8 issues | — | 0 | 0 | flake8 | Analysability 🟢 |
| Bandit issues | — | 0 | 0 (837 LOC) | bandit | Security 🟢 |
| Dependency CVEs | ไม่มี manifest | 0 | **0** (runtime 0 แพ็กเกจ · dev 17 แพ็กเกจ) | pip-audit | Security 🟢 |
| Recoverability (RTO ไฟล์ข้อมูลเสีย) | crash | อัตโนมัติ | 0.15 วินาที · RPO 1 รายการ | drill | Reliability 🟢 |

> ตัวเลข As-Is ต่างจากตัวอย่างในใบงาน (v(G) 22 · coverage 15% · 3 CVEs) เพราะทีมใช้ค่าที่**วัดได้จริง**จากโค้ดของโครงการนี้

### 2.3 วิธีนับ CBO (Chidamber & Kemerer, 1994)

| คลาส | คลาสในโปรเจกต์ที่ใช้ | CBO |
|---|---|---:|
| `Product` | — | 0 |
| `Settings` | — | 0 |
| `InventoryRepository` | `Product` | 1 |
| `CsvReportExporter` | `Product` (อ่าน field) | 1 |
| `InventoryService` | `InventoryRepository` (inject) · `Product` | 2 |
| `ConsoleUI` | `InventoryService` (inject) · `CsvReportExporter` | 2 |

---

## หมวดที่ 3 · Refactoring Surgery Logs

### 3.1 ผ่าตัด `global x` (Sprint 1 · INV-4 · PR #3)

```python
# ก่อน — app_v1.py
x = {}
def load():
    global x            # ทุกฟังก์ชันแก้ x ได้ ไล่หาว่าใครเปลี่ยนค่าไม่ได้
    ...
def save():
    json.dump(x, f)     # อ่าน x จากที่ไหนก็ไม่รู้
```

```python
# หลัง Sprint 1 — ส่งข้อมูลเป็นพารามิเตอร์
def load(inventory): ...
def save(inventory): ...
```

```python
# หลัง Sprint 2 — ข้อมูลเป็นของ service, ไฟล์เป็นของ repository
class InventoryService:
    def __init__(self, repository):
        self.repository = repository
        self.inventory = repository.load()
```

**ตาข่ายนิรภัย** — `test_app.py` 37 เคสเขียนก่อนผ่าตัด และ `load()`/`save()` ระดับโมดูลถูกคงไว้เป็น wrapper
ทำให้ regression suite ไม่แดงเลยตลอดการรื้อทั้งไฟล์ใน Sprint 2

### 3.2 ลำดับการผ่าตัด

| ครั้ง | งาน | commit / PR | Tests หลังผ่าตัด |
|---|---|---|---:|
| 1 | แก้ 9 จุดเสี่ยง INV-4…12 | PR #2–#6 | 37 |
| 2 | `Product` dataclass | `dff022f` | — |
| 3 | `InventoryRepository` | `3571b87` | — |
| 4 | `InventoryService` | `1250324` | — |
| 5 | `ConsoleUI` + composition root | `529eaf0` · PR #23 | 104 |
| 6 | Code smells: Duplicate · Feature Envy · Long conditional · Dead comments | `44f6042` | 167 |
| 7 | Settings / `.env` | `15fd95a` | 186 |
| 8 | Auto-backup + แยก `_parse_env_line()` (v(G) 9 → 5) | สัปดาห์ที่ 14 | 195 |

---

## หมวดที่ 4 · Change Requests

| CR | คำขอ | Impact | Effort | อนุมัติ | เอกสาร |
|---|---|---|---|---|---|
| CR-01 | Barcode + Reorder Point | `Product` +2 field · `InventoryService` +2 method · เมนู 6 | 4 ชม. (ในแผน Sprint 2) | ตามแผนรายวิชา | [Weekly W9–10 ข้อ 2.3](Weekly_Presentation_W9-W10.md#23-cr-01--barcode-และ-reorder-point) |
| CR-02 | Export CSV | คลาสใหม่ `CsvReportExporter` · เมนู 7 · **ไม่แตะ business logic** | 4.5 ชม. (กันชน) | CCB 2026-09-07 | [CR-02 Form](CR-02_Impact_and_Decision_Form.md) · [CCB Minutes](CCB_Meeting_Minutes.md) |
| FB-01…04 | คำขอหลัง Scope Freeze | — | — | ส่งเข้า Future Backlog v3.0 | [Scope Freeze ข้อ 5](week11/Scope_Freeze_Agreement.md#5-future-backlog-v30--คำขอที่รับทราบแต่ไม่ทำในโครงการนี้) |

---

## หมวดที่ 5 · Defect Logs & Root Cause Analysis

| ID | ข้อบกพร่อง | ความรุนแรง | พบโดย | สถานะ |
|---|---|---|---|---|
| DEF-01 (#20) | บาร์โค้ดซ้ำได้ | Medium | Bug bashing | ✅ `8cb3e25` |
| DEF-02 (#21) | Reorder point ติดลบถูกบันทึก | Medium | Bug bashing | ✅ `8cb3e25` |
| DEF-03 (#22) | ข้อมูลเสียแถวเดียว → เปิดโปรแกรมไม่ได้ | **High** | Bug bashing | ✅ `8cb3e25` |
| DEF-04 | ฟิลด์ที่หายถูกเติม default เงียบ ๆ | Low | Bug bashing | 📌 รับทราบ (KI-04) |
| HARD-01 | ดิสก์เขียนไม่ได้แต่ตอบ `Done.` | High | Hardening W11 | ✅ `44f6042` |
| HARD-02 | `data.json` เป็น array → crash | Medium | Hardening W11 | ✅ `44f6042` |
| UAT-DEF-01 | ขายถึงจุดสั่งซื้อแล้วไม่เตือน | Medium | UAT W12 | ✅ `3746f1b` |
| INST-01 | `setup.sh` เลือก `python3` stub บน Windows | Medium | Clean install W13 | ✅ `ab5d167` |
| INST-02 | pip-audit อ่าน requirements ที่มีภาษาไทยไม่ได้ (cp1252) | Low | Dependency audit W14 | ✅ สัปดาห์ที่ 14 |
| REL-01 | `main` ปัจจุบันรันเทสต์ของตัวเองไม่ผ่าน 24 เคส | **High** | Rollback drill W14 | 🔧 แก้เมื่อ merge release เข้า `main` |

**5 Whys** ของ DEF-03: [Maintenance Summary ข้อ 4](week12/Maintenance_Summary_Report_ISO14764.md#4-การวิเคราะห์สาเหตุราก-rca-ของข้อบกพร่องที่รุนแรงที่สุด--def-03)

### 5 Whys — REL-01 (`main` เสีย)

| # | ทำไม | คำตอบ |
|---|---|---|
| 1 | ทำไม `main` รันเทสต์ไม่ผ่าน | `test_app.py` เรียก `load(inv)` แต่ `app_v2.py` บน `main` มี `load()` ที่ไม่รับพารามิเตอร์ |
| 2 | ทำไมสองไฟล์ไม่ตรงกัน | PR #14 merge เทสต์เวอร์ชันใหม่เข้า `main` แล้ว PR #15 revert แค่บางส่วน |
| 3 | ทำไม merge เทสต์ที่ไม่ผ่านเข้า `main` ได้ | ไม่มี Branch Protection และ CI ไม่ทำงาน |
| 4 | ทำไมไม่มีใครเห็นตลอด 2 เดือน | ทีมทำงานบน `develop` อย่างเดียว ไม่มีใครรันเทสต์บน `main` อีกเลย |
| 5 | ทำไมไม่มีการตรวจ | ไม่มีขั้นตอนตรวจสุขภาพสาขา release เป็นระยะ |

**แก้** — release `v2.0.0-evolution` เข้า `main` จะแทนที่โค้ดชุดนี้ทั้งหมด (195 tests ผ่าน)
**ป้องกัน** — Branch Protection + Required status check บน `main` · Rollback ต้องไปที่แท็กที่ผ่านเทสต์เท่านั้น

---

## หมวดที่ 6 · Verification

### 6.1 สรุปผลการทดสอบ

| ชุดทดสอบ | เคส | ครอบคลุม |
|---|---:|---|
| `test_app.py` | 37 | Regression Sprint 1 |
| `test_app_v2.py` | 117 | 5 คลาส · CR-01 · CR-02 · DEF-01/02/03 · UAT-DEF-01 |
| `test_hardening.py` | 19 | Code smells · Atomic I/O · E2E |
| `test_deployment.py` | 13 | Smoke (3) · `.env` · Settings |
| `test_disaster_recovery.py` | 9 | Auto-backup · Fallback · Drill |
| **รวม** | **195** | coverage **99%** |

| การตรวจ | ผล | หลักฐาน |
|---|---|---|
| flake8 | 0 | [week11/evidence](week11/evidence/) |
| bandit | 0 issues | [week11/evidence](week11/evidence/) |
| pip-audit | 0 CVEs / 17 packages | [week14/evidence/pip_audit_report.txt](week14/evidence/pip_audit_report.txt) |
| UAT | 8/8 (รอบซ้อม) | [week12/evidence](week12/evidence/) |
| Clean install | 25 วิ (bash) · 19 วิ (PowerShell) | [week13/evidence](week13/evidence/) |
| post_maintenance_test.log | 186/186 · 0 regression | [week13/evidence/post_maintenance_test.log](week13/evidence/post_maintenance_test.log) |
| Data corruption drill | กู้ใน 0.15 วิ · RPO 1 รายการ | [week14/evidence/data_corruption_drill.txt](week14/evidence/data_corruption_drill.txt) |
| Git rollback drill | RTO 1.4 วิ · ประวัติไม่หาย | [week14/evidence/git_rollback_drill.txt](week14/evidence/git_rollback_drill.txt) |

### 6.2 ภาค 2 — Bidirectional Traceability Matrix

| ข้อกำหนด | WBS / Jira | โค้ด | Commit | Unit tests | UAT |
|---|---|---|---|---|---|
| **CR-01** Barcode & Reorder Point | SAM1-44 | `Product.barcode` · `reorder_point` · `needs_reorder()` · `InventoryService.find_by_barcode()` · `get_reorder_list()` · `ConsoleUI.handle_reorder()` | `74367ea` (PR #24) | `TestProductBarcodeAndReorderPoint` · `TestServiceFindByBarcode` · `TestServiceReorderList` · `TestConsoleUIReorderList` | UAT-SC01 |
| **CR-02** CSV Export | SAM1-45 | `CsvReportExporter.export()` · `ConsoleUI.handle_export()` | `4169f2c` (PR #25) | `TestCsvReportExporter` · `TestConsoleUIExportCsv` | UAT-SC03 · EC03 |
| **DEF-01** บาร์โค้ดซ้ำ | SAM1-47 · #20 | `InventoryService._barcode_owner()` | `8cb3e25` | `TestDef01DuplicateBarcode` | — |
| **DEF-02** reorder ติดลบ | SAM1-48 · #21 | `InventoryService.validate()` | `8cb3e25` | `TestDef02NegativeReorderPoint` | UAT-EC02 |
| **DEF-03** แถวเสีย | SAM1-46 · #22 | `InventoryRepository.load()` | `8cb3e25` | `TestDef03CorruptRowDoesNotKillTheApp` | — |
| **HARD-01/02** | S3-04 | `InventoryRepository.save()` · `_read_json_object()` | `44f6042` | `TestServiceDoesNotLieAboutSaving` · `TestLoadRejectsWrongShape` | — |
| **UAT-DEF-01** | S3-07 | `InventoryService.stock_out()` | `3746f1b` | `TestUatDef01ReorderAlertOnStockOut` | UAT-SC02-B |
| **Config externalization** | สัปดาห์ที่ 13 | `load_env_file()` · `Settings` · `ConsoleUI.export_path()` | `15fd95a` | `TestLoadEnvFile` · `TestSettings` · `TestExportPath` | Smoke |
| **Recoverability** (KI-03) | สัปดาห์ที่ 14 | `InventoryRepository.backup_path` · `_load_raw()` · `save()` | สัปดาห์ที่ 14 | `test_disaster_recovery.py` (9) | Data drill |

> ใบงานยกตัวอย่าง `BUG-101 (Legacy JSON)` — ในโครงการนี้ไฟล์ JSON เก่าที่ไม่มี key `b`/`r` **อ่านได้ตั้งแต่แรก**
> เพราะ `from_dict()` มีค่า default (ทดสอบโดย `TestProductFromDict`) จึงไม่เคยเกิดบั๊กนี้ ทีมไม่สร้างรายการขึ้นมาเพื่อให้ตรงตัวอย่าง

---

## หมวดที่ 7 · Handover

### 7.1 ภาค 3 — Admin Manual

คู่มือผู้ดูแลระบบฉบับเต็ม: **[System Operations & Maintenance Manual](System_Operations_and_Maintenance_Manual.md)**

| หัวข้อในใบงาน | อยู่ที่ |
|---|---|
| Architecture topology | บทที่ 2 |
| ติดตั้ง (script · wheel · docker) | บทที่ 3 |
| Emergency SOP — restart · กู้ไฟล์สำรอง · rollback | บทที่ 5.3 · 7.1 · 7.2 |
| Database migration guide | บทที่ 7.3 |
| Escalation path | บทที่ 7.4 |
| Known issues | บทที่ 6.2 |

### 7.2 Distribution Package

| ไฟล์ | SHA-256 |
|---|---|
| [`mini_inventory_system-2.0.1-py3-none-any.whl`](week14/artifacts/) | ดู [`SHA256SUMS.txt`](week14/artifacts/SHA256SUMS.txt) |
| [`mini_inventory_system-2.0.1.tar.gz`](week14/artifacts/) | ดู [`SHA256SUMS.txt`](week14/artifacts/SHA256SUMS.txt) |
| [`Dockerfile`](../Dockerfile) | build ยังไม่ได้ทดสอบ — เครื่องทีมไม่มี Docker |

### 7.3 Standalone Test

เกณฑ์รับมอบ: วิศวกรคนใหม่อ่านเล่มนี้ + O&M Manual แล้วติดตั้ง รันเทสต์ และกู้ข้อมูลได้เองโดยไม่ต้องถามทีมเดิม
**ทดสอบโดย:** ______________________ (ผู้ที่ไม่ใช่สมาชิกทีม) **ผล:** ☐ ผ่าน ☐ ไม่ผ่าน — หมายเหตุ: ______________

---

## การรับรอง Pre-Audit (สัปดาห์ที่ 14)

- [x] ตาราง Code Metrics (As-Is vs To-Be) มีข้อมูลประจักษ์ครบ — หมวด 2.2
- [x] Traceability Matrix เชื่อมโยงครบทุก CR และบั๊ก — หมวด 6.2
- [x] รายงาน pip-audit และผลซ้อม Rollback สมบูรณ์ — [DR & Security Report](week14/DR_and_Dependency_Security_Report.md)

| บทบาท | ชื่อ | ลายมือชื่อ | วันที่ |
|---|---|---|---|
| อาจารย์ผู้ตรวจ (Pre-Audit) | | | |
| Tech Lead | พนาวุฒน์ อภิปสันติ | | |
