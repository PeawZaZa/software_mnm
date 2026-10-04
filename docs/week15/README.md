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
| 5 | Final Defense Slide Deck | [สไลด์ 15 หน้า (claude.ai)](https://claude.ai/artifact/NTXw24yjoxAdmHHu3LPz7L) · [Storyboard](../week14/Final_Defense_Storyboard.md) | ✅ ดาวน์โหลดเป็น PPTX/PDF ได้จากหน้าสไลด์ |
| — | Final Project Acceptance Certificate | [Final_Project_Acceptance_Certificate.md](Final_Project_Acceptance_Certificate.md) | ⬜ Sponsor ลงนาม |
| — | Team Release & Peer Review | [Team_Release_and_Peer_Review.md](Team_Release_and_Peer_Review.md) | ⬜ ทุกคนกรอก |

## ⬜ ลำดับงานที่ต้องทำเองก่อนวันนำเสนอ

1. ✅ merge เข้า `main` + tag `v2.0.0-evolution` และ `v2.0.1-evolution` แล้ว · ⬜ ลงนามใบ UAT · ⬜ สร้างหน้า GitHub Release แนบไฟล์ใน [`../week14/artifacts/`](../week14/artifacts/)
2. ✅ Jira: Sprint 3 ปิด · Release `2.0.0-evolution` released · 45/45 issues · ⬜ แคปภาพหลักฐาน
3. ✅ Log Work จำลอง 169 ชม. ลงครบ 45 ใบ (ระบุในทุก worklog ว่าเป็นค่าประมาณ)
4. ✅ เปิด CSV ด้วย LibreOffice Calc จริง — ภาษาไทยและชื่อที่มีจุลภาคถูกต้อง ([ภาพ](evidence/csv_in_libreoffice_low_stock.png)) · เครื่องไม่มี Excel
4. ซ้อมสาธิตบนเครื่องอื่นตาม [Live Demo Script](Live_Demo_and_Defense_Script.md)
5. หลังนำเสนอ: ลงนามเอกสาร → ทำ [Repository Ownership Transfer](Technical_Handover_Certificate.md#4-repository-ownership-transfer-เจ้าของบัญชี-peawzaza-ทำ) → Archive Jira
