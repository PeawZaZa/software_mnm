# Project Archives — Organizational Process Assets (OPAs)

คลังสินทรัพย์กระบวนการของโครงการ **Mini Inventory System Evolution** (มิ.ย.–ต.ค. 2026)
จัดเก็บไว้ให้โครงการถัดไปหยิบไปใช้ซ้ำ — ทุกลิงก์ชี้ไปที่ไฟล์จริงใน repository นี้

| | |
|---|---|
| ผู้ดูแลคลัง | ปวริศ คูณศรี (PM) |
| วันที่จัดเก็บ | 2026-10-05 |
| สถานะ | ปิดรับการแก้ไขหลังลงนาม Final Project Acceptance (สัปดาห์ที่ 15) |

---

## 1. แม่แบบพร้อมใช้ ([`templates/`](templates/))

ปรับจากเอกสารจริงของโครงการนี้ โดยใส่บทเรียนเข้าไปแล้ว

| แม่แบบ | ใช้เมื่อ | ปรับปรุงจากต้นฉบับอย่างไร |
|---|---|---|
| [Definition_of_Done.md](templates/Definition_of_Done.md) | เริ่มโครงการ | ทุกข้อมี**กลไกบังคับ**กำกับ (บทเรียนหลักของโครงการ) |
| [Change_Request_Impact_Form.md](templates/Change_Request_Impact_Form.md) | มีคำขอเปลี่ยนแปลง | ใช้ได้จริงกับ CR-02 — อนุมัติได้ในวันเดียว |
| [UAT_Signoff_Sheet.md](templates/UAT_Signoff_Sheet.md) | ก่อน release | เพิ่มช่องแยก Defect / New Scope |
| [Lessons_Learned_Register.md](templates/Lessons_Learned_Register.md) | ปลายทุกเฟส | 5 คอลัมน์ตาม PMI + ช่องหลักฐาน |

## 2. สินทรัพย์ด้านการบริหาร (PM Artifacts)

| สินทรัพย์ | ไฟล์ |
|---|---|
| RACI Matrix + DoD ฉบับแรก + GitFlow guide | [`phase1 3 report.md`](../phase1%203%20report.md) |
| Risk Register + Data Flow Diagram | [`combined_report_phase1_2.md`](../combined_report_phase1_2.md) |
| WBS (INV-4…14) + Man-hours + Budget worksheet | [`Phase2_Inventory_System_Report.md`](../Phase2_Inventory_System_Report.md) |
| EVM (snapshot Sprint 1 · Final 3 sprints) | [`docs/EVM_Analysis.md`](../docs/EVM_Analysis.md) · [`docs/week12/Final_EVM_and_Velocity_Report.md`](../docs/week12/Final_EVM_and_Velocity_Report.md) |
| Contingency Reserve Log + Settlement | [`docs/Contingency_Reserve_Log.md`](../docs/Contingency_Reserve_Log.md) · [`docs/week12/Procurement_Closeout_and_Reserve_Settlement.md`](../docs/week12/Procurement_Closeout_and_Reserve_Settlement.md) |
| KPI Scorecard · ROI | [`docs/week13/Project_KPI_Scorecard.md`](../docs/week13/Project_KPI_Scorecard.md) · [`docs/week14/Benefit_Realization_ROI_Report.md`](../docs/week14/Benefit_Realization_ROI_Report.md) |
| เครื่องคำนวณ EVM / Reserve / ROI / กราฟ | [`tools/pm_metrics.py`](../tools/pm_metrics.py) + [`docs/data/project_metrics.json`](../docs/data/project_metrics.json) |

## 3. สินทรัพย์ด้านเทคนิค (Technical Artifacts)

| สินทรัพย์ | ไฟล์ |
|---|---|
| CI workflow (flake8 · bandit · coverage gate · matrix) | [`.github/workflows/pytest.yml`](../.github/workflows/pytest.yml) |
| Linter rules | [`.flake8`](../.flake8) · [`pytest.ini`](../pytest.ini) |
| สคริปต์ติดตั้งคำสั่งเดียว | [`setup.sh`](../setup.sh) · [`setup.ps1`](../setup.ps1) · [`.env.example`](../.env.example) |
| แพ็กเกจ / container | [`pyproject.toml`](../pyproject.toml) · [`MANIFEST.in`](../MANIFEST.in) · [`Dockerfile`](../Dockerfile) |
| UAT runner ผ่าน CLI จริง | [`tools/run_uat.py`](../tools/run_uat.py) |
| คู่มือ O&M + Dossier | [`docs/System_Operations_and_Maintenance_Manual.md`](../docs/System_Operations_and_Maintenance_Manual.md) · [`docs/Final_System_Maintenance_Dossier.md`](../docs/Final_System_Maintenance_Dossier.md) |

## 4. สินทรัพย์ด้าน Governance

| สินทรัพย์ | ไฟล์ |
|---|---|
| CR Impact Form (ตัวอย่างจริง) · CCB Minutes | [`docs/CR-02_Impact_and_Decision_Form.md`](../docs/CR-02_Impact_and_Decision_Form.md) · [`docs/CCB_Meeting_Minutes.md`](../docs/CCB_Meeting_Minutes.md) |
| Scope Freeze Agreement | [`docs/week11/Scope_Freeze_Agreement.md`](../docs/week11/Scope_Freeze_Agreement.md) |
| UAT Sheet · Release Runbook | [`docs/week12/UAT_Test_Scenarios_and_Signoff.md`](../docs/week12/UAT_Test_Scenarios_and_Signoff.md) · [`docs/week12/Release_Runbook_v2.0.0-evolution.md`](../docs/week12/Release_Runbook_v2.0.0-evolution.md) |
| Audit logs (เครื่องมือ · drill · install) | [`docs/week11/evidence/`](../docs/week11/evidence/) · [`docs/week12/evidence/`](../docs/week12/evidence/) · [`docs/week13/evidence/`](../docs/week13/evidence/) · [`docs/week14/evidence/`](../docs/week14/evidence/) |
| Defect Log | [`docs/Defect_Log.md`](../docs/Defect_Log.md) |

## 5. ฐานความรู้

| | |
|---|---|
| Lessons Learned Register (11 รายการ) | [`docs/week13/Lessons_Learned_Register.md`](../docs/week13/Lessons_Learned_Register.md) |
| Lessons Learned Compendium (3 ระดับ + Top 5 นโยบาย) | [`docs/week14/Lessons_Learned_Compendium.md`](../docs/week14/Lessons_Learned_Compendium.md) |
| ข้อมูลอ้างอิงสำหรับประมาณการครั้งหน้า | Velocity 16 / 19 / 10 issues ต่อ sprint · ~3.8 ชม./issue · CR ขนาดกลาง ~4.5 ชม. · Review queue เฉลี่ย 96 นาทีเมื่อ WIP = 5 |

## 6. Jira Export

| ไฟล์ | เนื้อหา |
|---|---|
| [`jira_all_issues.csv`](jira_all_issues.csv) | งานทั้ง 49 ใบ — key · type · status · assignee · sprint · fix version (UTF-8 BOM เปิดใน Excel ได้) |
| [`jira_sprints_and_release.md`](jira_sprints_and_release.md) | Sprint 1–3 · velocity · release `2.0.0-evolution` · ข้อผิดพลาด SAM1-39 ใน Sprint 3 |

> ⬜ ภาพหน้าจอ Velocity / Burndown / Release report ต้องแคปจาก Jira เอง (เบราว์เซอร์ของผู้ช่วยไม่ได้ล็อกอิน Atlassian)
