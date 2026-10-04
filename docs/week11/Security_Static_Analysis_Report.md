# รายงานผลการสแกนความปลอดภัยและคุณภาพโค้ด (Flake8 & Bandit Security Report)
## ENGSE225 · สัปดาห์ที่ 11 — System Hardening & Code Freeze · ชิ้นงานที่ 1

| | |
|---|---|
| ระบบ | Inventory System (`app_v2.py`) |
| สาขาที่สแกน | `hardening/week11-flake8-bandit` → merge เข้า `develop` |
| เครื่องมือ | flake8 7.4.1 · bandit 1.9.4 · radon 6.0.1 · Python 3.13.7 |
| ผู้จัดทำ | ตรัยรัตน์ วงษ์สิทธิ์ (QA) · ตรวจทานโดย พนาวุฒน์ อภิปสันติ (Tech Lead) |
| วันที่สแกน | 2026-10-05 |
| หลักฐานดิบ | [`evidence/`](evidence/) — ผลลัพธ์จากเครื่องมือโดยตรง ไม่ได้ตัดต่อ |

---

## 1. สรุปผลในหน้าเดียว

| ตัวชี้วัด | ก่อน (`develop` @ `1a5c024`) | หลัง | เกณฑ์ |
|---|---:|---:|---|
| Flake8 (PEP 8, Syntax, Unused imports) | **270** | **0** | 0 ✅ |
| Bandit — High / Medium / Low | 0 / 0 / 0 | 0 / 0 / 0 | ไม่มี Medium ขึ้นไป ✅ |
| Max Cyclomatic Complexity v(G) | 9 (`ConsoleUI.run`) | **6** | ≤ 8 ✅ |
| Code smell ที่พบ | 4 | 0 | — |
| ข้อบกพร่องแฝง (Latent defect) ที่พบระหว่าง hardening | — | **2 พบและแก้แล้ว** | — |
| Unit tests | 148 passed | **167 passed** | 100% ✅ |
| Coverage (`app_v2.py`) | 98% | **99%** | ≥ 90% ✅ |

---

## 2. Flake8 — ตรวจรูปแบบโค้ดตาม PEP 8

### 2.1 ผลก่อนแก้ (ค่า default ของ flake8 ไม่รวม `app_v1.py`)

```
1     E231 missing whitespace after ','
119   E261 at least two spaces before inline comment
1     E272 multiple spaces before keyword
6     E302 expected 2 blank lines, found 1
142   E501 line too long (89 > 79 characters)
1     W292 no newline at end of file
270
```

ไม่พบ `F401` (unused import), `F841` (unused variable) หรือ `E999` (syntax error)
ทั้งหมดเป็นปัญหารูปแบบ ไม่ใช่ปัญหาตรรกะ

### 2.2 สิ่งที่ทำ

| ประเภท | จำนวน | วิธีแก้ |
|---|---:|---|
| E261 คอมเมนต์ท้ายบรรทัดเว้นวรรคไม่พอ | 119 | เติมช่องว่างเป็น 2 ช่องก่อน `#` |
| E501 บรรทัดยาวเกิน | 142 | (1) ลบคอมเมนต์ประวัติ `# แก้ไข: ...` 111 จุดใน `test_app.py` — ดูข้อ 4.3 (2) ตัดบรรทัดที่เหลือ (3) ตั้ง `max-line-length = 99` |
| E302 / E231 / E272 / W292 | 9 | จัดบรรทัดว่าง/ช่องว่างตาม PEP 8 |

**เหตุผลที่ตั้ง `max-line-length = 99`** — PEP 8 ระบุว่าทีมสามารถตกลงขยายได้ถึง 99 ตัวอักษร
และโปรเจกต์นี้มีคอมเมนต์ภาษาไทยจำนวนมาก การตั้งค่าอยู่ในไฟล์ [`.flake8`](../../.flake8)
ซึ่งถูก commit เข้า repo ทำให้ทุกคนและ CI ใช้เกณฑ์เดียวกัน

> **ความโปร่งใส:** ถ้าวัดด้วยค่า default 79 ตัวอักษร จะยังเหลือ E501 จำนวน 92 จุด
> (ทุกจุดยาวระหว่าง 80–99 ตัวอักษร) ไม่มีปัญหาประเภทอื่นเหลือเลย

**`app_v1.py` ไม่ถูกสแกน** — เป็น baseline v1.0.0 ที่อาจารย์ให้มา เก็บไว้ตามต้นฉบับเพื่อใช้เทียบ
metrics ก่อน/หลังในแฟ้ม Maintenance Dossier (สัปดาห์ที่ 14) และไม่ได้ถูกใช้งานจริงแล้ว

