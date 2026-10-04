# รายงานผลการทดสอบ Full Regression Test Suite
## ENGSE225 · สัปดาห์ที่ 11 · ชิ้นงานที่ 2 และ 3

| | |
|---|---|
| Commit ที่ทดสอบ | `hardening/week11-flake8-bandit` (ก่อน merge เข้า `develop`) |
| สภาพแวดล้อม | Windows 11 · Python 3.13.7 · pytest 9.1.1 · pytest-cov 7.1.0 |
| ผู้ทดสอบ | ตรัยรัตน์ วงษ์สิทธิ์ (QA) |
| วันที่ | 2026-10-05 |
| Log เต็ม | [`evidence/pytest_coverage.txt`](evidence/pytest_coverage.txt) |

---

## 1. ผลการรัน

```
$ pytest -v --cov=app_v2 --cov-report=term-missing
...
test_hardening.py::TestMenuTable::test_every_choice_except_exit_has_a_handler PASSED [ 99%]
test_hardening.py::test_full_system_integration_flow PASSED              [100%]

Name        Stmts   Miss  Cover   Missing
-----------------------------------------
app_v2.py     224      2    99%   375, 379
-----------------------------------------
TOTAL         224      2    99%
============================= 167 passed in 1.12s =============================
```

| ไฟล์ | จำนวน | ผ่าน | ครอบคลุม |
|---|---:|---:|---|
| `test_app.py` | 37 | 37 | Regression suite ของ Sprint 1 — **ไม่ได้แก้ตรรกะเทสต์เลย** แก้เฉพาะรูปแบบให้ผ่าน flake8 |
| `test_app_v2.py` | 111 | 111 | คลาสทั้ง 5 · CR-01 · CR-02 · DEF-01/02/03 · integration |
| `test_hardening.py` | 19 | 19 | **ใหม่สัปดาห์นี้** — code smell refactor · atomic I/O · ข้อบกพร่องแฝง 2 จุด · E2E |
| **รวม** | **167** | **167 (100%)** | |

**บรรทัดที่ไม่ถูกครอบคลุม 2 บรรทัด** คือ `main()` และ `if __name__ == "__main__":`
ซึ่งเป็นจุดเข้าโปรแกรมที่ต้องรอ input จากคีย์บอร์ด ตรรกะข้างในทั้งหมดถูกทดสอบผ่าน `ConsoleUI` ที่ inject input/print ได้แล้ว

---

## 2. Coverage Benchmark เทียบเกณฑ์ใบงาน

| ชั้นสถาปัตยกรรม | เกณฑ์ | ผลจริง | สถานะ |
|---|---:|---:|---|
| Domain Model (`Product`) | 100% | 100% | 🟢 |
| Data Access (`InventoryRepository`) | 100% | 100% | 🟢 Atomic I/O ทดสอบทั้งกรณีสำเร็จและล้มเหลว |
| Business Logic (`InventoryService`) | 100% | 100% | 🟢 |
| Report (`CsvReportExporter`) | — | 100% | 🟢 |
| Presentation (`ConsoleUI`) | — | 100% | 🟢 |
| **ทั้งระบบ** | **≥ 90%** | **99%** | 🏆 |

> ตัวเลขรายคลาสได้จากการไล่บรรทัดที่ขาด (`375, 379`) ซึ่งอยู่นอกคลาสทั้งหมด
> pytest-cov รายงานเป็นรายไฟล์ ไม่ได้แยกรายคลาส

---

## 3. End-to-End Integration Test — `test_full_system_integration_flow`

ตามโจทย์ใบงาน ขั้นที่ 3 ทดสอบวงจรเต็มตั้งแต่สต๊อกถึงไฟล์ CSV โดยใช้คลาสจริงทุกตัวและไฟล์จริงบนดิสก์

| ขั้น | การกระทำ | สิ่งที่ตรวจ |
|---|---|---|
| 1 | เพิ่ม `P1 Pen` qty 10 · barcode `885` · reorder point 5 | ได้ `(True, "Done.")` |
| 2 | ตัดสต๊อก 6 ชิ้น (เหลือ 4) | สำเร็จ |
| 3 | เรียก `get_reorder_list()` | ได้ `["P1"]` |
| 4 | ค้นด้วยบาร์โค้ด `885` | เจอ qty 4 |
| 5 | Export CSV | 4 แถว (default 3 + Pen) |
| 6 | สร้าง service ใหม่จากไฟล์เดิม (จำลองปิด-เปิดโปรแกรม) | ข้อมูลตรงกับก่อนปิด |
| 7 | อ่าน CSV กลับ | `barcode=885`, `qty=4`, `reorder_point=5` และไม่มีไฟล์ `.tmp` ค้าง |

> ใบงานเรียกเมธอดว่า `get_low_stock_alerts()` — ในระบบนี้ชื่อ `get_reorder_list()` (ตั้งชื่อตั้งแต่ CR-01 สัปดาห์ที่ 9)

---

## 4. เทสต์ใหม่ที่จับข้อบกพร่องจริง

เทสต์ 2 กลุ่มนี้ตรวจพฤติกรรมที่**ยืนยันแล้วว่าผิดบนโค้ดก่อนแก้** (`develop` @ `1a5c024`)
และผ่านหลังแก้ — ผลการจำลองบนโค้ดเดิมดูใน [`evidence/latent_defects_on_develop.txt`](evidence/latent_defects_on_develop.txt)

| เทสต์ | ข้อบกพร่องที่จับได้ |
|---|---|
| `TestServiceDoesNotLieAboutSaving` (3 เคส) | ดิสก์เขียนไม่ได้แต่ระบบตอบ `Done.` — ข้อมูลหายเมื่อปิดโปรแกรม |
| `test_json_list_is_treated_as_corrupted` | `data.json` เป็น `[1,2,3]` ทำให้โปรแกรมตายตั้งแต่เปิด |

รายละเอียดสาเหตุดูใน [Security & Static Analysis Report ข้อ 5.2–5.3](Security_Static_Analysis_Report.md#52-️-ข้อบกพร่องแฝงที่พบ--save-กลืน-error-แล้วระบบตอบ-done)

---

## 5. ประวัติจำนวนเทสต์

| ช่วง | Tests | Coverage |
|---|---:|---:|
| Sprint 1 (v1.1) | 37 | — |
| Sprint 2 (v2.0) | 104 | — |
| หลัง CR-01/CR-02/Bug bashing (v2.1) | 148 | 98% |
| **หลัง Hardening สัปดาห์ที่ 11** | **167** | **99%** |

---

## 6. ภาพบันทึกหน้าจอ

> 📸 **ต้องแคปเอง:** รัน `pytest -v --cov=app_v2 --cov-report=term-missing` บนเครื่อง
> แล้วแคปหน้าจอส่วนท้ายที่เห็น `167 passed` และตาราง coverage `99%`
> บันทึกไว้ที่ `docs/week11/evidence/pytest_screenshot.png`
>
> ข้อความผลลัพธ์จริงเก็บไว้แล้วใน [`evidence/pytest_coverage.txt`](evidence/pytest_coverage.txt)
