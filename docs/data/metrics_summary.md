# Metrics Summary (สร้างอัตโนมัติจาก tools/pm_metrics.py — ห้ามแก้ไฟล์นี้ด้วยมือ)

## EVM ณ วันเสร็จจริงของแต่ละ Sprint

อัตราค่าแรง 300 บาท/ชม. (assumed)

| Sprint | PV | EV | AC | SV | CV | SPI | CPI | ส่งช้า (วัน) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sprint 1 | 19,200 | 19,200 | 19,350 | 0 | -150 | 1.00 | 0.992 | 21 |
| Sprint 2 | 20,100 | 20,100 | 20,100 | 0 | 0 | 1.00 | 1.000 | 0 |
| Sprint 3 | 11,250 | 11,250 | 11,250 | 0 | 0 | 1.00 | 1.000 | 14 |
| รวม 3 Sprints | 50,550 | 50,550 | 50,700 | 0 | -150 | 1.00 | 0.997 |  |

## SPI ณ วันสิ้นสุดตามแผนของแต่ละ Sprint (มุมมองที่ไม่บอด)

| Sprint | วันสิ้นสุดตามแผน | PV | EV ณ วันนั้น | SPI |
|---|---|---:|---:|---:|
| Sprint 1 | 2026-07-13 | 19,200 | 4,800 | 0.25 |
| Sprint 2 | 2026-09-07 | 20,100 | 20,100 | 1.00 |
| Sprint 3 | 2026-09-21 | 11,250 | 0 | 0.00 |

## Contingency Reserve

| รายการ | เรื่อง | เบิก (ชม.) | คงเหลือ (ชม.) |
|---|---|---:|---:|
| ยอดตั้งต้น |  | 0.0 | 12.0 |
| CR-2026-001 | แก้ข้อบกพร่องจาก Bug Bashing DEF-01/02/03 | 2.5 | 9.5 |
| CR-2026-002 | พัฒนา CR-02 Export CSV | 4.5 | 5.0 |
| CR-2026-003 | แก้ UAT-DEF-01 ตัดสต๊อกแล้วไม่เตือนเมื่อถึง Reorder Point | 1.5 | 3.5 |
| CR-2026-004 | ชดเชยค่าแรงส่วนเกิน: งานทำซ้ำ PR #14 → #15 → #19 (บันทึกตอนกระทบยอดปิดเฟส) | 0.5 | 3.0 |

คงเหลือสุทธิ **3.0 ชม. = 900 บาท**

## Flow (จาก GitHub PR)

| PR | สาขา | ผู้เปิด | Lead time (นาที) | Review (นาที) |
|---|---|---|---:|---:|
| #1 | feature/qa/unit-tests | TriratWongsit | 7 | 1 |
| #2 | feature/dev/input-validation | Saihakuto | 115 | 75 |
| #3 | feature/tl/refactor-global-state | Phanawut | 123 | 68 |
| #4 | feature/tl/fix-logic-bugs | Phanawut | 161 | 122 |
| #5 | feature/dev/fix-negative-stock | Saihakuto | 154 | 110 |
| #6 | feature/dev/fix-naming-and-io | Saihakuto | 134 | 103 |
| #8 | feature/tl/architecture-doc | Phanawut | 15 | 12 |
| #9 | feature/pm/docs | PeawZaZa | 4 | 1 |
| #10 | feature/pm/docs | PeawZaZa | 1 | 0 |
| #11 | feature/pm/docs | PeawZaZa | 1 | 0 |
| #14 | feature/test-app | PeawZaZa | 13 | 1 |
| #15 | revert-14-feature/test-app | PeawZaZa | 0 | 0 |
| #19 | feature/test-app | PeawZaZa | 19 | 13 |
| #23 | feature/sprint2-class-refactor | PeawZaZa | 58 | 1 |
| #24 | feature/cr01-barcode-reorder-point | PeawZaZa | 21 | 0 |
| #25 | feature/cr02-csv-export | PeawZaZa | 17 | 0 |
| #26 | fix/bug-bashing | PeawZaZa | 5 | 0 |

Sprint 1 (#1–#11): เฉลี่ย Lead time 71 นาที · Review 49 นาที

Sprint 2 (#23–#26): เฉลี่ย Lead time 25 นาที · Review 0 นาที

WIP สูงสุดในช่อง Review = **5 PR** เมื่อ 2026-07-13 00:02 (เวลาไทย)

## ROI

| ผลประโยชน์ | บาท/ปี |
|---|---:|
| B1 | 14,400 |
| B2 | 2,280 |
| B3 | 6,000 |
| **รวม** | **22,680** |

ต้นทุน (AC รวม) 50,700 บาท · ROI ปีแรก -55.3% · ROI 3 ปี +34.2% · คืนทุน 26.8 เดือน
