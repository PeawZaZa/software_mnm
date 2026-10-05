# สัปดาห์ที่ 15 — Final Defense · Handover · Formal Closure

| วิชา | หัวข้อ |
|---|---|
| ENGSE225 | Live Demo, Technical Defense & Handover (ISO/IEC 12207 6.4.10–6.4.11 · ISO/IEC 14764) |
| ENGSE202 | Final Defense & Formal Closure (PMBOK 7) |

## สิ่งส่งมอบ ENGSE225

| # | ชิ้นงาน | ไฟล์ | สถานะ |
|---|---|---|---|
| 1 | Final System Maintenance Dossier (7 หมวด) | [`../Final_System_Maintenance_Dossier.md`](../Final_System_Maintenance_Dossier.md) | ✅ |
| 2 | GitHub `main` + แท็ก `v2.0.0-evolution` | [Release Runbook](../week12/Release_Runbook_v2.0.0-evolution.md) | ✅ push + tag + หน้า Release ([ภาพ](evidence/github_releases.jpg)) — merge ตรงไม่ผ่าน PR (บันทึกใน Runbook) |
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

1. ✅ merge เข้า `main` + tag `v2.0.0-evolution` และ `v2.0.1-evolution` แล้ว · ⬜ ลงนามใบ UAT · ✅ สร้างหน้า GitHub Release ทั้ง 2 เวอร์ชันแล้ว ([ภาพ](evidence/github_releases.jpg)) · ⬜ แนบไฟล์ใน [`../week14/artifacts/`](../week14/artifacts/) เพิ่มเอง (ตอนนี้มีแค่ source zip อัตโนมัติ)
2. ✅ Jira: Sprint 3 ปิด · Release `2.0.0-evolution` released · 45/45 issues · ✅ แคปภาพหลักฐานแล้ว ([Summary](evidence/jira_summary.jpg) · [Reports](evidence/jira_reports_overview.jpg) · [Velocity](evidence/jira_velocity.jpg) · [Burnup](evidence/jira_burnup_sprint3.jpg) · [Burndown](evidence/jira_burndown_sprint3.jpg) · [CFD](evidence/jira_cfd.jpg))
   - ⚠️ **อ่านกราฟ Jira อย่างระวัง:** Velocity แสดง Commitment 0 เพราะโปรเจกต์ตั้ง Estimation = Time แต่ไม่ได้ใส่ original estimate ตอนเริ่ม sprint ·
     Burnup/Burndown (นับจำนวนงาน) ของ Sprint 3 เป็นเส้นแบน 11 ใบแล้วหักที่ 5 ต.ค. เพราะสถานะใน Jira ถูกอัปเดตย้อนหลังพร้อมกันในวันเดียว ไม่ได้อัปเดตระหว่าง sprint ·
     จำนวน 11 รวม SAM1-39 ที่ค้างมาจาก Sprint 2 ([รายละเอียด](../../project_archives/jira_sprints_and_release.md)) ·
     หลักฐานความคืบหน้าที่ใช้วิเคราะห์จริงคือกราฟใน [`docs/images/`](../images/) ที่สร้างจาก commit/PR history
   - บทเรียน: บอร์ดต้องอัปเดตทุกวันระหว่าง sprint ไม่ใช่ตอนปิดงาน — ตรงกับนโยบายข้อ 2 ใน Lessons Learned
3. ✅ Log Work จำลอง 169 ชม. ลงครบ 45 ใบ (ระบุในทุก worklog ว่าเป็นค่าประมาณ)
4. ✅ เปิด CSV ด้วย LibreOffice Calc จริง — ภาษาไทยและชื่อที่มีจุลภาคถูกต้อง ([ภาพ](evidence/csv_in_libreoffice_low_stock.png)) · เครื่องไม่มี Excel
5. ✅ Docker: build image + smoke test ผ่าน 5/5 ([log](evidence/docker_smoke_test.log))
6. ซ้อมสาธิตบนเครื่องอื่นตาม [Live Demo Script](Live_Demo_and_Defense_Script.md)
7. ⬜ **Branch Protection (เจ้าของ repo `PeawZaZa` ต้องทำ — บัญชีสมาชิกอื่นไม่มีสิทธิ์ admin):**
   Settings → Branches → Add classic branch protection rule สำหรับ `main` และ `develop`
   - ✅ Require a pull request before merging · Required approvals = 1
   - ✅ Do not allow bypassing the above settings
   - ⬜ ยังไม่ติ๊ก Require status checks จนกว่าจะเคลียร์ billing ของ GitHub Actions (ไม่งั้น merge ไม่ได้เลย)
8. หลังนำเสนอ: ลงนามเอกสาร → ทำ [Repository Ownership Transfer](Technical_Handover_Certificate.md#4-repository-ownership-transfer-เจ้าของบัญชี-peawzaza-ทำ) → Archive Jira
