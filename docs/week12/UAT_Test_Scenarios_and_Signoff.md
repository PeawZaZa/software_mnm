# UAT Test Scenarios & Sign-off Sheet
## ENGSE225 สัปดาห์ที่ 12 · ชิ้นงานที่ 1 — ส่งต่อให้ ENGSE202 ใช้ขอปิดเฟส

| | |
|---|---|
| ระบบที่ทดสอบ | Inventory System `2.0.0-evolution` (release candidate บน `develop`) |
| เวอร์ชันโค้ด | สาขา `release/v2.0.0-evolution` |
| มาตรฐานอ้างอิง | ISO/IEC/IEEE 29119-4:2021 (Scenario testing) · ISO/IEC/IEEE 12207 (Validation) |
| ผู้ออกแบบ | ตรัยรัตน์ วงษ์สิทธิ์ (QA) |
| วันที่ | 2026-10-05 |

---

## 1. ขอบเขต UAT

UAT ไม่ได้ทดสอบฟังก์ชันย่อย (unit test ทำไปแล้ว 173 เคส) แต่จำลอง**วงจรการทำงานจริงของผู้ใช้ตั้งแต่ต้นจนจบ**
เพื่อยืนยัน 2 เรื่อง

1. **ฟังก์ชันเดิมยังถูกต้อง** — สรุปมูลค่าคงคลังคำนวณถูก 100%
2. **ฟังก์ชันใหม่ตอบโจทย์ธุรกิจ** — Barcode · การเตือนจุดสั่งซื้อ · CSV Export

## 2. UAT Scenarios

ข้อมูลเริ่มต้น: ไม่มี `data.json` (ระบบสร้างสินค้าตั้งต้น 3 รายการ มูลค่ารวม 1,540 บาท)
ทุกสถานการณ์ทำต่อเนื่องกันบนข้อมูลชุดเดียว

| ID | ผู้ใช้ | ขั้นตอนและข้อมูลป้อน | ผลลัพธ์ทางธุรกิจที่คาดหวัง |
|---|---|---|---|
| **UAT-SC01** | Inventory Manager | เมนู 2 → ID `P100` · Name `Milk` · Qty `10` · Price `20` · Category `Dairy` · Barcode `885123456789` · Reorder Point `5` → เมนู 1 | ขึ้น `Done.` ไม่ crash และเห็น Milk สต๊อก 10 ในรายการ |
| **UAT-SC02** | Store Cashier | เมนู 3 → `P100` ออก `6` (เหลือ 4 ≤ จุดสั่งซื้อ 5) | ขึ้นข้อความเตือนทันทีหลังตัดสต๊อก |
| **UAT-SC02-B** | Store Cashier | เมนู 2 เพิ่ม `P200 Water` สต๊อก `40` · Reorder Point `30` → เมนู 3 ขายออก `12` (เหลือ 28 ≤ 30) | ขึ้นข้อความเตือนว่า**ถึงจุดสั่งซื้อ** ทันที — สินค้าขายเร็วต้องสั่งก่อนเหลือน้อยกว่า 10 |
| **UAT-SC03** | Purchasing Officer | เมนู 7 → ตั้งชื่อไฟล์ `uat_report.csv` → เปิดใน Microsoft Excel | มีคอลัมน์ `barcode` และ `reorder_point` · Milk บาร์โค้ดและสต๊อก 4 ถูกต้อง · ภาษาไทยไม่เพี้ยน |
| **UAT-SC04** | Store Owner | เมนู 4 Inventory Summary | มูลค่ารวม **1,900 บาท** = 1,540 + Milk 4×20 + Water 28×10 |
| **UAT-EC01** | กรรมการ (edge) | เมนู 3 ขอตัด Milk `999` ชิ้น | ปฏิเสธ `Not enough stock` · สต๊อกยังเป็น 4 · ไม่ crash |
| **UAT-EC02** | กรรมการ (edge) | เมนู 2 กรอกราคา `abc` และอีกรอบกรอกราคา `-5` | ปฏิเสธทั้งสองครั้งด้วยข้อความที่อ่านเข้าใจ ไม่มี Traceback |
| **UAT-EC03** | กรรมการ (edge) | เมนู 7 Export ไปไฟล์เดิมซ้ำ 2 รอบติดกัน | ไฟล์ถูกเขียนทับสมบูรณ์ ไม่มีแถวซ้ำ เปิดได้ปกติ |

