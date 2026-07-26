# Combined Report Phase 1.3
## RACI Matrix + Definition of Done (DoD) + GitHub Setup Guide
### Inventory System v1.0



---

## ส่วนที่ 1 — RACI Matrix

> **R** = Responsible (ผู้ลงมือทำ) | **A** = Accountable (ผู้รับผิดชอบผล) | **C** = Consulted (ผู้ให้คำปรึกษา) | **I** = Informed (ผู้รับทราบ)

| กิจกรรม / Deliverable | PM | Tech Lead | Developer | QA |
|---|:---:|:---:|:---:|:---:|
| **การวางแผนและติดตาม** | | | | |
| กำหนด Sprint Goal และ Timeline | A/R | C | I | I |
| อัปเดตสถานะงานใน Jira ทุกสัปดาห์ | R | I | R | R |
| ประสานงานระหว่าง Sprint | A/R | C | C | C |
| **GitHub Repository** | | | | |
| สร้าง GitHub Organization + Repo | R | C | I | I |
| กำหนด Branch Protection Rules | C | A/R | I | I |
| ตั้งค่า GitFlow (develop + feature/) | C | A/R | R | I |
| Review และ Merge Pull Request | I | A/R | C | R |
| **การพัฒนาโค้ด** | | | | |
| Refactor global state (INV-4) | I | A/R | C | C |
| แก้ไข Input Validation (INV-6,7) | I | C | A/R | C |
| แก้ไข Logic Bug (INV-5,8,9) | I | A | R | C |
| แก้ไข File I/O Safety (INV-10,11) | I | C | A/R | C |
| **การทดสอบ** | | | | |
| เขียน Test Plan (INV-13) | I | C | C | A/R |
| เขียน Unit Tests test_app.py (INV-14) | I | C | C | A/R |
| รัน Regression Test ก่อน Merge | I | C | C | A/R |
| ยืนยันว่า test ผ่านทั้งหมดก่อน merge | I | R | C | A/R |
| **เอกสาร** | | | | |
| System Architecture Document (INV-15) | I | A/R | C | I |
| Changelog + Release Notes (INV-16) | A/R | C | C | I |
| Combined Report ทุก Phase | A/R | C | C | C |

### สรุป Workload ตามบทบาท

| บทบาท | A/R (รับผิดชอบหลัก) | R (ลงมือทำ) | C (ปรึกษา) |
|---|:---:|:---:|:---:|
| PM | 5 | 3 | 5 |
| Tech Lead | 7 | 4 | 7 |
| Developer | 5 | 5 | 5 |
| QA | 5 | 3 | 4 |

---

## ส่วนที่ 2 — Definition of Done (DoD)

> เกณฑ์ที่ต้องครบถ้วน **ทุกข้อ** ก่อนย้าย Task จาก "In Review" → "Done" บน Jira

### 2.1 DoD สำหรับ Bug Fix Task (INV-5, 6, 7, 8, 9, 10, 11, 12)

- [x] **โค้ดเขียนถูกต้อง** — แก้ไขตรงกับ requirement ที่ระบุในตั๋ว Jira
- [x] **Unit Test ผ่าน** — `pytest test_app.py -v` ไม่มี FAILED ทุก test
- [x] **ไม่มี Regression** — test ทั้งหมดที่มีอยู่เดิมยังผ่าน (ไม่ใช่แค่ test ใหม่)
- [x] **Code Review ผ่าน** — Tech Lead ตรวจและ Approve PR แล้ว
- [x] **ไม่มี merge conflict** — branch อัปเดตจาก `develop` ล่าสุดแล้ว
- [x] **Commit message ชัดเจน** — ระบุว่าแก้อะไร อ้างอิง INV-XX
- [x] **ลบ debug code** — ไม่มี `print()` หรือ comment ที่ไม่จำเป็นหลงเหลือ

### 2.2 DoD สำหรับ Test Task (INV-13, 14)

- [x] **Test coverage ครอบคลุม** — ทุก menu มี test อย่างน้อย 3 กรณี (happy path, edge case, error case)
- [x] **Known bugs มี test ล็อกไว้** — ทุก bug ที่รู้แล้วต้องมี test ที่ขึ้นต้นด้วย `test_BUG_`
- [x] **Test รันได้ด้วย** `pytest test_app.py -v` ไม่มี ERROR
- [x] **Test isolate กัน** — แต่ละ test ไม่พึ่งพาลำดับการรัน (ใช้ fixture reset_inventory)
- [x] **ไม่ใช้ข้อมูล data.json จริง** — ใช้ temp_db fixture แทน

### 2.3 DoD สำหรับ Documentation Task (INV-15, 16)

- [x] **ครอบคลุมทุกส่วนที่เปลี่ยนแปลง** — ทุก function ที่แก้ไขมีอธิบายใหม่
- [x] **อ่านเข้าใจได้โดยคนนอกทีม** — ตรวจโดย PM
- [x] **เขียนเป็น Markdown** — push ขึ้น repo ได้เลย

