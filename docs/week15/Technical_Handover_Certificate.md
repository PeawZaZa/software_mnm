# Technical Handover Certificate
## ENGSE225 สัปดาห์ที่ 15 · ชิ้นงานที่ 4 — ISO/IEC/IEEE 12207 Clause 6.4.10 Transition

| | |
|---|---|
| ระบบ | Mini Inventory System `v2.0.1-evolution` (Production baseline `v2.0.0-evolution`) |
| Repository | https://github.com/PeawZaZa/software_mnm |
| ผู้ส่งมอบ | ทีมพัฒนา (PM · Tech Lead · QA · Developer) |
| ผู้รับมอบ | อาจารย์ผู้สอน (Project Sponsor) |

---

## 1. Artifacts Handover

| รายการ | ที่อยู่ | ตรวจ |
|---|---|---|
| Source code | สาขา `main` + แท็ก `v2.0.0-evolution` · `v2.0.1-evolution` | ☐ |
| ชุดทดสอบ (195 เคส · coverage 99%) | `test_*.py` · `pytest.ini` | ☐ |
| สคริปต์ build/deploy | `setup.sh` · `setup.ps1` · `pyproject.toml` · `Dockerfile` | ☐ |
| Release packages | [`docs/week14/artifacts/`](../week14/artifacts/) — wheel + sdist + SHA256 | ☐ |
| CI workflow | `.github/workflows/pytest.yml` | ☐ |

## 2. Operational Handover

| รายการ | รายละเอียด | ตรวจ |
|---|---|---|
| สิทธิ์ดูแล GitHub | โอน Owner ให้ Sponsor ตามข้อ 4 | ☐ |
| การตั้งค่า | `.env.example` + Environment Inventory ข้อ 5 | ☐ |
| แผนรับมือภัยพิบัติ | Auto-backup `.bak` · Rollback ไปแท็กที่ผ่านเทสต์ — ซ้อมแล้ว ([DR Report](../week14/DR_and_Dependency_Security_Report.md)) | ☐ |

## 3. Knowledge Handover

| รายการ | ไฟล์ | ตรวจ |
|---|---|---|
| Operations & Maintenance Manual (7 บท) | [`../System_Operations_and_Maintenance_Manual.md`](../System_Operations_and_Maintenance_Manual.md) | ☐ |
| Final System Maintenance Dossier (7 หมวด) | [`../Final_System_Maintenance_Dossier.md`](../Final_System_Maintenance_Dossier.md) | ☐ |
| As-Built Architecture | Manual บทที่ 2 | ☐ |
| Troubleshooting Matrix | Manual บทที่ 5.3 | ☐ |
| Escalation Path | Manual บทที่ 7.4 | ☐ |

## 4. Repository Ownership Transfer (เจ้าของบัญชี `PeawZaZa` ทำ)

| # | ขั้นตอน | ที่ไหน | ตรวจ |
|---|---|---|---|
| 1 | ตั้ง Branch Protection บน `main` และ `develop`: PR required · 1 approval · status check `PyTest CI` · ห้าม bypass | Settings → Branches | ☐ |
| 2 | ยืนยันแท็ก `v2.0.0-evolution` และ `v2.0.1-evolution` อยู่บน remote | Releases / Tags | ☐ |
| 3 | ลบสาขาชั่วคราวที่ merge แล้ว (16 สาขา) — คงไว้ `main` · `develop` | Branches → 🗑 หรือ `git push origin --delete <branch>` | ☐ |
| 4 | เพิ่มอาจารย์เป็น collaborator แล้ว **Transfer ownership** หรือเพิ่มเป็น Admin | Settings → Collaborators / Danger Zone → Transfer | ☐ |
| 5 | ลดสิทธิ์สมาชิกทีมเป็น Write / Maintain | Settings → Collaborators | ☐ |
| 6 | เคลียร์ billing lock ให้ GitHub Actions ทำงาน แล้วยืนยันว่ามี run สีเขียวบน `main` | Settings → Billing · Actions tab | ☐ |

## 5. Environment Inventory & Security Transition

| ตัวแปร | จำเป็น | ค่าแนะนำ | เป็นความลับหรือไม่ |
|---|---|---|---|
| `INVENTORY_DB_PATH` | ไม่ | `data/inventory_db.json` | ไม่ |
| `REPORT_EXPORT_DIR` | ไม่ | `exports` | ไม่ |

**ระบบนี้ไม่มีรหัสผ่าน API key หรือ token ใด ๆ** — ไม่มีอะไรต้องส่งมอบเป็นความลับ
ถ้าอนาคตต้องเพิ่ม (เช่น FB-02 ส่งอีเมล) ให้เก็บใน **GitHub Secrets** และใส่ชื่อตัวแปรใน `.env.example` เท่านั้น
**ห้ามส่งความลับทาง LINE / Discord / แชตสาธารณะ และห้าม commit ไฟล์ `.env`** (ถูก ignore แล้ว)

ตรวจซ้ำก่อนส่งมอบ:

```bash
git log --all -p | grep -i -E "password|secret|api[_-]?key|token" | head    # ต้องไม่พบค่าจริง
bandit -r . -x ./test_app.py,./test_app_v2.py,./test_hardening.py,./test_deployment.py,./test_disaster_recovery.py
```

## 6. ผลการสอบทานสด

| รายการ | เกณฑ์ | ผล |
|---|---|---|
| Clean install จากแท็ก | ≤ 2 นาที ไม่มี error | ______ วินาที ☐ ผ่าน |
| PyTest full suite | 100% · coverage ≥ 90% | ______ / 195 · ____ % ☐ ผ่าน |
| Barcode · Reorder alert · CSV ใน Excel | ทำงานถูกต้อง | ☐ ผ่าน |
| Edge cases ที่กรรมการสั่ง | ไม่ crash · ข้อความปลอดภัย | ☐ ผ่าน |
| Maintenance Dossier 7 หมวด | ครบถ้วน | ☐ ผ่าน |

---

## 7. การรับรอง

ข้าพเจ้ารับรองว่าได้รับมอบซอฟต์แวร์ คลังโค้ด ชุดทดสอบ และเอกสารบำรุงรักษาตามรายการข้างต้น
และผลการทดสอบสดเป็นไปตามเกณฑ์

| บทบาท | ชื่อ | ลายมือชื่อ | วันที่ |
|---|---|---|---|
| Tech Lead (ผู้ส่งมอบ) | พนาวุฒน์ อภิปสันติ | | |
| QA (ผู้ส่งมอบ) | ตรัยรัตน์ วงษ์สิทธิ์ | | |
| คณะกรรมการตรวจรับ | | | |
| Project Sponsor (ผู้รับมอบ) | | | |

> ส่งต่อใบรับรองนี้ให้ทีม ENGSE202 ใช้เป็นหลักฐานใน [Final Project Closure Report](Final_Project_Closure_Report.md)
