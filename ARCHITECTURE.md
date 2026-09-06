# System Architecture Document
## Inventory System v2.1 (Class-Based)

| # | ชื่อ | ตำแหน่ง |
|---|---|---|
| 1 | ปวริศ คูณศรี | Project Manager |
| 2 | พนาวุฒน์ อภิปสันติ| Tech Lead |
| 3 | ตรัยรัตน์ วงษ์สิทธิ์ | QA / Tester |
| 4 | ทวีชัย ทิใจ | Developer |

---

## 1. ภาพรวมระบบ

ระบบ CLI จัดการคลังสินค้า รันผ่าน Terminal เก็บข้อมูลในไฟล์ JSON

v2.1 แยกความรับผิดชอบออกเป็น 4 คลาสตามชั้น (layer) แต่ละคลาสรู้จักเฉพาะชั้นที่อยู่ถัดลงไป
ทำให้ทดสอบแยกส่วนได้ และเพิ่มฟีเจอร์ใหม่ (เช่น CR-01, CR-02) โดยไม่ต้องแตะชั้นอื่น

```
   ผู้ใช้
     │
     ▼
┌─────────────┐  input/print เท่านั้น ไม่มี business logic
│  ConsoleUI  │
└──────┬──────┘
       │ เรียก method
       ▼
┌──────────────────┐  กฎธุรกิจทั้งหมด ไม่ยุ่งกับไฟล์และหน้าจอ
│ InventoryService │
└──────┬───────────┘
       │ load() / save()
       ▼
┌─────────────────────┐  อ่าน/เขียนไฟล์อย่างเดียว
│ InventoryRepository │
└──────┬──────────────┘
       │ Product.from_dict() / to_dict()
       ▼
┌───────────┐        ┌───────────┐
│  Product  │◄──────►│ data.json │
└───────────┘        └───────────┘
```

---

## 2. โครงสร้างคลาส (v2.1)

### `Product` — dataclass [SAM1-28]

| สมาชิก | ชนิด | หมายเหตุ |
|---|---|---|
| `id` | `str` | รหัสสินค้า (ตรงกับ key ชั้นนอกของ `data.json`) |
| `name` | `str` | ชื่อสินค้า |
| `qty` | `int` | จำนวนคงเหลือ |
| `price` | `float` | ราคาต่อหน่วย (THB) |
| `category` | `str` | หมวดหมู่ |

| เมธอด | Return | หน้าที่ |
|---|---|---|
| `to_dict()` | `dict` | แปลงเป็น key ย่อ `n/q/p/c` เพื่อเขียนลงไฟล์ |
| `from_dict(product_id, data)` | `Product` | อ่านจาก key ย่อ + แปลงชนิด + เติมค่า default ให้ key ที่ขาด |

### `InventoryRepository` — persistence [SAM1-31]

| เมธอด | Return | หน้าที่ |
|---|---|---|
| `__init__(path=None)` | — | ไม่ส่ง path จะใช้ `db` ระดับโมดูล (อ่านตอนสร้าง instance) |
| `load()` | `dict[str, Product]` | ไม่มีไฟล์/ไฟล์เสีย → `DEFAULT_DATA` |
| `save(inventory)` | `None` | atomic write ผ่าน `.tmp` แล้ว `os.replace()` |

### `InventoryService` — business logic [SAM1-34]

| เมธอด | Return | หน้าที่ |
|---|---|---|
| `validate(qty, price)` | `(ok, error_msg)` | ปฏิเสธ `qty` และ `price` ที่ติดลบ |
| `add_update(id, name, qty, price, category)` | `(ok, message)` | เขียนทับเสมอ แล้ว `save()` |
| `stock_out(id, amt)` | `(ok, message)` | ปฏิเสธ `amt <= 0` และปฏิเสธเมื่อสต๊อกไม่พอ |
| `get_summary()` | `(total_items, total_val, low_stock_list)` | คำนวณมูลค่ารวมและรายชื่อสต๊อกต่ำ |

ค่าคงที่: `InventoryService.LOW_STOCK = 10` — แหล่งความจริงเดียวของเกณฑ์แจ้งเตือน

### `ConsoleUI` — presentation [SAM1-37]

| เมธอด | หน้าที่ |
|---|---|
| `__init__(service, input_fn=input, print_fn=print)` | inject I/O เพื่อให้ unit test ได้โดยไม่ต้อง monkeypatch builtins |
| `run()` | event loop + routing เมนู 1–5 |
| `handle_show()` / `handle_add()` / `handle_out()` / `handle_summary()` | หนึ่งเมธอดต่อหนึ่งเมนู |

`main()` เหลือหน้าที่เดียวคือประกอบร่าง (composition root):