### 2.3 ผลหลังแก้

```
$ flake8 . --count --statistics
0
```

---

## 3. Bandit — สแกนช่องโหว่ความปลอดภัยระดับซอร์สโค้ด

```
$ bandit -r . -x ./test_app.py,./test_app_v2.py,./test_hardening.py
Test results:
        No issues identified.
Code scanned:
        Total lines of code: 380
Run metrics:
        Total issues (by severity):  Undefined: 0  Low: 0  Medium: 0  High: 0
```

ผลเต็มอยู่ใน [`evidence/bandit_report.txt`](evidence/bandit_report.txt)

| สิ่งที่ Bandit ตรวจ | ผลในโปรเจกต์นี้ |
|---|---|
| Hardcode รหัสผ่าน / API key (B105–B107) | ไม่พบ — โปรแกรมไม่มีการเชื่อมต่อภายนอก |
| `eval()` / `exec()` / `pickle` (B102, B301, B307) | ไม่พบ — ใช้ `json` ซึ่งปลอดภัยต่อการ deserialize |
| `subprocess` / shell injection (B602–B607) | ไม่พบ |
| `try/except/pass` กลืน error (B110) | ไม่พบ — แต่พบ **การกลืน error แบบที่ Bandit จับไม่ได้** ดูข้อ 5.2 |
| ไฟล์ชั่วคราวที่คาดเดาได้ (B108) | ไม่พบหลังแก้ — เปลี่ยนเป็น `tempfile.mkstemp()` |

**ทำไมสแกนไม่รวมไฟล์เทสต์** — ไฟล์เทสต์ใช้ `assert` เป็นหลัก ซึ่ง Bandit จะรายงานเป็น B101
ทุกบรรทัด (เป็น false positive ที่ทราบกันดี) จึงยกเว้นตามคำสั่งในใบงาน `bandit -r . -x ./tests`

---

## 4. Code Smell Audit

### 4.1 Duplicate Code — ตรรกะค้นบาร์โค้ดเขียนซ้ำ 2 ที่

**ที่พบ:** `find_by_barcode()` และ `_barcode_owner()` วนลูปเทียบ `product.barcode == barcode`
และเช็กบาร์โค้ดว่างแยกกันคนละที่ ถ้าวันหนึ่งเปลี่ยนกฎ (เช่น ตัดช่องว่างหน้า-หลังบาร์โค้ด)
แล้วแก้ไม่ครบ ระบบจะค้นเจอแต่ตรวจซ้ำไม่เจอ

**แก้ด้วย Extract Method:** สร้าง `_products_with_barcode()` เป็นจุดเดียวที่ค้นหา แล้วให้ทั้งสองเมธอดเรียกใช้

