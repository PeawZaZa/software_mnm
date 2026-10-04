# Live Demo & Technical Defense Script
## ENGSE225 สัปดาห์ที่ 15 — Final Defense & Handover (15 นาที)

| | |
|---|---|
| ผู้สาธิต | พนาวุฒน์ อภิปสันติ (Tech Lead) · ผู้ช่วย ทวีชัย ทิใจ (Dev) |
| ซ้อมจริงแล้ว | 2026-10-05 บนโฟลเดอร์ใหม่ — ติดตั้ง 21 วิ · 195 passed · edge cases ผ่าน ([log](evidence/rehearsal_log.txt)) |
| เวอร์ชันที่สาธิต | แท็กล่าสุดบน `main` (`v2.0.1-evolution` — ถ้ายังไม่ได้ push ให้ใช้ `develop`) |

**ก่อนขึ้นเวที:** เครื่องที่ไม่ใช่เครื่องพัฒนา · Python ≥ 3.10 · Excel · ขยายฟอนต์ Terminal · ปิดแจ้งเตือน

---

## ขั้นที่ 1 — Clean Install สด (3 นาที · เกณฑ์ ≤ 2 นาที)

```bash
mkdir defense && cd defense
git clone https://github.com/PeawZaZa/software_mnm.git
cd software_mnm
git checkout v2.0.1-evolution
./setup.sh                      # PowerShell: powershell -ExecutionPolicy Bypass -File setup.ps1
```

**พูด:** "ไม่มี dependency ภายนอก · สคริปต์สร้าง virtual environment ใหม่ · คัดลอก `.env` · รัน smoke test ให้เอง
ซ้อมแล้ว 21 วินาที" → ชี้ `[2/5] Virtual environment: .venv` ว่าเป็น venv ใหม่

## ขั้นที่ 2 — PyTest สด (3 นาที)

```bash
source .venv/Scripts/activate   # macOS/Linux: source .venv/bin/activate
pytest -v --cov=app_v2 --cov-report=term-missing
```

**พูด:** "195 เคสใน 5 ไฟล์ · coverage 99% · บรรทัดเดียวที่ไม่ครอบคือ `if __name__ == '__main__'`"
ถ้ากรรมการถามรายคลาส → ทุกคลาส 100% (บรรทัดที่ขาดอยู่นอกคลาส)

## ขั้นที่ 3 — สาธิตฟังก์ชันหลัก (5 นาที)

```bash
python app_v2.py
```

| # | ปุ่ม | สิ่งที่โชว์ |
|---|---|---|
| 1 | `2` → `P999` · `Fresh Milk` · `10` · `25` · `Dairy` · `885999001` · `5` | เพิ่มสินค้าพร้อมบาร์โค้ดและจุดสั่งซื้อ → `Done.` |
| 2 | `3` → `P999` · `6` | `!!! REORDER POINT REACHED: 4 left (reorder point 5) !!!` |
| 3 | `6` | รายการต้องสั่งซื้อมี Fresh Milk |
| 4 | `7` → `low_stock.csv` | `Exported ... to exports\low_stock.csv` → **เปิดใน Excel** ชี้คอลัมน์ `barcode` · `qty` |
| 5 | `5` ออก → ลบตัวอักษรท้ายไฟล์ `data/inventory_db.json` → `python app_v2.py` → `1` | `Restored data from backup inventory_db.json.bak.` — กู้ข้อมูลเอง |

> การค้นด้วยบาร์โค้ด (`find_by_barcode`) ยังไม่มีเมนูของตัวเอง — โชวผ่านเทสต์ `TestServiceFindByBarcode`
> หรือผ่านข้อความ error เมื่อเพิ่มสินค้าบาร์โค้ดซ้ำ (`Barcode ... is already used by product ...`)

## ขั้นที่ 4 — Edge Cases ที่กรรมการสั่ง + ตรวจรับแฟ้ม (4 นาที)

| คำสั่งกรรมการ | ปุ่ม | ผลที่ต้องเห็น |
|---|---|---|
| "ตัดสต๊อกเกินที่มี" | `3` → `101` → `999` | `Error: Not enough stock!` |
| "ราคา 'abc'" | `2` → … → Price `abc` | `Invalid input: Qty and Price must be numbers.` |
| "ราคาติดลบ" | `2` → … → Price `-5` | `Invalid input: Price must not be negative.` |
| "Export ซ้ำสองรอบ" | `7` → `r.csv` สองครั้ง | ไฟล์ถูกเขียนทับ ไม่มีแถวซ้ำ |
| "จำนวนติดลบ / ศูนย์" | `3` → `101` → `-5` | `Error: Amount must be greater than zero!` |
| "บาร์โค้ดซ้ำ" | เพิ่มสินค้าใหม่ใช้ `885999001` | `Error: Barcode 885999001 is already used by product P999.` |

จากนั้นยื่น [Final System Maintenance Dossier](../Final_System_Maintenance_Dossier.md) และ
[Technical Handover Certificate](Technical_Handover_Certificate.md) ให้ลงนาม

## แผนสำรองถ้าหน้างานพัง

| ปัญหา | ทางออก |
|---|---|
| ไม่มีอินเทอร์เน็ต → `pip install` ไม่ได้ | `./setup.sh --runtime` (ไม่ต้องลงอะไรเพิ่ม) หรือรัน `python app_v2.py` ตรง ๆ · เปิด [`week13/evidence/post_maintenance_test.log`](../week13/evidence/post_maintenance_test.log) แทน pytest สด |
| `python3` ไม่ทำงานบน Windows | สคริปต์เลือก `python` / `py` ให้เอง (แก้แล้วสัปดาห์ที่ 13) |
| PowerShell ไม่ให้รันสคริปต์ | ใช้ `-ExecutionPolicy Bypass` ตามคำสั่งข้างบน |
| Excel ไม่มีในเครื่อง | เปิด CSV ด้วย LibreOffice / Google Sheets — ไฟล์มี BOM UTF-8 |
