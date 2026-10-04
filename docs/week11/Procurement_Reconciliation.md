# ตารางกระทบยอดค่าใช้จ่ายเครื่องมือ (Procurement Reconciliation Sheet)
## ENGSE202 · สัปดาห์ที่ 11 · ชิ้นงานที่ 4 (ส่วนที่ 2)

| | |
|---|---|
| ผู้จัดทำ | ปวริศ คูณศรี (Project Manager) |
| วันที่กระทบยอด | 2026-10-05 |
| Cost Baseline ที่ใช้เทียบ | [Phase 2 Project Budget Worksheet](../../Phase2_Inventory_System_Report.md#5-project-budget-worksheet) — Infrastructure "GitHub / Local Environment" = **0 บาท** |

---

## 1. ตารางกระทบยอด

| Tool / Resource | Baseline | Actual | ผลต่าง | สถานะ / หลักฐาน |
|---|---:|---:|---:|---|
| Jira Software Cloud | 0 | 0 | 0 | Free plan (≤ 10 users) ทีมมี 4 คน — ตรวจที่ Administration → Billing |
| GitHub Repository | 0 | 0 | 0 | Public repository |
| GitHub Actions | 0 | 0 | 0 | ใช้จริง **0 นาที** — ดูข้อ 2 |
| Python 3 + pytest / flake8 / bandit / radon / pip-audit | 0 | 0 | 0 | Open source (ดูรายการใน [`requirements-dev.txt`](../../requirements-dev.txt)) |
| Cloud server / Database hosting | 0 | 0 | 0 | **ไม่ได้ใช้** — โปรแกรมเป็น CLI รันบนเครื่องผู้ใช้ เก็บข้อมูลเป็นไฟล์ JSON |
| **รวมค่าเครื่องมือสุทธิ** | **0** | **0** | **0** | 🟢 ตรงตาม Baseline |

ตัวเลขเก็บไว้ที่ [`../data/project_metrics.json`](../data/project_metrics.json) หัวข้อ `tools`

> **ทำไมไม่มีรายการ Cloud Hosting เหมือนตัวอย่างในใบงาน** — ตัวอย่างในสไลด์มีค่า Cloud Server 500 บาท
> แต่โครงการนี้ไม่เคยเช่า server เลย ทีมจึงบันทึกตามจริงว่า 0 บาท แทนการใส่ตัวเลขตามตัวอย่าง

## 2. ภาระผูกพันค้างจ่าย — GitHub billing lock

| | |
|---|---|
| อาการ | ทุก workflow run ขึ้น *"The job was not started because your account is locked due to a billing issue."* ตั้งแต่สัปดาห์ที่ 9 |
| ผลต่อเงิน | ไม่มียอดเรียกเก็บในโครงการนี้ (repo เป็น public และใช้ Actions จริง 0 นาที) |
| ผลต่อคุณภาพ | DoD ข้อ "PyTest บน CI/CD" ไม่ผ่านใน Sprint 2 |
| สิ่งที่ต้องทำก่อนปิดสัญญา | เจ้าของบัญชีตรวจ Settings → Billing and plans ว่ามียอดค้างจากที่อื่นหรือไม่ แล้วเคลียร์ให้ Actions กลับมารัน |
| ผู้รับผิดชอบ | เจ้าของบัญชี GitHub `PeawZaZa` |

## 3. ข้อสังเกตจากการกระทบยอด — อัตราค่าแรงในเอกสารไม่ตรงกัน

| เอกสาร | อัตราค่าแรง | กันชน |
|---|---|---|
| [Phase 2 Budget Worksheet](../../Phase2_Inventory_System_Report.md#5-project-budget-worksheet) (สัปดาห์ที่ 5–7) | 500 บาท/ชม. | 20% |
| [EVM Analysis](../EVM_Analysis.md) และ [Contingency Log](../Contingency_Reserve_Log.md) (สัปดาห์ที่ 9–10) | 300 บาท/ชม. 🔶 | 10% (12 ชม.) |

ตัวเลข EVM ตั้งแต่สัปดาห์ที่ 9 ใช้ 300 บาท/ชม. มาตลอด เพื่อให้เทียบกันได้ต่อเนื่อง
**รายงานฉบับนี้และฉบับต่อไปจึงใช้ 300 บาท/ชม. ต่อ**

> **ข้อเสนอ:** ให้ PM ยืนยันกับ Sponsor ว่าจะยึดอัตราใดเป็น Cost Baseline ทางการ
> ถ้าเปลี่ยนเป็น 500 บาท/ชม. ให้แก้ค่า `labor_rate_thb_per_hour` ใน `project_metrics.json`
> แล้วรัน `python tools/pm_metrics.py` ตัวเลข EVM / ROI ทุกตารางจะคำนวณใหม่อัตโนมัติ
> (ค่า SPI/CPI จะไม่เปลี่ยน เพราะ PV EV AC คูณอัตราเดียวกันทั้งหมด — เปลี่ยนเฉพาะยอดเงิน)

## 4. สถานะงบสำรอง (Contingency Reserve)

| รายการ | ชม. | บาท |
|---|---:|---:|
| ยอดตั้งต้น (10% ของแผน 120 ชม.) | 12.0 | 3,600 |
| CR-2026-001 แก้ DEF-01/02/03 (สัปดาห์ที่ 10) | −2.5 | −750 |
| CR-2026-002 CR-02 Export CSV (สัปดาห์ที่ 10) | −4.5 | −1,350 |
| **คงเหลือ ณ สิ้น Sprint 2** | **5.0** | **1,500** |

**มาตรการสำหรับ Sprint 3** — ยอด 5.0 ชม. ถูก**ล็อกไว้สำหรับแก้ข้อบกพร่องจาก UAT และงาน Hardening เท่านั้น**
ห้ามใช้กับฟีเจอร์ใหม่ตาม [Scope Freeze Agreement](Scope_Freeze_Agreement.md)
ยอดที่เหลือ ณ วันปิดโครงการจะคืนให้ Sponsor

## 5. ลงนามรับรอง

| บทบาท | ชื่อ | ลายมือชื่อ | วันที่ |
|---|---|---|---|
| Project Manager | ปวริศ คูณศรี | | |
| Project Sponsor | | | |
