# Final Defense Storyboard (โครงร่างสไลด์ 20 นาที)
## ENGSE202 สัปดาห์ที่ 14 · Workshop ขั้นที่ 5 — ใช้ต่อในสัปดาห์ที่ 15

| ส่วน | เวลา | ผู้นำเสนอ | สไลด์ | ตัวเลข/หลักฐานที่ต้องโชว์ |
|---|---:|---|---|---|
| **1 · The Problem & Legacy Debt** | 3 นาที | PM — ปวริศ | ① ชื่อโครงการ + ทีม ② `app_v1.py`: `global x` · `main()` 72 บรรทัด · v(G) 14 · 0 tests ③ Charter 5 วัตถุประสงค์ + WBS | [Dossier หมวด 1](../Final_System_Maintenance_Dossier.md#หมวดที่-1--overview) |
| **2 · Architecture & Live Demo** | 8 นาที | Tech Lead — พนาวุฒน์ | ④ As-Is vs As-Built + class diagram ⑤ **สด:** `./setup.sh` บนเครื่องใหม่ (< 2 นาที) ⑥ **สด:** `pytest -v --cov` 195 passed 99% ⑦ **สด:** Barcode → ขายจนเตือน REORDER → Export CSV → เปิด Excel ⑧ **สด:** ทำไฟล์เสีย → เปิดใหม่กู้จาก `.bak` | [Demo script สัปดาห์ที่ 15](../week15/Live_Demo_and_Defense_Script.md) |
| **3 · Governance KPIs & EVM** | 5 นาที | PM — ปวริศ | ⑨ Burnup + CFD (คอขวด Review 5 PR) ⑩ EVM: PV=EV 50,550 · AC 50,700 · CPI 0.997 · **SPI ณ วันตามแผน 0.25/1.00/0.00** ⑪ KPI Scorecard 21 ข้อ | [Final EVM](../week12/Final_EVM_and_Velocity_Report.md) · [KPI](../week13/Project_KPI_Scorecard.md) |
| **4 · Business ROI & Lessons** | 4 นาที | QA — ตรัยรัตน์ · Dev — ทวีชัย | ⑫ ROI: คืนทุน 26.8 เดือน · 3 ปี +34% + sensitivity ⑬ Top 5 นโยบาย ⑭ "กฎที่ไม่มีกลไกบังคับ = ไม่มีกฎ" | [ROI](Benefit_Realization_ROI_Report.md) · [Compendium](Lessons_Learned_Compendium.md) |
| Q&A | — | ทุกคน | ⑮ สไลด์สำรองตอบคำถามยาก | ข้อ 2 |

## คำถามที่คาดว่ากรรมการจะถาม

| คำถาม | คำตอบ (พร้อมหลักฐาน) | ผู้ตอบ |
|---|---|---|
| "ทำไม CPI 0.997 — เชื่อได้แค่ไหน?" | AC ประมาณจากแผน + กันชน + งานทำซ้ำที่มีหลักฐานใน git เพราะไม่มีใคร Log Work — ยืนยันได้แค่ไม่มีหลักฐานใช้งบเกิน (LL-10) | PM |
| "SPI 1.00 แต่ส่งช้า?" | SPI ปลายทางบอดเสมอ — ณ วันตามแผน 0.25 / 1.00 / 0.00 เรารายงานมิติเวลาว่าไม่ผ่าน | PM |
| "ROI ติดลบปีแรก คุ้มไหม?" | คืนทุน 27 เดือน · คุณค่าใหญ่คือความเสี่ยงข้อมูลหาย 3 จุดที่ปิดได้ | PM |
| "ถ้าเปลี่ยนไป PostgreSQL ต้องรื้อเยอะไหม?" | สร้างคลาสใหม่ที่มี `load()`/`save()` แล้วส่งให้ `InventoryService` ใน `main()` — ไม่แตะ service/UI ([O&M 6.3](../System_Operations_and_Maintenance_Manual.md#63-แนวทางสำหรับนักพัฒนารุ่นต่อไป)) | Tech Lead |
| "มั่นใจได้อย่างไรว่าไม่มีบั๊กค้าง?" | 195 tests 99% · UAT 8/8 · flake8/bandit/pip-audit 0 — และเปิดเผย DEF-04 (Low) ที่รับทราบไว้ | QA |
| "ตัดสต๊อกเกินที่มี / ราคา 'abc' / export ซ้ำ" | ทดสอบไว้แล้ว UAT-EC01–03 — โชวสดได้ | Dev |
| "Rollback ทำอย่างไร?" | ไปแท็กที่ผ่านเทสต์ด้วย `git restore --source` — ซ้อมจริง RTO 1.4 วิ และเจอว่า `main` เดิมเสีย | Tech Lead |

## ⬜ ต้องเตรียม

- [ ] ทำสไลด์ตาม storyboard (ใช้กราฟใน [`../images/`](../images/))
- [ ] ซ้อมจับเวลา 20 นาที 2 รอบ
- [ ] เครื่องสาธิตที่ไม่ใช่เครื่องพัฒนา มี Python ≥ 3.10 + Excel