### 2.4 DoD สำหรับ Sprint (ภาพรวม)

- [x] **ทุก INV-XX ที่อยู่ใน Sprint มีสถานะ Done** — ไม่มี "In Progress" ค้างข้าม Sprint
- [x] **Jira board อัปเดตครบ** — ทุก task มี Assignee, ไม่มีที่ว่างเปล่า
- [x] **develop branch สะอาด** — ไม่มี merge conflict, CI ผ่าน (ถ้ามี)
- [x] **Sprint Review ทำแล้ว** — ทีมนำเสนอสิ่งที่ทำสำเร็จในรอบนี้

---

## ส่วนที่ 3 — GitHub Repository + GitFlow Setup Guide

> ส่วนนี้ทำเองโดยสมาชิกทีม — ทำตามขั้นตอนด้านล่างตามลำดับ

### 3.1 สร้าง GitHub Organization + Repository

```
1. ไปที่ github.com → ขวาบน + → "New organization"
2. เลือก Free plan → ตั้งชื่อ เช่น: ENGSE225-GroupX
3. เชิญสมาชิกทั้ง 4 คนเข้า organization
4. สร้าง repo ชื่อ: inventory-system-maintenance
   - Visibility: Public (ให้อาจารย์ตรวจได้)
   - เลือก "Add a README file"
   - เลือก .gitignore: Python
```

### 3.2 GitFlow Branch Structure

```
main          ← production (ห้ามแก้ตรง)
└── develop   ← integration branch (ทุก feature merge มาที่นี่)
    ├── feature/pm/project-charter         (INV-2)
    ├── feature/tl/refactor-global-state   (INV-4)
    ├── feature/dev/input-validation       (INV-6)
    ├── feature/dev/fix-negative-stock     (INV-7)
    ├── feature/dev/fix-naming-collision   (INV-5)
    └── feature/qa/unit-tests              (INV-13, INV-14)
```

### 3.3 คำสั่ง Git ที่ต้องรู้

```bash
# ── Clone repo ครั้งแรก ──
git clone https://github.com/ENGSE225-GroupX/inventory-system-maintenance.git
cd inventory-system-maintenance

# ── สร้าง develop branch ──
git checkout -b develop
git push -u origin develop

# ── แต่ละคนสร้าง feature branch ของตัวเอง ──
git checkout develop
git checkout -b feature/qa/unit-tests

# ── ทำงาน → commit ──
git add test_app.py
git commit -m "feat(qa): add unit tests for Check Check menu [INV-13,14]"

# ── Push และสร้าง Pull Request ──
git push -u origin feature/qa/unit-tests
# → ไปที่ GitHub → สร้าง PR: feature/qa/unit-tests → develop

# ── ก่อน merge ต้องรัน test ให้ผ่านก่อน ──
pytest test_app.py -v
```

### 3.4 Commit Message Convention

```
format: <type>(<scope>): <description> [INV-XX]

type:
  feat     = เพิ่มฟีเจอร์ใหม่
  fix      = แก้บั๊ก
  test     = เพิ่ม/แก้ test
  docs     = แก้เอกสาร
  refactor = refactor โดยไม่เปลี่ยน behavior

ตัวอย่าง:
  fix(menu3): validate negative amount input [INV-7]
  feat(menu2): add qty accumulation instead of overwrite [INV-8]
  test(qa): lock Check Check total value calculation [INV-14]
  refactor(core): remove global x, pass as parameter [INV-4]
```

### 3.5 Branch Protection Rules (ตั้งค่าใน GitHub)

```
Settings → Branches → Add rule → Branch name: develop

เลือก:
  ✅ Require a pull request before merging
  ✅ Require approvals: 1 (Tech Lead ต้อง approve)
  ✅ Require status checks to pass (ถ้ามี CI)
  ✅ Do not allow bypassing the above settings
```

### 3.6 .gitignore ที่แนะนำ

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
.pytest_cache/
.coverage

# Data (ห้าม commit ข้อมูลจริง)
data.json

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## Checklist ก่อนส่ง

- [x] ลิงก์ GitHub Repository: `https://github.com/PeawZaZa/software_mnm'`
- [x] Branch `develop` สร้างแล้วและมี commit อย่างน้อย 1 รายการ
- [x] แต่ละสมาชิกมี `feature/` branch ของตัวเองอย่างน้อย 1 อัน
- [x] ไฟล์ `test_app.py` push ขึ้น repo แล้วและ pytest ผ่านทุก test
- [x] RACI Matrix กรอกชื่อจริงของสมาชิกในแต่ละบทบาทแล้ว
- [] DoD copy ไปติดใน Jira board (Description ของ Sprint) แล้ว

---
*อ้างอิงจาก System Understanding Report — Code Archaeology Week 1 และ Project Charter Phase 1.1*
