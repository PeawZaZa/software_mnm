# รายงานนำเสนอผลงาน สัปดาห์ที่ 9–10
## Inventory System · ENGSE225 (Software Construction) + ENGSE202 (Project Management)

| | |
|---|---|
| ทีม | Billing System Dev (Jira project `SAM1`) |
| Repository | [`PeawZaZa/software_mnm`](https://github.com/PeawZaZa/software_mnm) |
| ช่วงเวลาที่รายงาน | สัปดาห์ที่ 9–10 |
| วันที่นำเสนอ | 2026-09-07 |

| # | ชื่อ | ตำแหน่ง |
|---|---|---|
| 1 | ปวริศ คูณศรี | Project Manager |
| 2 | พนาวุฒน์ อภิปสันติ | Tech Lead |
| 3 | ตรัยรัตน์ วงษ์สิทธิ์ | QA / Tester |
| 4 | ทวีชัย ทิใจ | Developer |

---

## 1. สรุปผลงานในหน้าเดียว

| ตัวชี้วัด | ก่อนสัปดาห์ที่ 9 | ปัจจุบัน |
|---|---|---|
| สถาปัตยกรรมโค้ด | ฟังก์ชันล้วน `load()/save()/main()` | **5 คลาสแยกตามชั้นความรับผิดชอบ** |
| จำนวน Unit Test | 37 | **148** (+300%) |
| ผลการทดสอบ | ผ่าน 100% | **ผ่าน 100%** |
| ฟีเจอร์ | 5 เมนู | **7 เมนู** (+Reorder List, +Export CSV) |
| Release tag | ไม่มี | **v2.0** และ **v2.1** |
| Jira Sprint 2 | ค้าง 11 งาน | **ปิดครบ 19 งาน** |
| ข้อบกพร่องที่ค้นพบและแก้ | — | **3 รายการ** (High 1 · Medium 2) |
| เอกสารบริหารโครงการ | — | **7 ฉบับ** |

**ประโยคสรุป:** ปิดหนี้ทางเทคนิคที่ค้างจาก Sprint 2 ให้จบก่อน แล้วจึงรับคำขอเปลี่ยนแปลง
2 รายการเข้ามาพัฒนาแบบ TDD พร้อมทำ Bug Bashing และจัดทำเอกสารกระบวนการครบทุกฉบับ

---

## 2. สัปดาห์ที่ 9 — ปิด Sprint 2 และพัฒนา CR-01

### 2.1 ปัญหาที่พบตอนเริ่มงาน

โจทย์สัปดาห์ที่ 9 กำหนดให้ *"เพิ่ม Attributes ใน `Product` และเมธอดใน `InventoryService`"*
แต่ตรวจสอบโค้ดจริงแล้วพบว่า **คลาสทั้งสองยังไม่มีอยู่เลย** — `app_v2.py` ยังเป็นโค้ดแบบฟังก์ชัน
ที่ตรรกะทุกอย่างรวมอยู่ใน `main()` ยาว 130 บรรทัด

> **การตัดสินใจของทีม:** ต้องเคลียร์งาน Sprint 2 (SAM1-28…43) ที่ค้างอยู่ให้เสร็จก่อน
> จึงจะทำ CR-01 ได้ ไม่สามารถลัดขั้นตอนได้

### 2.2 Sprint 2 — Refactor เป็น Class-Based

แยกความรับผิดชอบเป็น 4 ชั้น แต่ละชั้นรู้จักเฉพาะชั้นที่อยู่ถัดลงไป

```
   ผู้ใช้
     │
     ▼
┌─────────────┐  รับ input / พิมพ์ผล เท่านั้น
│  ConsoleUI  │  ไม่มี business logic
└──────┬──────┘
       ▼
┌──────────────────┐  กฎธุรกิจทั้งหมด
│ InventoryService │  ไม่ยุ่งกับไฟล์และหน้าจอ
└──────┬───────────┘
       ▼
┌─────────────────────┐  อ่าน/เขียนไฟล์อย่างเดียว
│ InventoryRepository │  atomic write ผ่าน .tmp
└──────┬──────────────┘
       ▼
┌───────────┐        ┌───────────┐
│  Product  │◄──────►│ data.json │
└───────────┘        └───────────┘
```

| Jira | งาน | หลักฐาน |
|---|---|---|
| SAM1-28 / 29 | `Product` dataclass + `to_dict()` / `from_dict()` | commit `dff022f` |
| SAM1-31 / 33 | `InventoryRepository` — file I/O + atomic write | commit `3571b87` |
| SAM1-34 / 35 | `InventoryService` — business logic | commit `1250324` |
| SAM1-37 / 39 / 40 | `ConsoleUI` + integration test | commit `529eaf0` |
| SAM1-41 / 43 | อัปเดต ARCHITECTURE / CHANGELOG / README | commit `6120776` |
| SAM1-42 | Code review ก่อน merge | PR #23 |

**ผลลัพธ์:** `main()` เหลือหน้าที่เดียวคือประกอบร่าง

```python
def main():
    ConsoleUI(InventoryService(InventoryRepository(db))).run()
```

**จุดที่อยากให้อาจารย์สังเกต** — ระหว่าง refactor ทั้งไฟล์ **regression suite เดิม 37 เคส
ไม่แดงแม้แต่ครั้งเดียว** ทำได้โดยคง `load()` / `save()` / `LOW_STOCK` ระดับโมดูลไว้เป็น
thin wrapper ที่ delegate ให้คลาสใหม่ ทำให้มีตาข่ายนิรภัยตลอดการรื้อโค้ด

### 2.3 CR-01 — Barcode และ Reorder Point

พัฒนาแบบ TDD ทุกขั้นตอน: เขียนเทสต์ให้แดงก่อน → เขียนโค้ดให้เขียว → commit

```python
@dataclass
class Product:
    ...
    barcode: str = ""       # [CR-01]
    reorder_point: int = 0  # [CR-01]
```

| เมธอดใหม่ใน `InventoryService` | หน้าที่ |
|---|---|
| `find_by_barcode(barcode)` | ค้นสินค้าจากบาร์โค้ด (บาร์โค้ดว่างไม่นับว่าตรงกัน) |
| `get_reorder_list()` | สินค้าที่ `qty <= reorder_point` — **เกณฑ์รายชิ้น** แยกจาก `LOW_STOCK` ที่เป็นเกณฑ์รวม |

เพิ่มเมนู **6. Reorder List** · หลักฐาน: PR #24, commit `74367ea`

**ประเด็นทางเทคนิคที่ภูมิใจ** — `to_dict()` เขียน key ย่อ `b` / `r` ต่อท้ายรูปแบบเดิม
และ `from_dict()` เติมค่า default เมื่อ key หาย ทำให้ **`data.json` ของเดิมใช้ต่อได้ทันที
โดยไม่ต้องเขียนสคริปต์ migrate เลย** — มี unit test คุมข้อนี้โดยเฉพาะ

---

## 3. สัปดาห์ที่ 10 — Bug Bashing และ CR-02

### 3.1 Bug Bashing — ทดสอบ 5 เคส พบข้อบกพร่องจริง 3 รายการ

| Case | สิ่งที่ทดลอง | ผล | ความรุนแรง |
|---|---|---|---|
| A | ป้อน barcode ซ้ำกับสินค้าอื่น | ❌ ระบบยอมรับทั้งคู่ | Medium |
| B1 | ป้อน Reorder Point เป็นตัวอักษร | ✅ **ดักได้ปกติ — ไม่ใช่บั๊ก** | — |
| B2 | ป้อน Reorder Point ติดลบ | ❌ บันทึกได้แล้วถูกละเลยเงียบ ๆ | Medium |
| C1/C2 | ลบ key `n` / `q` ใน `data.json` | ⚠️ ไม่ crash แต่เติม default เงียบ ๆ | Low |
| C3 | ค่าที่แปลงเป็นตัวเลขไม่ได้ (`"q": "abc"`) | 💥 **โปรแกรมตายตั้งแต่เปิด** | **High** |

> ทีมเลือก**บันทึกผลตามจริง** รวมถึงเคสที่ทดสอบแล้วผ่าน (B1) เพื่อให้ Defect Log
> สะท้อนสิ่งที่เกิดขึ้นจริง ไม่ใช่รายงานเฉพาะสิ่งที่เจอ

### 3.2 ข้อบกพร่องที่รุนแรงที่สุด — DEF-03

```
File "app_v2.py", line 39, in from_dict
    qty=int(data.get("q", 0)),
ValueError: invalid literal for int() with base 10: 'abc'
```

**สาเหตุ:** `InventoryRepository.load()` ครอบ `try/except` แค่ตอน parse JSON
แต่ไม่ได้ครอบตอนแปลงเป็น `Product` รายแถว

**ผลกระทบ:** ข้อมูลเสียเพียง **1 แถว** ทำให้ใช้ระบบไม่ได้ **ทั้งระบบ** ผู้ใช้ทั่วไปแก้เองไม่ได้

**หลังแก้:**

```
Warning: skipping corrupted row 'BAD' in data.json.
ID: GOOD | Name: Fine | Stock: 5 | Price: 2.0 THB | Type: T
Total product types: 1        ← เปิดโปรแกรมได้ตามปกติ
```

### 3.3 กระบวนการแก้บั๊กที่ใช้

```
ยิงทดสอบเจอบั๊ก
   → เปิด GitHub Issue พร้อม Steps to Reproduce (#20 #21 #22)
   → เขียน failing test ก่อน (RED)
   → แก้โค้ดจนเทสต์เขียว (GREEN)
   → commit อ้างเลข issue: "fix: ... (fixes #20)"
   → รัน full regression → merge → ปิด issue
```

| GitHub Issue | บั๊ก | จุดที่แก้ | เทสต์ที่เพิ่ม |
|---|---|---|---|
| [#22](https://github.com/PeawZaZa/software_mnm/issues/22) | ข้อมูลเสียแถวเดียวทำระบบล่ม | `InventoryRepository.load()` | 4 |
| [#20](https://github.com/PeawZaZa/software_mnm/issues/20) | barcode ซ้ำได้ | `InventoryService._barcode_owner()` | 5 |
| [#21](https://github.com/PeawZaZa/software_mnm/issues/21) | reorder point ติดลบ | `InventoryService.validate()` | 4 |

### 3.4 CR-02 — Export รายงานเป็น CSV

ผ่านกระบวนการ Change Control เต็มรูปแบบ: ยื่นคำขอ → ประเมินผลกระทบ → เข้าที่ประชุม CCB → อนุมัติ **4.5 Man-Hours**

**ผลการประเมินผลกระทบ**

| ส่วนของระบบ | ผลกระทบ |
|---|---|
| `CsvReportExporter` (คลาสใหม่) | เพิ่มใหม่ ~18 บรรทัด ใช้ `csv` จาก stdlib **ไม่ต้องลงไลบรารีเพิ่ม** |
| `ConsoleUI` | ต่ำ — เพิ่มเมนู 7 + `handle_export()` |
| `InventoryService` / `Repository` / `Product` | **ไม่กระทบเลย** |

> Tech Lead ตั้งข้อสังเกตในที่ประชุม CCB ว่า **CR นี้ไม่ต้องแตะ business logic เลย
> เป็นผลโดยตรงจากการ refactor แยกชั้นในสัปดาห์ที่ 9** — ถ้ายังเป็นโค้ดแบบเดิม
> ที่ตรรกะรวมอยู่ใน `main()` จะใช้เวลาเพิ่มอีกอย่างน้อย 2 ชั่วโมงและเสี่ยงพังของเดิม

**3 ปัญหาคลาสสิกของ CSV บน Windows ที่ดักไว้ด้วย unit test**

| ปัญหา | วิธีแก้ | เทสต์ที่ตรวจ |
|---|---|---|
| Excel อ่านภาษาไทยเป็นตัวต่างดาว | `encoding="utf-8-sig"` (ใส่ BOM) | ตรวจ 3 ไบต์แรกเป็น `EF BB BF` |
| มีบรรทัดว่างคั่นทุกแถว | `newline=""` | ตรวจว่าไม่มี `\r\n\r\n` |
| ชื่อสินค้ามีลูกน้ำทำคอลัมน์เลื่อน | `csv.writer` ครอบ quote เอง | อ่านกลับต้องได้ `"Snack, Large"` เป็นฟิลด์เดียว |

ผลการทดสอบจริง:

```csv
id,name,qty,price,category,barcode,reorder_point
101,Mama Noodles,50,6.0,Food,,0
P1,"มาม่าต้มยำ, ห่อใหญ่",4,6.0,อาหาร,8850001,5
```

---

## 4. หลักฐานการทำงาน

### 4.1 Git — 4 Pull Request merged เข้า `develop` ตามลำดับ

| PR | เรื่อง | Tests หลัง merge |
|---|---|---|
| [#23](https://github.com/PeawZaZa/software_mnm/pull/23) | Sprint 2 class-based architecture | 104 |
| [#24](https://github.com/PeawZaZa/software_mnm/pull/24) | CR-01 barcode + reorder point | 123 |
| [#25](https://github.com/PeawZaZa/software_mnm/pull/25) | CR-02 CSV export + เอกสาร ENGSE202 | 135 |
| [#26](https://github.com/PeawZaZa/software_mnm/pull/26) | แก้บั๊กจาก Bug Bashing | **148** |

```
*   Merge PR #26  fix/bug-bashing
|\
| * fix: reject duplicate barcode, negative reorder point, corrupt rows
* |   Merge PR #25  feature/cr02-csv-export
|\|
| * docs: add ENGSE202 project management documents
| * feat(dev): add CsvReportExporter and Export CSV menu [CR-02]
* |   Merge PR #24  feature/cr01-barcode-reorder-point
|\|
| * feat(dev): add barcode and reorder point [CR-01]
* |   Merge PR #23  feature/sprint2-class-refactor
|\|
| * docs: renumber Sprint 1 as v1.1 and Sprint 2 as v2.0 [SAM1-43]
| * feat(dev): extract ConsoleUI and slim main() [SAM1-37]
| * feat(dev): extract InventoryService [SAM1-34]
| * feat(dev): extract InventoryRepository [SAM1-31]
| * feat(dev): add Product dataclass [SAM1-28]
```

Release tag: **`v2.0`** (Sprint 2 class-based) และ **`v2.1`** (CR-01, CR-02, bug fixes)

### 4.2 ผลการทดสอบ

```
test_app.py      37 passed   ← regression suite ของ Sprint 1 (ไม่ต้องแก้เลยตลอด 2 สัปดาห์)
test_app_v2.py  111 passed   ← คลาสทั้ง 5 + CR-01 + CR-02 + bug fixes + integration
─────────────────────────
รวม            148 passed
```

**ทดสอบการรันจริงเพิ่มเติม (ไม่ใช่แค่ unit test)**

| # | ทดสอบ | ผล |
|---|---|---|
| 1 | ไม่มี `data.json` → โหลด default 3 รายการ | ✅ |
| 2 | `data.json` เป็น JSON เสีย → เตือนแล้วโหลด default | ✅ |
| 3 | `data.json` รูปแบบเดิม (ไม่มี key `b`/`r`) → อ่านได้ | ✅ |
| 4 | เพิ่มสินค้า → ตัดสต๊อก → ดูสรุป → เปิดใหม่ ข้อมูลตรง | ✅ |
| 5 | Export CSV ชื่อภาษาไทยที่มีลูกน้ำ → เปิดกลับอ่านได้ครบ | ✅ |
| 6 | เขียน CSV ไปยัง path ที่ไม่มีอยู่ → แจ้ง error ไม่ crash | ✅ |

---

## 5. งานฝั่งบริหารโครงการ (ENGSE202)

### 5.1 EVM Analysis ของ Sprint 1

ใช้วันตัดข้อมูล 2026-07-13 ซึ่งเป็นวันสิ้นสุด Sprint 1 ตามแผน

| ตัวชี้วัด | ค่า | แปลผล |
|---|---|---|
| งานที่เสร็จทันกำหนด | 4 / 16 ใบ (25%) | 🔴 |
| **SV** (Schedule Variance) | −14,400 บาท | 🔴 ล่าช้ากว่าแผนมาก |
| **CV** (Cost Variance) | −2,400 บาท | 🔴 ใช้ต้นทุนเกินงาน |
| **SPI** | 0.25 | 🔴 ทำได้แค่ 1/4 ของแผน |
| **CPI** | 0.67 | 🔴 จ่าย 1 บาท ได้งาน 0.67 บาท |

**ข้อสังเกตเชิงวิชาการที่ทีมเจอเอง** — พอ Sprint เสร็จครบ **SV กลับเป็น 0 และ SPI กลับเป็น 1.00**
ทั้งที่ความจริงส่งงานช้าไป 3 สัปดาห์ นี่คือข้อจำกัดที่รู้จักกันของ EVM ที่ตัวชี้วัด
ด้านกำหนดการจะบอดตอนใกล้จบโครงการ จึงต้องดูควบคู่กับวันส่งมอบจริงและ Burndown Chart เสมอ

### 5.2 Sprint 1 Retrospective — ประเด็นที่มีหลักฐานรองรับ

| ประเด็น | หลักฐานจาก git |
|---|---|
| 😡 งานกองที่ 2 วันสุดท้าย | PR 10 จาก 11 ใบ merge ในวันที่ 2026-07-12 และ 07-13 |
| 😡 งานต้องทำซ้ำ 3 รอบ | PR #14 merge → revert (#15) → merge ใหม่ (#19) |
| 😡 ภาระงานไม่สมดุล | PM 51 commit (60%) · คนอื่นรวมกัน 30 commit |
| 😢 DoD มีแต่ไม่ถูกบังคับใช้ | SAM1-38 ระบุ "PyTest 100%" แต่ PR #14 merge ทั้งที่เทสต์ไม่ผ่าน |
| 😄 เทสต์คุมพฤติกรรมก่อน refactor | `test_app.py` ทำให้รื้อโค้ดทั้งไฟล์ได้โดยไม่พัง |
| 😄 แยก branch ตาม role | `feature/tl/...`, `feature/dev/...`, `feature/qa/...` ตามงานได้ง่าย |

### 5.3 เอกสารที่จัดทำ 7 ฉบับ (โฟลเดอร์ `docs/`)

| ไฟล์ | เนื้อหา |
|---|---|
| `Sprint1_Retrospective.md` | Mad / Sad / Glad + Action Items 7 ข้อ |
| `EVM_Analysis.md` | SV, CV, SPI, CPI, EAC, VAC + บทวิเคราะห์สาเหตุ |
| `Defect_Log.md` | ข้อบกพร่อง 4 รายการ พร้อม Steps to Reproduce และผลหลังแก้ |
| `CR-02_Impact_and_Decision_Form.md` | Technical Impact + ทางเลือก 3 แบบ + ประมาณการ 4.5 Man-Hours |
| `CCB_Meeting_Minutes.md` | บันทึกประชุม 3 วาระ + มติและผู้รับผิดชอบ |
| `Contingency_Reserve_Log.md` | เบิกกันชนไป 7.0 จาก 12.0 ชม. (58.3%) + ข้อเสนอแนะ |
| `JIRA_SETUP.md` | ขั้นตอนตั้งค่า Sprint บน Jira |

---

## 6. ปัญหาที่พบระหว่างทำงานและวิธีจัดการ

| ปัญหา | วิธีจัดการ |
|---|---|
| คลาส `Product` / `InventoryService` ที่โจทย์อ้างถึงยังไม่มีจริง | เคลียร์ Sprint 2 ที่ค้างให้จบก่อน แล้วจึงทำ CR-01 |
| เลขเวอร์ชันชนกัน — `CHANGELOG` ใช้ v2.0 กับ Sprint 1 ไปแล้ว | เลื่อน Sprint 1 เป็น v1.1 แล้วให้ Sprint 2 เป็น v2.0 ตาม backlog |
| Jira project ยังไม่ได้เปิดฟีเจอร์ Sprints | เปิดใน Project settings → Features แล้วจัดงานเข้า sprint ครบ 35 ใบ |
| ชื่อสินค้าภาษาไทยเพี้ยนตอนทดสอบผ่าน pipe | ตรวจแล้วเป็นเรื่อง encoding ของ stdin บน Windows **ไม่ใช่บั๊กของโปรแกรม** |

### ⚠️ ข้อจำกัดที่ต้องรายงานตามตรง

**GitHub Actions รันไม่ได้ตลอดสองสัปดาห์นี้**

```
The job was not started because your account is locked due to a billing issue.
```

workflow `PyTest CI` ถูกตั้งค่าไว้ครบและถูกต้อง (`.github/workflows/pytest.yml`)
แต่บัญชี GitHub ถูกล็อกเรื่องการชำระเงิน job จึงไม่เคยถูกรันเลย

**การรับมือของทีม:** รัน `pytest` ในเครื่องก่อน merge **ทุก PR** และบันทึกผลไว้ใน
PR description ทุกใบ พร้อมระบุเหตุผลว่าทำไม CI ถึงไม่เขียว — ไม่ปกปิดหรือข้ามขั้นตอน

---

## 7. บทเรียนที่ได้

1. **ลงทุนกับเทสต์ก่อน refactor คุ้มเสมอ** — `test_app.py` 37 เคสที่เขียนไว้ตั้งแต่ Sprint 1
   ทำให้รื้อโค้ดทั้งไฟล์เป็น class-based ได้อย่างมั่นใจ โดยไม่แดงแม้แต่ครั้งเดียว

2. **สถาปัตยกรรมที่ดีวัดผลได้เป็นตัวเลข** — CR-02 ใช้เวลา 4.5 ชม. แทนที่จะเป็น 6.5+ ชม.
   เพราะไม่ต้องแตะ business logic เลย นี่คือผลตอบแทนของการ refactor ที่จับต้องได้

3. **บั๊กที่อันตรายที่สุดคือบั๊กที่เงียบ** — DEF-02 (reorder point ติดลบ) ไม่มี error ใด ๆ
   ระบบตอบ `Done.` ตามปกติ แต่สินค้านั้นจะไม่มีวันขึ้นรายการสั่งซื้อ อันตรายกว่าบั๊กที่ crash เสียอีก

4. **กระบวนการที่ไม่มีกลไกบังคับ = ไม่มีกระบวนการ** — DoD เขียนว่า "PyTest 100%"
   แต่ PR #14 ยัง merge ผ่านได้เพราะไม่มี Branch Protection บังคับ

5. **EVM ต้องอ่านคู่กับ Burndown** — SPI ที่กลับมาเป็น 1.00 ตอนจบ sprint
   ไม่ได้แปลว่าโครงการตรงเวลา

---

## 8. แผนงานถัดไป

| # | สิ่งที่จะทำ | แก้ปัญหาอะไร |
|---|---|---|
| 1 | ตั้ง Branch Protection บน `develop` ให้ `PyTest CI` ต้องเขียวก่อน merge | DoD ไม่ถูกบังคับใช้ · PR ที่ต้อง revert |
| 2 | เคลียร์ปัญหา billing เพื่อให้ GitHub Actions กลับมาทำงาน | CI ไม่เคยรัน |
| 3 | เพิ่มคำเตือนเมื่ออ่านแถวที่ฟิลด์หายไป (DEF-04) | ข้อมูลหายแบบเงียบ |
| 4 | จำกัด Work In Progress ไม่เกิน 2 ใบต่อคน + Daily Standup | งานกองปลาย sprint |
| 5 | บันทึกชั่วโมงทำงานจริงลง Jira Time Tracking | ค่า AC ใน EVM ยังเป็นค่าประมาณ |

---

## ภาคผนวก — วิธีตรวจสอบผลงาน

```bash
git clone git@github.com:PeawZaZa/software_mnm.git
cd software_mnm
git checkout develop
pip install pytest

pytest -v          # ต้องได้ 148 passed
python app_v2.py   # เมนู 1–7 ใช้งานได้จริง
```

| หลักฐาน | ที่อยู่ |
|---|---|
| Pull Requests | [PR #23–#26](https://github.com/PeawZaZa/software_mnm/pulls?q=is%3Apr+is%3Amerged) |
| GitHub Issues (Bug Bashing) | [#20, #21, #22](https://github.com/PeawZaZa/software_mnm/issues?q=is%3Aissue+label%3Abug) |
| Release tags | `v2.0`, `v2.1` |
| Jira board | `SAM1` — Sprint 1 (16 ใบ) · Sprint 2 (19 ใบ) |
| เอกสารบริหารโครงการ | โฟลเดอร์ [`docs/`](.) |
