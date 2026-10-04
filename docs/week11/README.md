# สัปดาห์ที่ 11 — System Hardening · Flow Metrics · Scope Freeze

| วิชา | หัวข้อ |
|---|---|
| ENGSE225 | System Hardening & Code Freeze (ISO/IEC/IEEE 12207) |
| ENGSE202 | Flow Metrics (CFD / Burnup) & Scope Freeze (PMBOK 7) |

## สิ่งส่งมอบ

| # | วิชา | ชิ้นงาน | ไฟล์ | สถานะ |
|---|---|---|---|---|
| 1 | ENGSE225 | รายงานสแกนความปลอดภัย Static Analysis + ซอร์สโค้ดบน `develop` | [Security_Static_Analysis_Report.md](Security_Static_Analysis_Report.md) · [`app_v2.py`](../../app_v2.py) | ✅ |
| 2 | ENGSE225 | Full Regression Test Suite + ผลรัน PyTest 100% (coverage ≥ 90%) | [Regression_Test_Report.md](Regression_Test_Report.md) · [`test_hardening.py`](../../test_hardening.py) | ✅ (ภาพหน้าจอต้องแคปเอง) |
| 3 | ENGSE202 | วิเคราะห์ CFD / Burnup + บันทึกปิด Sprint 2 | [Flow_Metrics_and_Sprint2_Closure.md](Flow_Metrics_and_Sprint2_Closure.md) | ✅ |
| 4 | ENGSE202 | สัญญา Scope Freeze + ตาราง Procurement | [Scope_Freeze_Agreement.md](Scope_Freeze_Agreement.md) · [Procurement_Reconciliation.md](Procurement_Reconciliation.md) | ✅ (รอลงนาม) |

หลักฐานดิบจากเครื่องมือ: [`evidence/`](evidence/)

## ตัวเลขสำคัญ

| | ก่อน | หลัง |
|---|---:|---:|
| Flake8 | 270 | **0** |
| Bandit (High/Med/Low) | 0/0/0 | **0/0/0** |
| Tests | 148 | **167** |
| Coverage | 98% | **99%** |
| Max v(G) | 9 | **6** |
| ข้อบกพร่องแฝงที่พบและแก้ | — | **2** |
| WIP สูงสุดในช่อง Review (Sprint 1) | | **5 PR** · รอเฉลี่ย 96 นาที |
| Sprint 2 Burnup | | **19/19 (100%)** |

## ⬜ งานที่ต้องทำเอง (เครื่องมือทำแทนไม่ได้)

- [ ] **Jira:** Complete Sprint 2 → แคป Velocity Report
- [ ] **Jira:** สร้าง Sprint 3 + issue S3-01…S3-09 → Start Sprint (2026-09-08 → 2026-09-21)
- [ ] **Jira:** Board settings → Columns → ตั้ง Max = 3 ที่คอลัมน์ In Review (WIP Limit)
- [ ] **Jira:** Reports → Cumulative flow diagram → แคปหน้าจอแนบเพิ่ม
- [ ] **GitHub:** Settings → Branches → Branch protection ของ `develop` และ `main`
      เลือก *Require a pull request before merging* + *Require approvals: 1* + *Require status checks: PyTest CI*
- [ ] **GitHub:** เคลียร์ billing ให้ Actions กลับมารัน
- [ ] แคปหน้าจอ `pytest -v --cov=app_v2` → `evidence/pytest_screenshot.png`
- [ ] พิมพ์ Scope Freeze Agreement และ Procurement Sheet ให้อาจารย์ลงนาม
- [ ] ทุกคน Log Work ใน Jira ย้อนหลัง Sprint 2–3 แล้วแก้ `actual_hours` ใน [`../data/project_metrics.json`](../data/project_metrics.json)
