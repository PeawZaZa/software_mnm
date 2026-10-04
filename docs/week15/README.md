# สัปดาห์ที่ 15 — Final Defense · Handover · Formal Closure

| วิชา | หัวข้อ |
|---|---|
| ENGSE225 | Live Demo, Technical Defense & Handover (ISO/IEC 12207 6.4.10–6.4.11 · ISO/IEC 14764) |
| ENGSE202 | Final Defense & Formal Closure (PMBOK 7) |

## สิ่งส่งมอบ ENGSE225

| # | ชิ้นงาน | ไฟล์ | สถานะ |
|---|---|---|---|
| 1 | Final System Maintenance Dossier (7 หมวด) | [`../Final_System_Maintenance_Dossier.md`](../Final_System_Maintenance_Dossier.md) | ✅ |
| 2 | GitHub `main` + แท็ก `v2.0.0-evolution` | [Release Runbook](../week12/Release_Runbook_v2.0.0-evolution.md) | ⬜ ต้อง push + PR + tag |
| 3 | GitHub Actions เขียวบน `main` | — | ⬜ ต้องเคลียร์ billing ก่อน |
| 4 | Technical Handover Certificate | [Technical_Handover_Certificate.md](Technical_Handover_Certificate.md) | ⬜ ลงนามหลังสาธิต |
| — | สคริปต์สาธิตสด + แผนสำรอง | [Live_Demo_and_Defense_Script.md](Live_Demo_and_Defense_Script.md) · [ซ้อมแล้ว](evidence/rehearsal_log.txt) | ✅ |

## สิ่งส่งมอบ ENGSE202

| # | ชิ้นงาน | ไฟล์ | สถานะ |
|---|---|---|---|
| 1 | Final Project Closure Report | [Final_Project_Closure_Report.md](Final_Project_Closure_Report.md) | ✅ |
| 2 | Master KPI Scorecard | [Master_KPI_Scorecard.md](Master_KPI_Scorecard.md) | ✅ (2 ช่องเติมหลังกิจกรรม) |
| 3 | Procurement & Reserve Close-out | [Procurement_and_Reserve_Closeout_Sheet.md](Procurement_and_Reserve_Closeout_Sheet.md) | ✅ |
| 4 | Comprehensive Lessons Learned Register | [Comprehensive_Lessons_Learned_Register.md](Comprehensive_Lessons_Learned_Register.md) | ✅ 13 รายการ |
| 5 | Final Defense Slide Deck | [Storyboard](../week14/Final_Defense_Storyboard.md) | ⬜ ดูหมายเหตุด้านล่าง |
| — | Final Project Acceptance Certificate | [Final_Project_Acceptance_Certificate.md](Final_Project_Acceptance_Certificate.md) | ⬜ Sponsor ลงนาม |
| — | Team Release & Peer Review | [Team_Release_and_Peer_Review.md](Team_Release_and_Peer_Review.md) | ⬜ ทุกคนกรอก |

## ⬜ ลำดับงานที่ต้องทำเองก่อนวันนำเสนอ

1. Cross-team UAT + ลายเซ็น → push → PR release เข้า `main` → tag `v2.0.0-evolution` ([Runbook](../week12/Release_Runbook_v2.0.0-evolution.md))
2. Merge `develop` (งานสัปดาห์ที่ 13–14) เข้า `main` อีกรอบ → tag `v2.0.1-evolution` → แนบไฟล์ใน [`../week14/artifacts/`](../week14/artifacts/) กับ GitHub Release
3. ปิดงาน Jira ตาม [Jira Closure Guide](../week13/Jira_Closure_Guide.md)
4. ซ้อมสาธิตบนเครื่องอื่นตาม [Live Demo Script](Live_Demo_and_Defense_Script.md)
5. หลังนำเสนอ: ลงนามเอกสาร → ทำ [Repository Ownership Transfer](Technical_Handover_Certificate.md#4-repository-ownership-transfer-เจ้าของบัญชี-peawzaza-ทำ) → Archive Jira
