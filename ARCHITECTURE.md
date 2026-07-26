# System Architecture Document
## Inventory System v2.0

| # | ชื่อ | ตำแหน่ง |
|---|---|---|
| 1 | ปวริศ คูณศรี | Project Manager |
| 2 | พนาวุฒน์ อภิปสันติ| Tech Lead |
| 3 | ตรัยรัตน์ วงษ์สิทธิ์ | QA / Tester |
| 4 | ทวีชัย ทิใจ | Developer |

---

## 1. ภาพรวมระบบ

ระบบ CLI จัดการคลังสินค้าเบื้องต้น รันผ่าน Terminal รับ input จากผู้ใช้และเก็บข้อมูลในไฟล์ JSON

```
User → main() → inventory (dict) → save() → data.json
                      ↑
                   load() ← data.json (ตอนเริ่มโปรแกรม)
```

---

## 2. โครงสร้างฟังก์ชัน (v2.0)

| ฟังก์ชัน | หน้าที่ | Parameter | Return |
|---|---|---|---|
| `load(inventory)` | อ่านข้อมูลจาก `data.json` เข้า dict | `inventory: dict` | None |
| `save(inventory)` | เขียน dict ลงไฟล์แบบ atomic | `inventory: dict` | None |
| `main()` | event loop + menu routing | — | None |

---

## 3. Data Structure

```python
inventory = {
    "101": {
        "n": str,    # ชื่อสินค้า
        "q": int,    # จำนวนคงเหลือ
        "p": float,  # ราคาต่อหน่วย (THB)
        "c": str     # หมวดหมู่
    }
}
```

**ค่าคงที่:**
```python
LOW_STOCK = 10   # เกณฑ์แจ้งเตือนสต๊อกต่ำ (ใช้ร่วมกันทั้งเมนู 3 และ 4)
db = "data.json" # path ของไฟล์ฐานข้อมูล
```

---

## 4. Data Flow (v2.0)

```
เริ่มโปรแกรม
    └── main()
         └── load(inventory)
              ├── มีไฟล์ → json.load() → inventory.update()
              └── ไม่มีไฟล์ / เสียหาย → default data → inventory.update()

เมนู 1 (Show All)
    └── อ่าน inventory → print (ไม่แก้ไข)

เมนู 2 (Add/Update)
    └── รับ input → validate (try/except) → inventory[id] = {...} → save(inventory)

เมนู 3 (Stock Out)
    └── รับ input → validate amt > 0 → inventory[id]['q'] -= amt → save(inventory)
         └── if q < LOW_STOCK → WARNING

เมนู 4 (Inventory Summary)
    └── วนลูป inventory → คำนวณ total_val, low_stock_list (q < LOW_STOCK) → print

save(inventory)
    └── เขียนลง data.json.tmp → os.replace() → data.json
```

---

## 5. การเปลี่ยนแปลงจาก v1.0 → v2.0

| จุด | v1.0 | v2.0 |
|---|---|---|
| State management | `global x` | `inventory` dict ส่งผ่าน parameter |
| Input validation | ไม่มี | `try/except ValueError` ทุกจุด |
| Negative stock cut | ผ่านได้ | ตรวจ `amt <= 0` ก่อน |
| File write | เขียนทับตรง | Atomic write ผ่าน `.tmp` |
| File read error | crash | `try/except` → โหลด default |
| Low stock threshold | เมนู 3 ใช้ 5, เมนู 4 ใช้ 10 | `LOW_STOCK = 10` ทั้งคู่ |
| เมนู 4 ชื่อ | "Check Check" | "Inventory Summary" |

---

## 6. ข้อจำกัดที่ยังมีอยู่ (Known Limitations)

- ไม่มี Authentication / Authorization
- ไม่มีฐานข้อมูลจริง (ใช้ JSON file แทน)
- ไม่รองรับ concurrent access (ใช้คนเดียวได้)
- ไม่มี GUI — เป็น CLI เท่านั้น
