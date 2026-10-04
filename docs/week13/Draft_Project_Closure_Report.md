# Project Closure Report (ฉบับร่าง)
## Mini Inventory System Evolution · ENGSE202 สัปดาห์ที่ 13 · ชิ้นงานที่ 4

| | |
|---|---|
| สถานะเอกสาร | **Draft v0.1** — ฉบับสมบูรณ์ส่งสัปดาห์ที่ 15 |
| ผู้จัดทำ | ปวริศ คูณศรี (Project Manager) |
| วันที่ | 2026-10-05 |
| Sponsor | อาจารย์ผู้สอน |

---

## ส่วนที่ 1 · Executive Summary

**ปัญหาตั้งต้น** — `app_v1.py` เป็นโปรแกรมคลังสินค้าแบบฟังก์ชันเดียวยาว 72 บรรทัด
ใช้ตัวแปร global แก้ไขจากทุกที่ ไม่มีชุดทดสอบ และพบจุดเสี่ยง 9 จุด (INV-4…12)

**วัตถุประสงค์ตาม Charter**

| # | วัตถุประสงค์ | ผล |
|---|---|---|
| 1 | ปรับโครงสร้างล้างหนี้ทางเทคนิค | ✅ 5 คลาสแยกชั้น · global 0 · v(G) 14 → 7 · 186 tests coverage 99% |
| 2 | ต่อเติมระบบ Barcode / Reorder Point (CR-01) | ✅ ส่งมอบ + เตือนตอนขาย (UAT-DEF-01) |
| 3 | รับมือคำขอเปลี่ยนแปลงระหว่างทาง (CR-02) | ✅ ผ่าน CCB · 4.5 ชม. ตามประมาณการ |
| 4 | ส่งมอบตามกำหนดเวลา | ❌ 2 ใน 3 sprints ช้า (21 และ 14 วัน) |
| 5 | อยู่ในงบประมาณ | ✅ คืนเงินสำรอง 900 บาท |

**ข้อสรุปหนึ่งประโยค** — ส่งมอบขอบเขตครบและคุณภาพเกินเป้า ภายในงบ
แต่ไม่ตรงเวลาเพราะวินัยการกระจายงานตลอดรอบ ซึ่งเป็นบทเรียนหลักของทีม

## ส่วนที่ 2 · Performance KPIs

ตารางเต็ม: [Project KPI Scorecard](Project_KPI_Scorecard.md)

| มิติ | ผล | สถานะ |
|---|---|---|
| Schedule | SPI ณ วันสิ้นสุดตามแผน 0.25 / 1.00 / 0.00 · ตรงเวลา 1 / 3 sprints | 🔴 |
| Cost | CPI 0.997 🔶 · ค่าเครื่องมือ 0 บาท · เงินสำรองคงเหลือ 900 บาท | 🟡 |
| Quality | Coverage 99% · v(G) 7 · flake8 0 · bandit 0 · Critical defects 0 | 🏆 |
| Stakeholder | UAT รอบแรก 7/8 → 8/8 · Scope 100% · Cross-team UAT รอผล | 🟡 |

## ส่วนที่ 3 · Financials & EVM

ตารางเต็ม: [Final EVM & Velocity Report](../week12/Final_EVM_and_Velocity_Report.md)

| PV | EV | AC | SV | CV | SPI | CPI |
|---:|---:|---:|---:|---:|---:|---:|
| 50,550 | 50,550 | 50,700 🔶 | 0 | −150 | 1.00 | 0.997 |

Velocity 16 → 19 → 10 issues · เฉลี่ย 15 issues/sprint

## ส่วนที่ 4 · Procurement Close-out

ตารางเต็ม: [Procurement Close-out & Reserve Settlement](../week12/Procurement_Closeout_and_Reserve_Settlement.md)

| รายการ | ผล |
|---|---|
| ค่าเครื่องมือ | Budget 0 · Actual 0 · ไม่มีหนี้ค้างจากโครงการ |
| เงินสำรอง | 12.0 ชม. → ใช้ 9.0 → **คืน 3.0 ชม. = 900 บาท** |
| ค้าง | GitHub billing lock (เจ้าของบัญชีต้องตรวจ) |

## ส่วนที่ 5 · Lessons Learned

ทะเบียนเต็ม 11 รายการ: [Lessons Learned Register](Lessons_Learned_Register.md)

| ทำต่อ 😄 | เลิกทำ 😡 |
|---|---|
| เขียน characterization test ก่อนแตะ legacy (LL-01) | ปล่อยงานกองถึงวันสุดท้าย (LL-02) |
| ใช้ CR Impact Form + CCB ทุกคำขอ (LL-06) | merge PR ของตัวเองโดยไม่มีคน review (LL-03) |
| ทดสอบติดตั้งบนเครื่องสะอาดก่อน release (LL-11) | กลืน exception แล้วตอบว่าสำเร็จ (LL-07) |

---

## ส่วนที่ยังต้องเติมก่อนฉบับสมบูรณ์

- [ ] ผล Cross-team UAT และลายเซ็น UAT Sign-off
- [ ] หลักฐาน Tag `v2.0.0-evolution` บน `main` + GitHub Release
- [ ] ผล pip-audit (สัปดาห์ที่ 14)
- [ ] ROI / Benefit realization (สัปดาห์ที่ 14)
- [ ] ชั่วโมงจริงจาก Jira Log Work (แทน AC ประมาณการ)
- [ ] ภาพหลักฐาน Jira ตาม [Jira Closure Guide](Jira_Closure_Guide.md)