> UAT-SC02-B, SC04 และ EC01–EC03 ทีมเพิ่มจากตัวอย่างในใบงาน — SC02-B ทดสอบกรณีที่จุดสั่งซื้อรายชิ้น**สูงกว่า**เกณฑ์รวม 10
> เพราะตัวอย่างในใบงาน (เหลือ 4 ≤ 5) ต่ำกว่า 10 อยู่แล้ว จึงพิสูจน์ไม่ได้ว่าระบบเตือนเพราะ reorder point จริง ๆ

## 3. ผลรอบซ้อม (Internal dry-run โดยทีม) — รันผ่านหน้าจอ CLI จริงด้วย `tools/run_uat.py`

| ID | รอบที่ 1 — `develop` @ `3bbfdb8` | รอบที่ 2 — หลังแก้ UAT-DEF-01 |
|---|---|---|
| UAT-SC01 | ✅ Pass | ✅ Pass |
| UAT-SC02 | ✅ Pass | ✅ Pass |
| UAT-SC02-B | ❌ **Fail** — ระบบตอบแค่ `Stock updated.` | ✅ Pass — `Stock updated. !!! REORDER POINT REACHED: 28 left (reorder point 30) !!!` |
| UAT-SC03 | ✅ Pass (ตรวจไฟล์อัตโนมัติ: BOM · header · ข้อมูล Milk) | ✅ Pass |
| UAT-SC04 | ✅ Pass — 1900.0 THB | ✅ Pass |
| UAT-EC01 | ✅ Pass | ✅ Pass |
| UAT-EC02 | ✅ Pass | ✅ Pass |
| UAT-EC03 | ✅ Pass | ✅ Pass |
| **รวม** | **7 / 8** | **8 / 8** |

Transcript หน้าจอเต็ม: [`evidence/uat_run_1_before_fix.txt`](evidence/uat_run_1_before_fix.txt) ·
[`evidence/uat_run_2_after_fix.txt`](evidence/uat_run_2_after_fix.txt)

> สคริปต์ตรวจ UAT-SC03 ได้แค่ว่าไฟล์ถูกต้องตามรูปแบบที่ Excel อ่านได้ **การเปิดใน Excel จริงต้องให้ผู้ทดสอบทำ** ในรอบ Cross-Team

## 4. แยกแยะ UAT Defect กับ New Scope

