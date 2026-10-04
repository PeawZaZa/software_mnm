# Jira Export — Sprints · Velocity · Release

ดึงจาก Jira `SAM1` ผ่าน Atlassian connector วันที่ 2026-10-05 · รายการงานทั้งหมด: [`jira_all_issues.csv`](jira_all_issues.csv) (49 ใบ)

## Sprints

| Sprint | Start | End (แผน) | Complete (จริง) | Issues ใน sprint | Done |
|---|---|---|---|---:|---:|
| SAM1 Sprint 1 | 2026-06-29 | 2026-07-13 | 2026-09-07 ¹ | 16 | 16 |
| SAM1 Sprint 2 | 2026-08-10 | 2026-09-07 | 2026-09-07 | 19 | 19 |
| SAM1 Sprint 3 | 2026-09-08 | 2026-09-21 | 2026-10-05 | 11 ² | 11 |

¹ Sprint 1 ถูกกด Complete ในระบบเมื่อ 7 ก.ย. (ตอนเปิดใช้ฟีเจอร์ Sprints) แม้งานปิดครบตั้งแต่ 3 ส.ค. — ใช้วันที่ 3 ส.ค. ในการวิเคราะห์ EVM

² **ข้อผิดพลาดตอนจัด sprint:** SAM1-39 (งาน Sprint 2 ที่ Done แล้ว) ค้างอยู่ใน Sprint 3 ตอนปิด sprint
Velocity Report ของ Jira จึงแสดง Sprint 3 = 11 ใบ ค่าที่ถูกต้องตามเอกสารคือ **10 ใบ** (แผน 9 + UAT-DEF-01)
sprint ที่ปิดแล้วแก้ไม่ได้ จึงบันทึกไว้ที่นี่

## Release

| Version | สถานะ | Release date | Issues |
|---|---|---|---:|
| `2.0.0-evolution` | ✅ Released | 2026-10-05 | 45 (Done 45) |
| `3.0` | Unreleased — Future Backlog | — | 4 (FB-01…04) |

JQL ยืนยัน:
- `project = SAM1 AND statusCategory != Done` → 4 ใบ (เฉพาะ FB-01…04 ใน version 3.0)
- `project = SAM1 AND fixVersion = "2.0.0-evolution"` → 45 ใบ

## Worklogs

ไม่มี — สมาชิกยังไม่ได้ Log Work จึงไม่มีไฟล์ `jira_worklogs.csv` (AC ใน EVM ประมาณจากหลักฐานใน git)
