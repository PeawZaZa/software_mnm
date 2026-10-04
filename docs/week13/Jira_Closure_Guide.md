# คู่มือปิดกระดาน Jira และ Release Version 2.0.0
## ENGSE202 สัปดาห์ที่ 13 · ชิ้นงานที่ 3

ขั้นตอนนี้**ต้องกดเองใน Jira** (`https://nicky2011abcd.atlassian.net` · project `SAM1`)
ทำต่อจากขั้นตอนใน [`../JIRA_SETUP.md`](../JIRA_SETUP.md) และ checklist ของ [สัปดาห์ที่ 11](../week11/README.md) / [12](../week12/README.md)

---

## 0. สถานะปัจจุบัน (ตรวจผ่าน Atlassian connector 2026-10-05)

| รายการ | สถานะ |
|---|---|
| Sprint 1 · Sprint 2 | ✅ Closed |
| Sprint 3 (SAM1-49…58) | 🟢 Active · Done 9/10 · เหลือ **SAM1-56 Release** (In Progress — ปิดหลัง merge เข้า `main` + tag) |
| Version `2.0.0-evolution` | ✅ สร้างแล้ว (Unreleased) |
| Version `3.0` + FB-01…04 (SAM1-59…62) | ✅ สร้างแล้ว อยู่ใน Backlog ไม่อยู่ใน sprint |
| Fix version ของงานที่ส่งมอบ | ⬜ ทำด้วย Bulk change (ข้อ 3) |
| Log Work | ⬜ สมาชิกต้องลงเอง — ห้ามลงแทนกัน |

## 1. ตรวจ Zero Open Tasks

ค้นด้วย JQL (Filters → Advanced issue search):

```
project = SAM1 AND statusCategory != Done
```

ต้องได้ **0 issues** ถ้ายังเหลือ ให้ปิดหรือย้ายเข้า Future Backlog ดังนี้

| ประเภทใบที่ค้าง | ทำอย่างไร |
|---|---|
| งาน Sprint 3 ที่ทำเสร็จแล้วใน git | ย้ายเป็น Done แล้วใส่ลิงก์ commit ในคอมเมนต์ (ดูตาราง [Maintenance Summary 2.3](../week12/Maintenance_Summary_Report_ISO14764.md#23-sprint-3--สัปดาห์ที่-1112-hardening--release)) |
| คำขอใหม่ (FB-01…04) | สร้างเป็น issue พร้อม label `future-backlog-v3` แล้วตั้ง Fix version = `3.0` — **ไม่อยู่ใน sprint ใด** |
| DEF-04 | ตั้ง Resolution = *Won't Do (accepted)* พร้อมอ้าง Known Issue KI-04 |

## 2. ตรวจทุก Sprint ปิดแล้ว

Backlog → ไม่ควรเหลือ sprint ที่ Active
Reports → **Sprint Report** เลือกทีละ sprint ต้องเห็น Completed ครบ

## 3. สร้างและ Release Version 2.0.0

1. เมนูซ้าย → **Releases** (team-managed: *Project settings → Features → Releases* ต้องเปิดก่อน)
2. **Create version** → Name `2.0.0-evolution` · Start date `2026-06-29` · Release date = วันที่ merge เข้า `main` จริง
3. Filters → ค้น JQL `project = SAM1 AND key <= SAM1-58 AND fixVersion is EMPTY` → **Bulk change** → Edit → Fix versions = `2.0.0-evolution`
4. กลับไปหน้า Releases → กด **Release** → ใส่วันที่ → **Release**
5. แคปหน้า Release report ที่เห็น 100% issues done

## 4. ภาพหลักฐานที่ต้องเก็บ

| ภาพ | เก็บที่ |
|---|---|
| ผล JQL = 0 issues | `docs/week13/evidence/jira_zero_open.png` |
| Board ทุกการ์ดอยู่ช่อง Done | `docs/week13/evidence/jira_board_done.png` |
| Release `2.0.0-evolution` สถานะ Released | `docs/week13/evidence/jira_release.png` |
| Project dashboard / Summary | `docs/week13/evidence/jira_dashboard.png` |

## Checklist

- [ ] JQL `statusCategory != Done` = 0
- [ ] Sprint 1 · 2 · 3 Completed
- [ ] Future Backlog FB-01…04 อยู่ใน version `3.0` ไม่อยู่ใน sprint
- [ ] Version `2.0.0-evolution` Released
- [ ] แคปภาพครบ 4 ภาพ
