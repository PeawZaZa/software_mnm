# Disaster Recovery & Dependency Security Report
## ENGSE225 สัปดาห์ที่ 14 — Packaging, Disaster Recovery & Audit · ชิ้นงานที่ 1 และ 3

| | |
|---|---|
| มาตรฐาน | ISO/IEC/IEEE 12207 6.4.10 (Transition) · ISO/IEC 25010 (Reliability — Recoverability · Security) |
| ผู้จัดทำ | ทวีชัย ทิใจ (Developer) · ตรัยรัตน์ วงษ์สิทธิ์ (QA) · ตรวจทาน พนาวุฒน์ อภิปสันติ (Tech Lead) |
| วันที่ | 2026-10-05 |
| หลักฐานดิบ | [`evidence/`](evidence/) |

---

## 1. สรุป

| ด่านตรวจ | ผล |
|---|---|
| Package distribution (sdist + wheel) | ✅ build ผ่าน · ติดตั้ง wheel ใน venv เปล่าแล้วคำสั่ง `mini-inventory` ทำงาน |
| Docker image | ⚠️ เขียน `Dockerfile` แล้ว **ยังไม่ได้ build** — เครื่องทีมไม่มี Docker |
| pip-audit | ✅ **0 CVEs** ใน 17 แพ็กเกจ · runtime dependency 0 แพ็กเกจ |
| Data corruption drill | ✅ กู้จาก `.bak` อัตโนมัติ 0.15 วินาที · RPO 1 รายการ |
| Git rollback drill | ✅ RTO 1.4 วินาที · ประวัติไม่หาย — **พบว่า `main` ปัจจุบันเสีย (REL-01)** |
| ข้อบกพร่องที่พบจากการตรวจสัปดาห์นี้ | 2 รายการ (INST-02 · REL-01) + 1 ข้อผิดพลาดในรายงานสัปดาห์ที่ 13 |

---

## 2. Package Distribution

### 2.1 `pyproject.toml`

| ฟิลด์ | ค่า |
|---|---|
| name / version | `mini-inventory-system` / `2.0.1` |
| requires-python | `>=3.10` |
| dependencies | `[]` — ไม่มี runtime dependency |
| optional `dev` | pytest · pytest-cov · flake8 · bandit |
| console script | `mini-inventory = app_v2:main` |

`MANIFEST.in` สั่งให้ `.tar.gz` มีเทสต์ทั้ง 5 ไฟล์ · requirements · `setup.sh`/`setup.ps1` · `Dockerfile`
เพื่อให้ผู้รับ source distribution ตรวจซ้ำได้ด้วยตัวเอง

### 2.2 ผล build และทดสอบติดตั้ง

```
$ python -m build
Successfully built mini_inventory_system-2.0.1.tar.gz and mini_inventory_system-2.0.1-py3-none-any.whl

$ python -m venv venv && source venv/Scripts/activate
$ pip install mini_inventory_system-2.0.1-py3-none-any.whl
$ printf '4\n5\n' | mini-inventory
=== INVENTORY SYSTEM v2.0 ===
Total product types: 3
Total inventory value: 1540.0 THB
Bye
```

| ไฟล์ | ขนาด | SHA-256 |
|---|---:|---|
| `mini_inventory_system-2.0.1-py3-none-any.whl` | ~11 KB | `2d2a36b4…b1b5b8` |
| `mini_inventory_system-2.0.1.tar.gz` | ~36 KB (รวมเทสต์และสคริปต์ติดตั้ง) | `72720b5d…fbb13` |

ไฟล์และ checksum เต็ม: [`artifacts/`](artifacts/) · `dist/` ถูก gitignore จึงเก็บสำเนาส่งงานไว้ที่นี่

### 2.3 Docker

[`Dockerfile`](../../Dockerfile) ใช้ `python:3.12-slim` · ติดตั้ง requirements ก่อนคัดลอกโค้ด (cache ชั้น dependencies)
· รันด้วยผู้ใช้ `appuser` ไม่ใช่ root · แยก `/app/data` และ `/app/exports` เป็น volume

```bash
docker build -t mini-inventory:v2.0.1 .
docker run -it --rm -v inventory-data:/app/data mini-inventory:v2.0.1
```

> ⚠️ **ยังไม่ได้ทดสอบจริง** — `docker: command not found` บนเครื่องที่ใช้ทำงาน
> ⬜ ต้องให้สมาชิกที่มี Docker Desktop build และรันคำสั่งข้างบน แล้วแคปหน้าจอเก็บที่ `evidence/docker_run.png`

---

## 3. Dependency Audit — pip-audit

### 3.1 ผล

```
$ pip-audit -r requirements.txt -r requirements-dev.txt
No known vulnerabilities found
```

| | |
|---|---|
| Runtime dependencies | **0** — โปรแกรมใช้แค่ standard library |
| Dev/CI dependencies ที่ถูก resolve และตรวจ | 17 แพ็กเกจ (bandit 1.9.4 · flake8 7.4.1 · pytest 9.1.1 · pytest-cov 7.1.0 · PyYAML 6.0.3 · rich 15.0.0 · …) |
| CVE ที่พบ | **0** |
| รายงาน JSON | [`evidence/security_report.json`](evidence/security_report.json) |

