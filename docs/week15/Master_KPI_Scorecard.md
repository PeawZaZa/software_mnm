# Master Project KPI Scorecard (ฉบับทางการ)
## ENGSE202 สัปดาห์ที่ 15 · ชิ้นงานที่ 2

| | |
|---|---|
| ผู้จัดทำ | ปวริศ คูณศรี (PM) |
| วันที่ | 2026-10-05 |
| ฉบับก่อนหน้า | [KPI Scorecard สัปดาห์ที่ 13](../week13/Project_KPI_Scorecard.md) — ฉบับนี้เพิ่มผล pip-audit และ DR drill |

## 4 มิติแห่งความสำเร็จ

| มิติ | สรุป | สถานะ |
|---|---|---|
| **1 Schedule** | SPI ณ วันงานเสร็จ 1.00 แต่ **SPI ณ วันตามแผน 0.25 / 1.00 / 0.00** · ตรงเวลา 1 จาก 3 sprints | 🔴 |
| **2 Cost** | CPI 0.997 🔶 · ค่าเครื่องมือ 0 บาท · คืนเงินสำรอง 900 บาท | 🟡 |
| **3 Quality** | Coverage 99% · v(G) 14 → 7 · global 0 · flake8 / bandit / CVEs = 0 · ติดตั้งสด 21 วิ | 🏆 |
| **4 Stakeholder** | Scope 100% · UAT รอบแรก 7/8 → 8/8 · ROI คืนทุน 26.8 เดือน | 🟡 |

## ตาราง Master Scorecard

| หมวด | ตัวชี้วัด | Target | Actual | สถานะ |
|---|---|---:|---:|---|
| Schedule | SPI (at completion) | 1.00 | 1.00 | 🟢 |
| Schedule | SPI ณ วันสิ้นสุดตามแผน (S1/S2/S3) | 1.00 | 0.25 / 1.00 / 0.00 | 🔴 |
| Schedule | Sprint ปิดตรงกำหนด | 3/3 | 1/3 | 🔴 |
| Cost | CPI | ≥ 0.95 | 0.997 🔶 | 🟡 |
| Cost | ค่าเครื่องมือ | ≤ 0 บาท | 0 บาท | 🟢 |
| Cost | เงินสำรองไม่ติดลบ · คืน Sponsor | ≥ 0 | +900 บาท | 🟢 |
| Quality | PyTest coverage | ≥ 90% | 99% | 🏆 |
| Quality | Max Cyclomatic Complexity | ≤ 8 | 7 | 🟢 |
| Quality | Coupling (CBO) | ≤ 4 | 2 | 🟢 |
| Quality | Global mutable state | 0 | 0 | 🟢 |
| Quality | Flake8 / Bandit | 0 / 0 | 0 / 0 | 🟢 |
| Technical | Third-party vulnerabilities (pip-audit) | 0 CVEs | 0 CVEs | 🟢 |
| Technical | Clean deployment (สด) | ≤ 2 นาที | 21 วิ (ซ้อม) | 🟢 |
| Technical | Recoverability RTO | อัตโนมัติ | 0.15 วิ · RPO 1 รายการ | 🟢 |
| Technical | Critical/High defects ค้าง | 0 | 0 — REL-01 แก้แล้วเมื่อ merge release เข้า `main` | 🟢 |
| Business | Scope delivery (CR-01 · CR-02) | 100% | 100% | 🟢 |
| Business | UAT first-time pass | 100% | 87.5% → 100% | 🟡 |
| Business | UAT รอบตรวจรับ | 100% (Cross-team) | 8/8 แบบจำลองโดยทีม — ไม่มี Cross-team | 🟡 |
| Business | Sponsor satisfaction | ≥ 4/5 | ______ | ⬜ |
| Business | ROI 3 ปี | > 0 | +34.2% | 🟢 |

**สรุป 20 ตัวชี้วัด:** 🟢/🏆 14 · 🟡 3 · 🔴 2 · ⬜ 1 (Sponsor satisfaction กรอกหลังนำเสนอ)

> ทีมเลือกรายงานมิติเวลาว่า**ไม่ผ่าน** ทั้งที่ใช้ SPI ปลายทาง 1.00 ได้ — เพราะความจริงคือส่งช้า 2 ใน 3 sprints
> และนี่คือบทเรียนอันดับหนึ่งที่ส่งต่อให้โครงการถัดไป
