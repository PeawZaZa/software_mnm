# สัปดาห์ที่ 14 — Packaging · Disaster Recovery · Benefit Realization

| วิชา | หัวข้อ |
|---|---|
| ENGSE225 | Packaging, Disaster Recovery & Pre-Closure Audit (ISO/IEC 12207 6.4.10 · 14764 · 25010) |
| ENGSE202 | Benefit Realization & Closure Audit (PMBOK 7) |

## สิ่งส่งมอบ

| # | วิชา | ชิ้นงาน | ไฟล์ | สถานะ |
|---|---|---|---|---|
| 1 | ENGSE225 | DR & Dependency Security Report | [DR_and_Dependency_Security_Report.md](DR_and_Dependency_Security_Report.md) | ✅ |
| 2 | ENGSE225 | Complete Maintenance Dossier (3 ภาค) | [`../Final_System_Maintenance_Dossier.md`](../Final_System_Maintenance_Dossier.md) | ✅ รอลงนาม Pre-Audit |
| 3 | ENGSE225 | Wheel + sdist + Dockerfile | [`artifacts/`](artifacts/) · [`pyproject.toml`](../../pyproject.toml) · [`Dockerfile`](../../Dockerfile) | ✅ wheel ทดสอบแล้ว · ⚠️ Docker ยังไม่ build |
| 1 | ENGSE202 | Benefit Realization & ROI | [Benefit_Realization_ROI_Report.md](Benefit_Realization_ROI_Report.md) | ✅ |
| 2 | ENGSE202 | Closure Readiness Checklist 4 เสา | [Closure_Readiness_Checklist.md](Closure_Readiness_Checklist.md) | ✅ 14/23 ผ่าน · 7 รอคนทำ |
| 3 | ENGSE202 | OPAs + Lessons Compendium | [`../../project_archives/`](../../project_archives/README.md) · [Lessons_Learned_Compendium.md](Lessons_Learned_Compendium.md) | ✅ |
| 4 | ENGSE202 | หลักฐานปิดบอร์ด Jira + Export | ข้อด้านล่าง | ⬜ |
| — | ENGSE202 | โครงร่างสไลด์ Final Defense | [Final_Defense_Storyboard.md](Final_Defense_Storyboard.md) | ✅ |

## ตัวเลขสำคัญ

| | |
|---|---|
| Tests | 186 → **195** · coverage 99% · max v(G) 7 |
| pip-audit | **0 CVEs** / 17 แพ็กเกจ · runtime deps 0 |
| Data drill | RTO **0.15 วิ** · RPO 1 รายการ |
| Git rollback drill | RTO **1.4 วิ** — พบ **REL-01** `main` เดิมเสีย 24 เทสต์ |
| ROI | ปีแรก −55.3% · 3 ปี +34.2% · คืนทุน **26.8 เดือน** |
| Closure readiness | ✅ 14 · ⚠️ 2 · ⬜ 7 (หลัง release) |

## ⬜ งานที่ต้องทำเอง

- [ ] **Docker:** สมาชิกที่มี Docker Desktop `docker build -t mini-inventory:v2.0.1 .` + `docker run -it --rm mini-inventory:v2.0.1` → แคปภาพ `evidence/docker_run.png`
- [ ] **Jira Archive:** Project settings → Archive project (ทำ**หลัง**สัปดาห์ที่ 15) · Filters → All issues → Export CSV (all fields) → `project_archives/jira_all_issues.csv`
- [ ] **Jira:** Reports → Velocity / Epic burndown → แคปภาพเก็บใน `project_archives/`
- [ ] ให้อาจารย์ลงนาม Pre-Audit ท้าย [Dossier](../Final_System_Maintenance_Dossier.md)
- [ ] ทำสไลด์ตาม [Storyboard](Final_Defense_Storyboard.md)
