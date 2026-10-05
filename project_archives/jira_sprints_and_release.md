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

## Worklogs (จำลอง)

ลงใน Jira ครบ 45 ใบ เมื่อ 2026-10-05 ผ่าน Atlassian connector — **เป็นชั่วโมงประมาณการ ไม่ใช่ timesheet จริง**
ทุก worklog มีหมายเหตุ "⚠️ ชั่วโมงประมาณการ (จำลอง)" และถูกบันทึกในชื่อบัญชีที่เชื่อม connector (ไม่ใช่ชื่อสมาชิกแต่ละคน)

| Sprint | Issues | ชั่วโมง | ที่มา |
|---|---:|---:|---|
| Sprint 1 | 16 | 64.5 | 4 ชม./ใบ + งานทำซ้ำ PR #14→#19 0.5 ชม. (SAM1-24) |
| Sprint 2 | 19 | 67.0 | 4 ชม./ใบ · CR-02 4.5 · DEF-03 1.25 · DEF-01 0.75 · DEF-02 0.5 |
| Sprint 3 | 10 | 37.5 | 4 ชม./ใบ · UAT-DEF-01 1.5 |
| **รวม** | **45** | **169.0** | ตรงกับ AC ใน [Final EVM](../docs/week12/Final_EVM_and_Velocity_Report.md) |
