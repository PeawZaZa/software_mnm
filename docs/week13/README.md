# สัปดาห์ที่ 13 — Deployment Readiness · Project Closure & KPIs

| วิชา | หัวข้อ |
|---|---|
| ENGSE225 | Clean Deployment & Verification (ISO/IEC 12207 6.4.9 · ISO/IEC 14764) |
| ENGSE202 | Project Closure · KPI Scorecard · Lessons Learned (PMBOK 7) |

## สิ่งส่งมอบ — Phase 4.1 Bundle

| # | วิชา | ชิ้นงาน | ไฟล์ | สถานะ |
|---|---|---|---|---|
| 1 | ENGSE225 | รายงานการติดตั้งบน Clean Environment | [Clean_Environment_Installation_Report.md](Clean_Environment_Installation_Report.md) | ✅ |
| 2 | ENGSE225 | `post_maintenance_test.log` | [`evidence/post_maintenance_test.log`](evidence/post_maintenance_test.log) | ✅ 186 passed |
| 3 | ENGSE225 | System Operations & Maintenance Manual (6 บท) | [`../System_Operations_and_Maintenance_Manual.md`](../System_Operations_and_Maintenance_Manual.md) | ✅ |
| 4 | ENGSE225 | `setup.sh` + `.env.example` | [`setup.sh`](../../setup.sh) · [`setup.ps1`](../../setup.ps1) · [`.env.example`](../../.env.example) | ✅ |
| 1 | ENGSE202 | Project KPI Scorecard | [Project_KPI_Scorecard.md](Project_KPI_Scorecard.md) | ✅ |
| 2 | ENGSE202 | Lessons Learned Register | [Lessons_Learned_Register.md](Lessons_Learned_Register.md) | ✅ 11 รายการ |
| 3 | ENGSE202 | หลักฐานปิดกระดาน Jira + Release 2.0.0 | [Jira_Closure_Guide.md](Jira_Closure_Guide.md) | ✅ ปิดผ่าน Atlassian connector · ⬜ แคปภาพ |
| 4 | ENGSE202 | Draft Project Closure Report | [Draft_Project_Closure_Report.md](Draft_Project_Closure_Report.md) | ✅ ฉบับร่าง |

## ตัวเลขสำคัญ

| | |
|---|---|
| Clean install | `setup.sh` 25 วินาที · `setup.ps1` 19 วินาที · รอบแรกพัง (`python3` stub บน Windows) → แก้แล้ว |
| Tests | 173 → **186** (smoke 3 เคส) · coverage 99% |
| KPI Scorecard | 21 ตัวชี้วัด: 13 🟢/🏆 · 3 🟡 · 2 🔴 · 3 ⬜ |
| Lessons Learned | 11 รายการ — ทำได้ดี 3 · ต้องปรับ 8 |

## ⬜ งานที่ต้องทำเอง

- [ ] ทำตาม [Jira Closure Guide](Jira_Closure_Guide.md) และแคปภาพ 4 ภาพ
- [x] เปิด CSV ด้วย **LibreOffice Calc** (เครื่องไม่มี Excel) → [`../week15/evidence/csv_in_libreoffice_low_stock.png`](../week15/evidence/csv_in_libreoffice_low_stock.png)
- [ ] ทดสอบ `setup.sh` / `setup.ps1` บนเครื่องของสมาชิกคนอื่นอย่างน้อย 1 เครื่อง (ทดสอบแล้วบนเครื่องเดียว)
- [ ] ประชุม Retrospective ทั้งทีม ยืนยันบทเรียน 11 ข้อ แล้วเพิ่ม/แก้ตามความเห็นสมาชิก