| เรื่องที่พบ | ประเภท | เหตุผล | การจัดการ |
|---|---|---|---|
| **UAT-DEF-01** ขายสินค้าจนถึงจุดสั่งซื้อแล้วไม่มีคำเตือน ถ้า reorder point > 10 | 🐞 **Defect** | CR-01 สัญญาว่ามี "Reorder Point" และใบงานกำหนดให้ระบบเตือนเมื่อสต๊อก ≤ Reorder Point — ระบบทำไม่ได้ตามที่สัญญา | แก้ทันทีบนสาขา `fix/uat-def-01-reorder-alert` · เทสต์ใหม่ 6 เคส (4 เคสแดงก่อนแก้) · ใช้กันชน 1.5 ชม. |
| ผู้ใช้อยากได้ CSV **เฉพาะ**สินค้าสต๊อกต่ำ | ✨ **New Scope** | CR-02 ที่ CCB อนุมัติคือ "ส่งออกสินค้า**ทั้งหมด**" ([CR-02 Form](../CR-02_Impact_and_Decision_Form.md)) | ไม่ทำ — บันทึกเป็น FB-01 ใน [Future Backlog v3.0](../week11/Scope_Freeze_Agreement.md#5-future-backlog-v30--คำขอที่รับทราบแต่ไม่ทำในโครงการนี้) ผู้ใช้กรองคอลัมน์ `reorder_point` ใน Excel ได้ |

### Root cause ของ UAT-DEF-01

```python
# ก่อนแก้ — stock_out() ดูแค่เกณฑ์รวม
if product.qty < self.LOW_STOCK:          # 10
    return True, "Stock updated. !!! WARNING ... !!!"
return True, "Stock updated."
```

CR-01 เพิ่ม `reorder_point` และเมนู 6 สำหรับ*ดูรายการ* แต่ไม่ได้ต่อเข้ากับจังหวะ*ขายของ*
เทสต์ของ CR-01 ทดสอบ `get_reorder_list()` แยกเดี่ยว จึงไม่มีเทสต์ไหนจับได้ — จับได้เมื่อทดสอบเป็นวงจรผู้ใช้ใน UAT

## 5. UAT รอบตรวจรับ — **จำลอง** (Simulated UAT)

> ⚠️ **ทีมจัดทำ UAT แบบจำลอง เนื่องจากไม่มีเวลาจัด Cross-team UAT กับกลุ่มอื่น**
> สคริปต์ [`tools/run_uat.py`](../../tools/run_uat.py) เล่นบทผู้ใช้ทั้ง 4 บทบาท ป้อนข้อมูลผ่านหน้าจอ CLI จริงของโปรแกรม
> บนโค้ดล่าสุด (`develop` @ `7feb2e4`) — **ไม่ได้ทดสอบโดยคนนอกทีม** จึงยังมีความเสี่ยงเรื่อง Confirmation Bias
> ถ้ามีเวลาก่อนนำเสนอ ให้กลุ่มอื่นทดสอบตามตารางข้อ 2 แล้วกรอกเพิ่มในคอลัมน์ "ผู้ทดสอบภายนอก"

| ID | ผลจำลอง (`develop` @ `7feb2e4`) | สิ่งที่เห็นบนหน้าจอ | ผู้ทดสอบภายนอก (ถ้ามี) |
|---|---|---|---|
| UAT-SC01 | ✅ Pass | `Done.` · `Name: Milk \| Stock: 10` | |
| UAT-SC02 | ✅ Pass | `!!! WARNING ... !!! !!! REORDER POINT REACHED: 4 left (reorder point 5) !!!` | |
| UAT-SC02-B | ✅ Pass | `!!! REORDER POINT REACHED: 28 left (reorder point 30) !!!` | |
| UAT-SC03 | ✅ Pass (ตรวจไฟล์: BOM · header · แถว Milk) — ⚠️ ยังไม่ได้เปิดใน Excel จริง | `Exported 5 products to .../uat_report.csv` | |
| UAT-SC04 | ✅ Pass | `Total inventory value: 1900.0 THB` | |
| UAT-EC01 | ✅ Pass | `Error: Not enough stock!` · สต๊อกยัง 4 | |
| UAT-EC02 | ✅ Pass | `must be numbers` · `must not be negative` · ไม่มี Traceback | |
| UAT-EC03 | ✅ Pass | Export 2 รอบ ไม่มีแถวซ้ำ | |
| **รวม** | **8 / 8** | Transcript: [`evidence/uat_run_3_simulated_final.txt`](evidence/uat_run_3_simulated_final.txt) | |

---

## 6. ใบรับรองการตรวจรับงาน (UAT Sign-off Certificate)

| | |
|---|---|
| ระบบ | Mini Inventory System v2.0.0-evolution |
| จำนวน Scenarios | 8 |
| ผ่าน | **8 / 8** (UAT จำลอง — ข้อ 5) |
| ข้อบกพร่องที่ค้าง | **0** รายการ (UAT-DEF-01 แก้แล้ว) |
| วิธีทดสอบ | จำลองโดยทีมผ่าน `tools/run_uat.py` — ไม่ใช่ Cross-team |

**ข้อความรับรอง** — ข้าพเจ้าได้ทดสอบระบบตาม UAT Scenarios ข้างต้นในฐานะผู้ใช้งาน
และยืนยันว่าระบบตอบโจทย์ทางธุรกิจตามขอบเขตที่ตกลงไว้ใน Scope Freeze Agreement (SFA-2026-001)
**อนุมัติให้ปล่อยสู่ Production** (รวมสาขาเข้า `main` และติดแท็ก `v2.0.0-evolution`)

| บทบาท | ชื่อ | กลุ่ม | ลายมือชื่อ | วันที่ |
|---|---|---|---|---|
| ตัวแทนผู้ทดสอบ (ลูกค้าสมมติ) — ถ้าไม่มีคนนอก ให้อาจารย์/PM ลงนามในฐานะผู้รับรองผลจำลอง | | | | |
| Tech Lead | พนาวุฒน์ อภิปสันติ | กลุ่มเจ้าของระบบ | | |
| QA | ตรัยรัตน์ วงษ์สิทธิ์ | กลุ่มเจ้าของระบบ | | |

> 🖊️ สแกนใบที่ลงนามแล้วเก็บไว้ที่ `docs/week12/signed/UAT_Signoff_signed.pdf`
> **ห้าม merge เข้า `main` ก่อนได้ลายเซ็นนี้** — เป็นเงื่อนไขข้อแรกของ [Release Runbook](Release_Runbook_v2.0.0-evolution.md)