> ตัวอย่างในใบงานมีการอัปเกรดแพ็กเกจที่มี CVE — ในโครงการนี้**ไม่พบ CVE จึงไม่มีอะไรต้องอัปเกรด**
> การตัดสินใจไม่ใช้ไลบรารีภายนอกในตัวโปรแกรมตั้งแต่ต้นทำให้พื้นผิวการโจมตีจาก supply chain เป็นศูนย์

### 3.2 ⚠️ ข้อบกพร่องที่พบ — INST-02: pip-audit อ่าน requirements ไม่ได้

```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 43
decoding with 'cp1252' codec failed
```

| | |
|---|---|
| สาเหตุ | `requirements*.txt` มีคอมเมนต์ภาษาไทย — pip-audit บน Windows อ่านไฟล์ด้วย code page ของระบบ (cp1252) ไม่ใช่ UTF-8 |
| ทำไมไม่เคยเจอ | `pip install -r` อ่าน UTF-8 ได้ จึงผ่านทั้ง `setup.sh` และ `setup.ps1` |
| แก้ | เขียนคอมเมนต์ใน `requirements*.txt` เป็นภาษาอังกฤษ ASCII ล้วน และบันทึกกติกานี้ไว้ในไฟล์ |

---

## 4. Disaster Recovery

### 4.1 กลไกใหม่ — Rolling Auto-Backup & Automated Fallback

| กลไก | การทำงาน |
|---|---|
| **Rolling backup** | ก่อน `os.replace()` ทุกครั้ง คัดลอกไฟล์เดิมเป็น `<ชื่อไฟล์>.bak` — **ข้ามถ้าไฟล์เดิมเสีย** เพื่อไม่ให้ไฟล์เสียทับสำเนาที่ดี |
| **Fallback ตอนเปิด** | ไฟล์หลักเสีย*หรือ*ถูกลบ → โหลด `.bak` พร้อมข้อความเตือน → ถ้า `.bak` เสียด้วยจึงใช้ข้อมูลตั้งต้น |

```
ไฟล์หลักอ่านได้? ──ใช่──► ใช้ไฟล์หลัก
     │ไม่ (เสีย/หาย)
     ▼
.bak อ่านได้? ──ใช่──► ใช้ .bak + "Restored data from backup ..."
     │ไม่
     ▼
ข้อมูลตั้งต้น + "Loading default data."
```

ปิด Known Issue **KI-03** (สัปดาห์ที่ 13) ที่ไฟล์เสียทั้งไฟล์แล้วการบันทึกครั้งถัดไปจะทับข้อมูลเดิม

**เทสต์ใหม่** — [`test_disaster_recovery.py`](../../test_disaster_recovery.py) 9 เคส รวม
`test_repository_disaster_recovery_fallback` ตามโจทย์ใบงาน · ชุดทดสอบรวม **195 passed** · coverage 99%

### 4.2 Drill 1 — Data Corruption (รันผ่าน CLI จริง)

| ขั้น | การกระทำ | ผล |
|---|---|---|
| 1 | เพิ่ม Milk 10 ชิ้น → ขาย 3 (บันทึก 2 ครั้ง) | มี `inventory_db.json` และ `inventory_db.json.bak` |
| 2 | ลบปีกกาปิดท้ายไฟล์ | `JSONDecodeError: Expecting ',' delimiter` |
| 3 | เปิดโปรแกรมใหม่ | `Warning: Database file is corrupted. Restored data from backup inventory_db.json.bak.` |
| 4 | ดูสินค้า → ขายต่อ 2 | Milk แสดง 10 · ขายได้ปกติ → 8 |
| 5 | ตรวจไฟล์ | ไฟล์หลักกลับมาถูกต้อง (8) · `.bak` = 10 |

| ตัวชี้วัด | ค่า |
|---|---|
| **RTO** (เปิดโปรแกรมจนใช้งานต่อได้) | **150 ms** — อัตโนมัติ ไม่ต้องมีคนช่วย |
| **RPO** (ข้อมูลที่หาย) | **รายการล่าสุด 1 รายการ** — การขาย 3 ชิ้นก่อนไฟล์เสียหายไป ผู้ใช้ต้องตรวจและบันทึกซ้ำ |

Log: [`evidence/data_corruption_drill.txt`](evidence/data_corruption_drill.txt)

### 4.3 Drill 2 — Git Rollback (scratch clone ไม่แตะ repo จริง)

**รอบที่ 1 — ตามตัวอย่างในใบงาน: `git revert -m 1` merge ของ release**

| | |
|---|---|
| ขั้นตอน | จำลอง merge release เข้า `main` → `git revert -m 1 HEAD` → รันเทสต์ → tag `v1.0.0-rollback` |
| เวลา | 1.1 วินาที |
| ผล | ❌ **24 failed, 13 passed** — โปรแกรมเปิดได้ แต่ระบบที่ถอยกลับไปเป็นของที่เสียอยู่แล้ว |