**ผลพลอยได้:** แบบเดิม `_barcode_owner()` หยุดที่สินค้าตัวแรกที่ตรง ถ้า `data.json` เก่ามีบาร์โค้ดซ้ำ
(ก่อนแก้ #20) แบบใหม่ข้ามตัวเองไปเจอเจ้าของตัวจริงได้ — มีเทสต์ `test_owner_skips_itself_even_with_legacy_duplicates`

### 4.2 Feature Envy — คลาสอื่นคำนวณข้อมูลของ `Product` เอง

| จุดที่พบ | ย้ายไปเป็น |
|---|---|
| `InventoryService.get_summary()` คำนวณ `p.qty * p.price` | `Product.stock_value` (property) |
| `InventoryService.get_reorder_list()` เช็ก `p.reorder_point > 0 and p.qty <= p.reorder_point` | `Product.needs_reorder()` |

กฎ "reorder point = 0 แปลว่ายังไม่ได้ตั้ง" ตอนนี้อยู่ที่เดียวในคลาสเจ้าของข้อมูล

### 4.3 Dead Code — คอมเมนต์ประวัติการแก้ 111 จุด

`test_app.py` มีคอมเมนต์ต่อท้ายบรรทัดแบบ `# แก้ไข: เปลี่ยนจาก app.x เป็น inventory` 111 จุด
ซึ่งเป็นบันทึกว่า *เคย* แก้อะไร ไม่ได้อธิบายว่าโค้ด *ตอนนี้* ทำอะไร ข้อมูลนี้อยู่ใน git history ครบแล้ว
(`git log -p test_app.py`) จึงลบทิ้งตามหลัก *Delete Ruthlessly*

คอมเมนต์ `# global variables` เหนือ `db = "data.json"` ก็ทำให้เข้าใจผิดว่ายังมี global state อยู่
จึงเปลี่ยนเป็นคำอธิบายที่ถูกต้อง (เป็นค่าคงที่ระดับโมดูล ไม่ถูกแก้ระหว่างรัน)

### 4.4 Long Conditional — `ConsoleUI.run()` มี if/elif 8 ชั้น

เปลี่ยนเป็นตารางเมนู `menu()` ที่จับคู่ เลขเมนู → (ชื่อ, handler) ข้อดีคือ
เพิ่มเมนูใหม่แก้ที่เดียว และชื่อเมนูที่พิมพ์กับ handler ที่เรียกจะไม่มีทางไม่ตรงกัน

| เมธอด | v(G) ก่อน | v(G) หลัง |
|---|---:|---:|
| `ConsoleUI.run` | 9 | 5 |
| ค่าเฉลี่ยทั้งไฟล์ | — | 2.79 (A) |

---

## 5. ความมั่นคงของระบบไฟล์ (Secure & Atomic I/O)

### 5.1 Atomic File Writing — ปรับปรุงจากของเดิม

ระบบมี atomic write ตั้งแต่ INV-11 (Sprint 1) แล้ว แต่ตรวจพบจุดอ่อน 3 ข้อ

| จุดอ่อนเดิม | ความเสี่ยง | แก้เป็น |
|---|---|---|
| ชื่อไฟล์ชั่วคราวตายตัว `data.json.tmp` | เปิดโปรแกรม 2 หน้าต่างพร้อมกัน จะเขียนทับไฟล์ชั่วคราวของกันและกัน | `tempfile.mkstemp()` ชื่อไม่ซ้ำ อยู่โฟลเดอร์เดียวกับไฟล์จริง |
| ไม่ `fsync` ก่อนสลับไฟล์ | ไฟดับหลัง `os.replace()` ข้อมูลอาจยังค้างใน cache ของ OS | `f.flush()` + `os.fsync()` ก่อน `os.replace()` |
| บันทึกล้มเหลวแล้วทิ้งไฟล์ `.tmp` ค้าง | ขยะสะสม | ลบไฟล์ชั่วคราวใน `except` |

```python
fd, temp_name = tempfile.mkstemp(prefix=self.path.name + ".", suffix=".tmp", dir=directory)
with os.fdopen(fd, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)
    f.flush()
    os.fsync(f.fileno())
os.replace(temp_name, self.path)      # All-or-Nothing ระดับ OS
```

ทดสอบโดยจำลองให้ `os.replace()` ล้มเหลว แล้วยืนยันว่า**ไฟล์เดิมยังอยู่ครบทุกไบต์**
(`test_failed_save_keeps_original_file_intact`)

### 5.2 ⚠️ ข้อบกพร่องแฝงที่พบ — `save()` กลืน error แล้วระบบตอบ "Done."

```python
# ก่อนแก้
except Exception as e:
    print(f"Error saving data: {e}")      # แล้วจบ ไม่คืนค่าอะไร
```

`InventoryService` ไม่รู้เลยว่าบันทึกไม่สำเร็จ จึงตอบผู้ใช้ว่า `Done.` / `Stock updated.`
ข้อมูลอยู่แค่ในหน่วยความจำ **ปิดโปรแกรมเมื่อไหร่ข้อมูลหายทันที** — เป็นตัวอย่างของ
*Blind Exception Swallowing* ตามใบงาน ที่ Bandit จับไม่ได้เพราะไม่ใช่ `except: pass` ตรง ๆ

| | ก่อน | หลัง |
|---|---|---|
| `save()` | คืน `None` เสมอ | คืน `True` / `False` และจับเฉพาะ `OSError` |
| `add_update()` เมื่อบันทึกไม่ได้ | ตอบ `Done.` | ย้อนข้อมูลในหน่วยความจำ แล้วตอบ `Error: could not save data to disk. No changes were made.` |
| `stock_out()` เมื่อบันทึกไม่ได้ | ตอบ `Stock updated.` | คืนจำนวนสต๊อกเดิม แล้วตอบข้อความเดียวกัน |

### 5.3 ⚠️ ข้อบกพร่องแฝงที่พบ — `load()` พังเมื่อ JSON ถูกไวยากรณ์แต่ผิดรูปแบบ

ไฟล์ `data.json` ที่เป็น `[1, 2, 3]` ผ่าน `json.loads()` ได้ แต่ไปพังที่ `.items()` ด้วย
`AttributeError` ซึ่ง**อยู่นอก** `try` จึงทำให้โปรแกรมตายตั้งแต่เปิด
แก้โดยตรวจว่าเป็น `dict` ภายใน `try` และเปลี่ยน `except Exception` เป็น exception ที่เจาะจง
`(OSError, UnicodeDecodeError, ValueError)`

---

## 6. การผสานสายงาน CR-01 + CR-02 (Integration)

ใบงานให้ merge `feature/cr01-barcode-reorder-point` ก่อน แล้วจึง sync และ merge `feature/cr02-csv-export`
**ทีมทำตามลำดับนี้ไปแล้วในสัปดาห์ที่ 10** ตรวจสอบย้อนหลังได้จาก GitHub

| ลำดับ | PR | เวลา merge (เวลาไทย) | Conflict |
|---|---|---|---|
| 1 | [#24](https://github.com/PeawZaZa/software_mnm/pull/24) CR-01 | 2026-09-07 01:18 | ไม่มี |
| 2 | [#25](https://github.com/PeawZaZa/software_mnm/pull/25) CR-02 | 2026-09-07 01:19 | ไม่มี — สาขา cr02 แตกออกจาก commit ของ cr01 (`74367ea`) โดยตรง จึงมีโค้ด CR-01 อยู่แล้ว |
| 3 | [#26](https://github.com/PeawZaZa/software_mnm/pull/26) Bug fixes | 2026-09-07 01:20 | ไม่มี |

สัปดาห์นี้งาน hardening ทำบนสาขาเดียว `hardening/week11-flake8-bandit` แล้ว merge เข้า `develop`
แบบ `--no-ff` เพื่อให้ประวัติแสดงเป็นก้อนงานที่ชัดเจน

---

## 7. CI Pipeline — ล็อกคุณภาพไม่ให้ถอยหลัง

ปรับ [`.github/workflows/pytest.yml`](../../.github/workflows/pytest.yml) ให้ทุก push/PR ไป `develop` และ `main` ต้องผ่าน

1. `flake8 . --count --statistics` — ต้องได้ 0
2. `bandit -r . -ll` — ล้มเมื่อพบ Medium ขึ้นไป
3. `pytest --cov=app_v2 --cov-fail-under=90` — เทสต์ต้องผ่านทั้งหมดและ coverage ≥ 90%
4. รันบน Python 3.10 และ 3.12

> ⚠️ **ข้อจำกัดที่ยังมีอยู่:** บัญชี GitHub ยังติดปัญหา billing ตั้งแต่สัปดาห์ที่ 9 workflow จึงยังไม่ถูกรันจริง
> ทีมรันคำสั่งชุดเดียวกันบนเครื่องก่อน merge ทุกครั้ง และเก็บผลไว้ใน [`evidence/`](evidence/)

---

## 8. ประกาศ Code Freeze (ISO/IEC/IEEE 12207 — Integration & Release)

| | |
|---|---|
| วันที่มีผล | **2026-10-05** หลัง merge สาขา hardening เข้า `develop` |
| Baseline ที่ถูกแช่แข็ง | `develop` — 7 เมนู · CR-01 · CR-02 · DEF-01/02/03 · hardening สัปดาห์ที่ 11 |
| สิ้นสุด | หลังติดแท็ก `v2.0.0-evolution` บน `main` (สัปดาห์ที่ 12) |

| ❌ ห้ามทำ | ✅ อนุญาต |
|---|---|
| แตก branch เพิ่มฟีเจอร์ใหม่ | แก้ข้อบกพร่องวิกฤตที่พบจาก UAT/การทดสอบ |
| ปรับหน้าตา UI เพื่อความสวยงาม | อุดช่องโหว่ตามรายงาน Bandit / Flake8 |
| รับ Change Request ใหม่ (ให้ลง Future Backlog v3.0) | เพิ่ม Unit Test เพื่อยกระดับ coverage |

ส่งต่อสถานะความเสถียรของโค้ดให้ PM ใช้ทำ [Scope Freeze Agreement](Scope_Freeze_Agreement.md) (ENGSE202)

---

## 9. วิธีตรวจสอบซ้ำ

```bash
pip install -r requirements-dev.txt
flake8 . --count --statistics                                    # ต้องได้ 0
bandit -r . -x ./test_app.py,./test_app_v2.py,./test_hardening.py  # No issues identified
pytest -v --cov=app_v2 --cov-report=term-missing                 # 167 passed, 99%
radon cc -s -a app_v2.py                                          # max = B (6)
```