```python
def main():
    ConsoleUI(InventoryService(InventoryRepository(db))).run()
```

---

## 3. Data Structure

รูปแบบไฟล์ **ไม่เปลี่ยน** จาก v1.0 — `data.json` เดิมใช้กับ v2.1 ได้ทันที ไม่ต้อง migrate

```json
{
  "101": { "n": "Mama Noodles", "q": 50, "p": 6.0, "c": "Food" }
}
```

การแปลงระหว่าง key ย่อในไฟล์ ↔ ชื่อเต็มในโค้ด อยู่ใน `Product.to_dict()` / `from_dict()` ที่เดียว

**ค่าคงที่:**

```python
db = "data.json"                    # path ของไฟล์ฐานข้อมูล (ระดับโมดูล)
InventoryService.LOW_STOCK = 10     # เกณฑ์แจ้งเตือนสต๊อกต่ำ
InventoryRepository.DEFAULT_DATA    # ข้อมูลตั้งต้น 3 รายการ
```

---

## 4. Data Flow (v2.1)

```
เริ่มโปรแกรม
    main() → InventoryRepository(db) → InventoryService → ConsoleUI.run()
                     └── load()
                          ├── มีไฟล์ → json.loads() → Product.from_dict() ต่อแถว
                          └── ไม่มีไฟล์ / JSON เสีย → DEFAULT_DATA (+ พิมพ์คำเตือน)

เมนู 1 (Show All)
    ConsoleUI.handle_show() → อ่าน service.inventory → print (ไม่แก้ไข)

เมนู 2 (Add/Update)
    handle_add() → int()/float() ดักพิมพ์ผิด [INV-6]
        → service.add_update() → validate() → เขียนทับ → repository.save()

เมนู 3 (Stock Out)
    handle_out() → int() ดักพิมพ์ผิด [INV-6]
        → service.stock_out() → ตรวจ amt > 0 [INV-7] → ตรวจสต๊อกพอ
        → หักจำนวน → repository.save() → ถ้า qty < LOW_STOCK แนบคำเตือนใน message

เมนู 4 (Inventory Summary)
    handle_summary() → service.get_summary() → print

เมนู 5 (Exit)
    print("Bye") → ออกจาก loop

repository.save(inventory)
    Product.to_dict() ทุกแถว → เขียน data.json.tmp → os.replace() → data.json [INV-11]
```

---

## 5. การเปลี่ยนแปลงแต่ละเวอร์ชัน

| จุด | v1.0 | v2.0 (Sprint 1) | v2.1 (Sprint 2) |
|---|---|---|---|
| โครงสร้าง | ฟังก์ชัน + `global x` | ฟังก์ชัน + ส่ง dict เป็น parameter | 4 คลาสแยกตามชั้น |
| ข้อมูลสินค้า | dict `{"n","q","p","c"}` | dict เหมือนเดิม | `Product` dataclass |
| I/O ไฟล์ | ปนอยู่ใน `load()/save()` | เหมือนเดิม + atomic write | `InventoryRepository` |
| Business logic | ปนอยู่ใน `main()` | ปนอยู่ใน `main()` | `InventoryService` |
| หน้าจอ / เมนู | ปนอยู่ใน `main()` | ปนอยู่ใน `main()` | `ConsoleUI` (inject I/O ได้) |
| Default data | เขียนซ้ำ 2 ที่ | เขียนซ้ำ 2 ที่ | `DEFAULT_DATA` ที่เดียว |
| ตรวจค่าติดลบตอนเพิ่มสินค้า | ไม่มี | ไม่มี | `validate()` |
| Unit tests | ไม่มี | 37 tests (`test_app.py`) | +67 tests (`test_app_v2.py`) รวม 104 |

> `load(inventory)` / `save(inventory)` / `LOW_STOCK` ระดับโมดูลยังคงอยู่ในฐานะ wrapper
> เพื่อให้ regression suite ของ Sprint 1 (`test_app.py`) ยังรันผ่านโดยไม่ต้องแก้

---

## 6. ข้อจำกัดที่ยังมีอยู่ (Known Limitations)

- ไม่มี Authentication / Authorization
- ไม่มีฐานข้อมูลจริง (ใช้ JSON file แทน)
- ไม่รองรับ concurrent access (ใช้คนเดียวได้)
- ไม่มี GUI — เป็น CLI เท่านั้น
- แถวใน `data.json` ที่มีค่าแปลงเป็นตัวเลขไม่ได้ (เช่น `"q": "abc"`) จะทำให้ `load()` โยน `ValueError`
  — ยังไม่มีการดักที่ระดับแถว (รอ Bug Bashing สัปดาห์ที่ 10)