### ⚠️ ข้อค้นพบสำคัญ — REL-01: `main` ปัจจุบันเสียมาตั้งแต่เดือนสิงหาคม

```
TypeError: load() takes 0 positional arguments but 1 was given
```

`main` (`a10ea24`) มี `test_app.py` เวอร์ชันที่เรียก `load(inv)` แต่ `app_v2.py` เวอร์ชันที่ `load()` ไม่รับพารามิเตอร์
— ผลจาก PR #14 (merge เทสต์ที่ไม่ผ่าน) และ PR #15 (revert ไม่ครบ) ไม่มีใครเห็นเพราะทีมทำงานบน `develop` อย่างเดียว
5 Whys อยู่ใน [Dossier หมวด 5](../Final_System_Maintenance_Dossier.md#5-whys--rel-01-main-เสีย)

| แท็ก | ผลรันเทสต์ |
|---|---|
| `v1.0.0-baseline` | ไม่มีเทสต์ |
| `v2.0` | 104 passed |
| `v2.1` | **148 passed** ← แท็กล่าสุดที่ผ่านการทดสอบ |

**รอบที่ 2 — ขั้นตอนที่ถูกต้อง: คืนสภาพจากแท็กที่ผ่านการทดสอบเป็น commit ใหม่**

```bash
git restore --source v2.1 --staged --worktree -- .
git commit -m "Emergency rollback to last verified release v2.1"
python -m pytest -q                       # 148 passed
git tag -a v2.1-rollback -m "Emergency rollback to last verified release v2.1"
```

| ตัวชี้วัด | ค่า |
|---|---|
| **RTO** (restore → commit → test → tag → เปิดโปรแกรม) | **1.37 วินาที** (ไม่รวมเวลาตัดสินใจของคน) |
| ประวัติ commit | ครบ — เป็น commit ใหม่ ไม่ใช้ `reset --hard` |
| เนื้อหาหลัง rollback | ตรงกับ `v2.1` ทุกไฟล์ (`git diff --quiet v2.1 HEAD`) |
| Roll-forward (revert ตัว revert) | 1.5 วินาที · 195 passed |

Log: [`evidence/git_rollback_drill.txt`](evidence/git_rollback_drill.txt)

**บทเรียน** — *จุดถอยกลับต้องเป็นแท็กที่ผ่านเทสต์ ไม่ใช่ "commit ก่อนหน้า"* ปรับไว้ใน
[O&M Manual บทที่ 7.2](../System_Operations_and_Maintenance_Manual.md#72-rollback-เวอร์ชัน-ซ้อมจริงแล้วสัปดาห์ที่-14--rto-14-วินาที)
และเป็นอีกเหตุผลที่ต้องรีบ release `v2.0.0-evolution` เข้า `main`

### 4.4 Disaster Recovery Test Report Form

| # | สถานการณ์ | วิธีจำลอง | เกณฑ์ผ่าน | RTO | RPO | ผล |
|---|---|---|---|---|---|---|
| DR-01 | ไฟล์ข้อมูลเสีย | ลบปีกกาปิดท้าย | กู้อัตโนมัติ ไม่ crash | 0.15 s | 1 รายการ | ✅ |
| DR-02 | ไฟล์ข้อมูลถูกลบ | ลบไฟล์หลัก | กู้จาก `.bak` | อัตโนมัติ | 1 รายการ | ✅ (unit test) |
| DR-03 | ไฟล์หลักและ `.bak` เสียทั้งคู่ | เขียนขยะทั้งสองไฟล์ | ไม่ crash · เตือนชัดเจน | — | ทั้งหมด → ต้องใช้สำรองนอกเครื่อง | ✅ (unit test) |
| DR-04 | Release พังบน production | `git revert` merge | กลับสู่สถานะที่เทสต์ผ่าน | 1.1 s | — | ❌ ถอยไปเจอ `main` ที่เสีย |
| DR-05 | Release พังบน production | `git restore --source v2.1` | กลับสู่สถานะที่เทสต์ผ่าน | 1.37 s | — | ✅ 148 passed |

---

## 5. แก้ไขรายงานสัปดาห์ที่ 13

ระหว่างตรวจ complexity สัปดาห์นี้พบว่า `load_env_file()` ที่เพิ่มในสัปดาห์ที่ 13 มี v(G) = **9** เกินเกณฑ์ ≤ 8
แต่รายงานสัปดาห์ที่ 13 ระบุ max = 7 (สแกนก่อนเพิ่มฟังก์ชันนี้)
แก้โดยแยก `_parse_env_line()` ออกมา → `load_env_file` 5 · `_parse_env_line` 6 · max ทั้งไฟล์กลับเป็น **7**
และเพิ่มหมายเหตุแก้ไขในรายงานสัปดาห์ที่ 13 แล้ว
