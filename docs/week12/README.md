# สัปดาห์ที่ 12 — UAT · Production Release · Final EVM & Close-out

| วิชา | หัวข้อ |
|---|---|
| ENGSE225 | UAT & Production Release (ISO/IEC 12207 · ISO/IEC 14764 · SemVer 2.0) |
| ENGSE202 | Final EVM & Procurement Close-out (PMBOK 7) |

## สิ่งส่งมอบ — เล่มรายงานฉบับรวม Phase 3

| ส่วน | วิชา | ชิ้นงาน | ไฟล์ | สถานะ |
|---|---|---|---|---|
| 1 | ENGSE225 | UAT Sign-off Sheet | [UAT_Test_Scenarios_and_Signoff.md](UAT_Test_Scenarios_and_Signoff.md) | ✅ รอบซ้อม 8/8 · ⬜ รอ Cross-team + ลายเซ็น |
| 1 | ENGSE225 | `main` + Tag `v2.0.0-evolution` | [Release_Runbook_v2.0.0-evolution.md](Release_Runbook_v2.0.0-evolution.md) · [Release Notes](Release_Notes_v2.0.0-evolution.md) | ⬜ ทำหลังได้ลายเซ็น UAT |
| 1 | ENGSE225 | CHANGELOG + รายงาน ISO/IEC 14764 | [CHANGELOG.md](../../CHANGELOG.md) · [Maintenance_Summary_Report_ISO14764.md](Maintenance_Summary_Report_ISO14764.md) | ✅ |
| 1 | ENGSE225 | PyTest 100% | [`evidence/regression_release_candidate.txt`](evidence/regression_release_candidate.txt) | ✅ บนเครื่อง · ⚠️ CI ติด billing |
| 2 | ENGSE202 | Final EVM + Velocity 3 Sprints | [Final_EVM_and_Velocity_Report.md](Final_EVM_and_Velocity_Report.md) | ✅ (ภาพจาก Jira ต้องแคปเอง) |
| 2 | ENGSE202 | Procurement Sheet + Reserve | [Procurement_Closeout_and_Reserve_Settlement.md](Procurement_Closeout_and_Reserve_Settlement.md) | ✅ |
| 3 | ENGSE202 | Phase 3 Completion Certificate | [Phase3_Completion_Certificate.md](Phase3_Completion_Certificate.md) | ⬜ รอลงนาม |

## ตัวเลขสำคัญ

| | |
|---|---|
| UAT รอบซ้อม | รอบ 1: 7/8 → พบ **UAT-DEF-01** → แก้ → รอบ 2: **8/8** |
| Tests | 167 → **173** · coverage 99% |
| Final EVM | PV = EV = 50,550 · AC = 50,700 🔶 · SPI 1.00 · CPI 0.997 |
| SPI ณ วันสิ้นสุดตามแผน | S1 **0.25** · S2 **1.00** · S3 **0.00** |
| Velocity | 16 → 19 → 10 issues |
| กันชน | ใช้ 9.0 / 12.0 ชม. · **คืน Sponsor 900 บาท** |
| ค่าเครื่องมือจริง | **0 บาท** |

## ⬜ งานที่ต้องทำเอง

- [ ] **Cross-team UAT** — ยื่น [UAT sheet ข้อ 5](UAT_Test_Scenarios_and_Signoff.md#5-cross-team-uat-ทำในห้องเรียน) ให้กลุ่มข้างเคียงทดสอบ เปิด CSV ใน Excel จริง แล้วลงนาม
- [ ] **Release** ตาม [Runbook](Release_Runbook_v2.0.0-evolution.md) ขั้นที่ 2–6 (push → PR → Tech Lead approve → tag → GitHub Release)
- [ ] **Jira:** ปิดใบ S3-01…09 + UAT-DEF-01 → Complete Sprint 3 → แคป Velocity Report และ Epic Burndown
- [ ] **Jira:** ทุกคน Log Work แล้วแก้ `actual_hours` ใน [`../data/project_metrics.json`](../data/project_metrics.json) → รัน `python tools/pm_metrics.py`
- [ ] พิมพ์ Phase 3 Completion Certificate และ Procurement Sheet ให้อาจารย์ลงนาม
