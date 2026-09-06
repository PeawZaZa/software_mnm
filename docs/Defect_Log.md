# Defect Log — Bug Bashing Session
## Inventory System v2.1 · ENGSE225 / ENGSE202

| รายการ | ค่า |
|---|---|
| วันที่ทำ Bug Bashing | 2026-09-07 |
| เวอร์ชันที่ทดสอบ | v2.1 (หลัง CR-01, ก่อนแก้บั๊ก) |
| commit ที่ทดสอบ | `74367ea` (CR-01) |
| ผู้ทดสอบ | ตรัยรัตน์ วงษ์สิทธิ์ (QA) |
| วิธีทดสอบ | Exploratory testing ตามเคสที่กำหนดในใบงาน + ตรวจสถานะภายในด้วยสคริปต์ |

---

## สรุปผล

ยิงทดสอบ **5 เคส** พบข้อบกพร่องจริง **3 รายการ** (High 1 · Medium 2) และ **1 เคสผ่าน**

| ID | เคส | ผล | ความรุนแรง | สถานะ |
|---|---|---|---|---|
| DEF-01 | Barcode ซ้ำกับสินค้าอื่น | ❌ พบข้อบกพร่อง | Medium | ✅ แก้แล้ว [#20](https://github.com/PeawZaZa/software_mnm/issues/20) |
| DEF-02 | Reorder Point ติดลบ | ❌ พบข้อบกพร่อง | Medium | ✅ แก้แล้ว [#21](https://github.com/PeawZaZa/software_mnm/issues/21) |
| DEF-03 | ค่าใน `data.json` แปลงเป็นตัวเลขไม่ได้ | ❌ พบข้อบกพร่อง | **High** | ✅ แก้แล้ว [#22](https://github.com/PeawZaZa/software_mnm/issues/22) |
| DEF-04 | ลบฟิลด์ใน `data.json` | ⚠️ ทำงานได้แต่ผลเงียบผิด | Low | 📌 รับทราบ ยกไป sprint ถัดไป |
| — | Reorder Point เป็นตัวอักษร | ✅ ผ่าน ไม่พบข้อบกพร่อง | — | — |

> ทุกรายการแก้เสร็จและปิด issue แล้วใน commit เดียวกัน — ชุดทดสอบเพิ่มจาก 135 เป็น **148 tests**

---

## DEF-01 — ระบบยอมให้สินค้าคนละตัวใช้ barcode เดียวกัน

| | |
|---|---|
| ความรุนแรง | **Medium** |
| GitHub Issue | [#20](https://github.com/PeawZaZa/software_mnm/issues/20) |
| เคสในใบงาน | Case A |
| ส่วนที่เกี่ยวข้อง | `InventoryService.add_update()`, `InventoryService.find_by_barcode()` |

**Steps to Reproduce**

1. เปิดโปรแกรม เลือกเมนู `2` เพิ่มสินค้า `A1` / ชื่อ `Item A` / barcode `8850001`
2. เลือกเมนู `2` อีกครั้ง เพิ่มสินค้า `A2` / ชื่อ `Item B` / barcode `8850001` (ซ้ำ)

**Expected** — ระบบต้องปฏิเสธ พร้อมแจ้งว่าบาร์โค้ดนี้ถูกใช้กับสินค้าอื่นแล้ว

**Actual** — ระบบตอบ `Done.` ทั้งสองครั้ง บันทึกลง `data.json` ทั้งคู่

```
products sharing barcode 8850001: ['A1', 'A2']
find_by_barcode returns: A1
```

**Impact** — `find_by_barcode()` วนลูปเจอตัวแรกแล้ว `return` ทันที สินค้า `A2`
จึงค้นด้วยบาร์โค้ดไม่เจอตลอดไป ถ้าเอาไปต่อกับเครื่องยิงบาร์โค้ดจริงจะตัดสต๊อกผิดตัว

---

## DEF-02 — Reorder Point ติดลบถูกบันทึกและถูกละเลยเงียบๆ

| | |
|---|---|
| ความรุนแรง | **Medium** |
| GitHub Issue | [#21](https://github.com/PeawZaZa/software_mnm/issues/21) |
| เคสในใบงาน | Case B (ส่วนค่าติดลบ) |
| ส่วนที่เกี่ยวข้อง | `InventoryService.validate()`, `InventoryService.get_reorder_list()` |

**Steps to Reproduce**

1. เมนู `2` เพิ่มสินค้า `B2` / qty `2` / **Reorder Point `-5`**
2. เมนู `6` ดู Reorder List

**Expected** — ปฏิเสธตั้งแต่ตอนกรอก เพราะจุดสั่งซื้อซ้ำติดลบไม่มีความหมายทางธุรกิจ

**Actual**

```
Done.
No product has reached its reorder point.
stored reorder_point: -5
appears in reorder list: []
```

**Impact** — `validate()` ตรวจแค่ `qty` กับ `price` ไม่ได้ตรวจ `reorder_point`
และ `get_reorder_list()` กรองด้วย `reorder_point > 0` สินค้าที่ตั้งค่าติดลบ
จึง**ไม่มีวันขึ้นรายการสั่งซื้อ** ทั้งที่ผู้ใช้เข้าใจว่าตั้งค่าไว้แล้ว — ล้มเหลวแบบเงียบ

---

## DEF-03 — โปรแกรมตายตั้งแต่เปิด เมื่อข้อมูลในไฟล์แปลงเป็นตัวเลขไม่ได้ 🔴

| | |
|---|---|
| ความรุนแรง | **High** |
| GitHub Issue | [#22](https://github.com/PeawZaZa/software_mnm/issues/22) |
| เคสในใบงาน | Case C (ต่อยอด) |
| ส่วนที่เกี่ยวข้อง | `Product.from_dict()`, `InventoryRepository.load()` |

**Steps to Reproduce**

1. แก้ `data.json` ให้แถวใดแถวหนึ่งเป็น `{"n": "Broken", "q": "abc", "p": 10.0, "c": "Food"}`
2. รัน `python app_v2.py`

**Expected** — ข้ามหรือซ่อมแถวที่เสีย แจ้งเตือน แล้วเปิดโปรแกรมต่อได้

**Actual** — โปรแกรมตายทันที เข้าเมนูไม่ได้เลย

```
File "app_v2.py", line 39, in from_dict
    qty=int(data.get("q", 0)),
ValueError: invalid literal for int() with base 10: 'abc'
```

**Impact** — รุนแรงที่สุดในชุดนี้ ข้อมูลเสียแค่ **แถวเดียว** ทำให้ใช้ระบบไม่ได้ทั้งระบบ
`load()` มี `try/except` ครอบแค่ตอน parse JSON ไม่ได้ครอบตอนแปลงเป็น `Product` รายแถว
ผู้ใช้ทั่วไปแก้เองไม่ได้เพราะต้องไปไล่แก้ JSON ด้วยมือ

---

## DEF-04 — ฟิลด์ที่หายไปถูกเติมค่า default เงียบๆ

| | |
|---|---|
| ความรุนแรง | **Low** (พฤติกรรมตามที่ออกแบบไว้ แต่ควรแจ้งผู้ใช้) |
| GitHub Issue | *(ไม่เปิด — บันทึกไว้เป็นข้อสังเกต)* |
| เคสในใบงาน | Case C |

**ผลการทดลอง**

| ลบ key | ผล | สิ่งที่ผู้ใช้เห็น |
|---|---|---|
| `n` (ชื่อ) | ไม่ crash | `ID: C1 \| Name:  \| Stock: 5` — ชื่อว่างเปล่า |
| `q` (จำนวน) | ไม่ crash | `Stock: 0` และมูลค่ารวม `0.0 THB` เหมือนของหมด |

**บทวิเคราะห์** — `from_dict()` ตั้งใจเติม default เพื่อไม่ให้ `KeyError` ล้มทั้งระบบ
ซึ่งถูกต้องในแง่ความทนทาน แต่**ไม่มีการแจ้งเตือนเลย** ผู้ใช้จึงแยกไม่ออกว่า
"ของหมดจริง" กับ "ข้อมูลหาย" ทีมรับทราบและเสนอให้เพิ่มคำเตือนใน sprint ถัดไป

---

## เคสที่ผ่าน — Reorder Point เป็นตัวอักษร

ป้อน `abc` ในช่อง Reorder Point → ระบบตอบ
`Invalid input: Reorder Point must be a number.` และไม่บันทึกสินค้า

`ConsoleUI.handle_add()` ครอบ `int()` ด้วย `try/except ValueError` ไว้ตั้งแต่ CR-01 แล้ว
**ไม่พบข้อบกพร่อง**

---

## หมายเหตุระหว่างทดสอบ (ไม่ใช่ข้อบกพร่องของระบบ)

ตอนป้อนชื่อสินค้าภาษาไทยผ่าน pipe ใน Git Bash เกิด
`UnicodeEncodeError: ... surrogates not allowed`
ตรวจแล้วเป็นเรื่องการถอดรหัส stdin ของ Windows ไม่ใช่บั๊กของโปรแกรม —
ตั้ง `PYTHONIOENCODING=utf-8` แล้วภาษาไทยทำงานถูกต้องทั้งการบันทึกและการส่งออก CSV


---

## การแก้ไข (Resolution)

แก้ทั้ง 3 รายการบน branch `fix/bug-bashing` ตามแนวทาง TDD —
เขียนเทสต์ให้แดงก่อนทุกข้อ แล้วจึงแก้โค้ดให้เขียว

| ID | Issue | สิ่งที่แก้ | เทสต์ที่เพิ่ม |
|---|---|---|---|
| DEF-01 | #20 | `InventoryService._barcode_owner()` ตรวจเจ้าของบาร์โค้ด และ `add_update()` ปฏิเสธเมื่อซ้ำ | 5 |
| DEF-02 | #21 | `validate()` รับ `reorder_point` เพิ่มและปฏิเสธค่าติดลบ | 4 |
| DEF-03 | #22 | `InventoryRepository.load()` ดัก `ValueError` รายแถว ข้ามแถวเสียพร้อมแจ้งชื่อแถว | 4 |

**ผลการตรวจสอบซ้ำในโปรแกรมจริง**

```
#20  Error: Barcode 8850001 is already used by product A1.
#21  Invalid input: Reorder Point must not be negative.
#22  Warning: skipping corrupted row 'BAD' in data.json.
     ID: GOOD | Name: Fine | Stock: 5 | Price: 2.0 THB | Type: T
     Total product types: 1        ← เปิดโปรแกรมได้ตามปกติ
```

**Regression** — ชุดทดสอบทั้งโปรเจกต์ 148 tests ผ่านครบ 100%
รวมถึง regression suite ของ Sprint 1 ทั้ง 37 เคสที่ไม่ต้องแก้เลย

**หมายเหตุการออกแบบ** — DEF-01 ยอมให้สินค้าหลายตัวมีบาร์โค้ดว่างพร้อมกันได้
และยอมให้สินค้าตัวเดิมแก้ไขโดยใช้บาร์โค้ดของตัวเองซ้ำได้ มีเทสต์คุมทั้งสองกรณี
