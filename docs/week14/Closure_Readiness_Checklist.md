# Project Closure Readiness Checklist — 4 เสาหลัก
## ENGSE202 สัปดาห์ที่ 14 · ชิ้นงานที่ 2

| | |
|---|---|
| ผู้ตรวจ | ปวริศ คูณศรี (PM) |
| วันที่ตรวจ | 2026-10-05 |
| เกณฑ์ | ทุกข้อต้องเป็น ✅ ก่อนลงนาม Final Project Acceptance ในสัปดาห์ที่ 15 |

สัญลักษณ์: ✅ ผ่าน (มีหลักฐาน) · ⬜ ยังไม่ทำ — ต้องทำโดยคน · ⚠️ ผ่านแบบมีข้อจำกัด

---

## เสาที่ 1 — Scope & Quality

| # | รายการ | สถานะ | หลักฐาน |
|---|---|---|---|
| 1.1 | ทุกงานในเกณฑ์ DoD ทำเสร็จในโค้ด | ✅ | 45/45 issues · [Final EVM](../week12/Final_EVM_and_Velocity_Report.md) |
| 1.2 | การ์ด Jira ทุกใบใน Sprint 1–3 เป็น Done | ⬜ | ทำตาม [Jira Closure Guide](../week13/Jira_Closure_Guide.md) |
| 1.3 | CR-01 และ CR-02 ถูกรวมเข้า `main` | ✅ | `main` @ `34747aa` · tag `v2.0.0-evolution` |
| 1.4 | PyTest Full Suite 100% | ✅ | 195 passed · coverage 99% |
| 1.5 | ผ่านการติดตั้งบน Clean Environment | ✅ | [Week 13 report](../week13/Clean_Environment_Installation_Report.md) — 25 วิ / 19 วิ |
| 1.6 | ไม่มีข้อบกพร่อง Critical/High ค้างบน production | ✅ | REL-01 แก้แล้ว — `main` ผ่าน 173 เทสต์ |
| 1.7 | pip-audit 0 CVEs · Bandit 0 | ✅ | [DR & Security Report](DR_and_Dependency_Security_Report.md) |

## เสาที่ 2 — Financial

| # | รายการ | สถานะ | หลักฐาน |
|---|---|---|---|
| 2.1 | สมาชิกทุกคน Log Work ใน Jira ครบ 100% | ⬜ | ยังไม่มี — AC ใช้ค่าประมาณตามหลักฐาน |
| 2.2 | AC กระทบยอดกับชั่วโมงจริง | ⚠️ | 50,700 บาท 🔶 — ยืนยันได้หลัง 2.1 |
| 2.3 | สรุปผลต่าง CV | ✅ | CV = −150 บาท (Sprint 1 งานทำซ้ำ) |
| 2.4 | ตัดยอดเงินสำรองและสรุปยอดคงเหลือ | ✅ | ใช้ 9.0 / 12.0 ชม. · คงเหลือ **900 บาท** |
| 2.5 | ทำเรื่องคืนเงินสำรองคงเหลือให้ Sponsor | ⬜ | ระบุในใบ Final Acceptance สัปดาห์ที่ 15 |
| 2.6 | ไม่มีหนี้สินค้างทางการเงิน | ✅ | ค่าเครื่องมือจริง 0 บาท |

## เสาที่ 3 — Contractual & Tools

| # | รายการ | สถานะ | หลักฐาน |
|---|---|---|---|
| 3.1 | Final Procurement Reconciliation ครบทุกรายการ | ✅ | [Procurement Close-out](../week12/Procurement_Closeout_and_Reserve_Settlement.md) |
| 3.2 | GitHub Actions ไม่เกิน Free tier | ✅ | ใช้ 0 นาที |
| 3.3 | ไม่มีภาระผูกพันหรือค่าบริการค้างจ่าย | ⚠️ | ฝั่งโครงการไม่มี — แต่บัญชี GitHub ติด **billing lock** ต้องให้เจ้าของบัญชีตรวจ |
| 3.4 | ปิดฐานข้อมูลทดสอบ / Mock server | ✅ | ไม่มีให้ปิด — เทสต์ใช้ `tmp_path` และไม่เรียกเครือข่าย |
| 3.5 | คงไว้เฉพาะ repository หลัก | ⬜ | ลบสาขาชั่วคราว 16 สาขาหลังแท็ก (สัปดาห์ที่ 15) |

## เสาที่ 4 — Stakeholder Acceptance

| # | รายการ | สถานะ | หลักฐาน |
|---|---|---|---|
| 4.1 | UAT Sign-off มีลายเซ็นผู้ใช้ | ⬜ | UAT จำลอง 8/8 · รอลายเซ็น |
| 4.2 | Scope Freeze ถูกปฏิบัติตาม | ✅ | ไม่มีฟีเจอร์ใหม่หลัง 5 ต.ค. — คำขอใหม่อยู่ใน Future Backlog |
| 4.3 | Phase 3 Completion Certificate ลงนาม | ⬜ | [ใบรับรอง](../week12/Phase3_Completion_Certificate.md) รอลงนาม |
| 4.4 | Pre-Audit Maintenance Dossier ลงนาม | ⬜ | [Dossier](../Final_System_Maintenance_Dossier.md) |
| 4.5 | ร่าง Final Project Acceptance Certificate | ✅ | [สัปดาห์ที่ 15](../week15/Final_Project_Acceptance_Certificate.md) |

---

## สรุป

| เสา | ✅ | ⚠️ | ⬜ |
|---|---:|---:|---:|
| Scope & Quality | 6 | 0 | 1 |
| Financial | 3 | 1 | 2 |
| Contractual & Tools | 3 | 1 | 1 |
| Stakeholder | 2 | 0 | 3 |
| **รวม 23 ข้อ** | **14** | **2** | **7** |

**ยังไม่พร้อมปิดโครงการ** — 7 ข้อที่ค้างทั้งหมดเป็นงานที่*คนต้องทำ* (กดใน Jira/GitHub · ลงนาม · Log Work)
ไม่มีงานค้างด้านโค้ดหรือเอกสาร ลำดับที่แนะนำก่อนสัปดาห์ที่ 15:

1. ลายเซ็น UAT (4.1) → เปิด PR release เข้า `main` (1.3 · แก้ 1.6 พร้อมกัน)
2. Log Work ทุกคน (2.1) → รัน `tools/pm_metrics.py` ใหม่ (2.2)
3. ปิดการ์ด Jira + Release version (1.2) → Archive project
4. ลงนามเอกสาร 4.3 · 4.4 และเตรียม 2.5 ในใบ Final Acceptance
