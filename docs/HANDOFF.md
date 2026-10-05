# บันทึกส่งต่องาน (Handoff) — อัปเดต 2026-10-05

สถานะล่าสุดของโครงการ Mini Inventory System Evolution (ENGSE225 × ENGSE202) สำหรับทำต่อบนเครื่องอื่น (เช่น macOS)

## 1. เริ่มบนเครื่องใหม่ (macOS)

```bash
git clone https://github.com/PeawZaZa/software_mnm.git
cd software_mnm
git checkout develop
./setup.sh                 # สร้าง .venv + ติดตั้ง requirements-dev + .env + smoke test
source .venv/bin/activate
python -m pytest -q        # ต้องได้ 195 passed
python app_v2.py           # รันโปรแกรม
```

- Docker (ถ้ามี Docker Desktop for Mac): `bash tools/docker_smoke_test.sh` → ต้องได้ `RESULT: ALL PASS` (image `python:3.12-slim` รองรับ Apple Silicon)
- UAT จำลอง: `python tools/run_uat.py` · ตัวเลข/กราฟ PM: `python tools/pm_metrics.py`
- ไม่มี GitHub CLI บนเครื่องเดิม — งาน GitHub ทำผ่าน `git` + หน้าเว็บ ถ้าบน Mac มี `gh` ใช้ได้เลย

## 2. สถานะ ณ ตอนส่งต่อ

| เรื่อง | สถานะ |
|---|---|
| โค้ด | `main` = `develop` · 195 tests ผ่าน · coverage 99% · flake8 0 · bandit 0 (Medium+) · pip-audit 0 CVE · v(G) สูงสุด 7 |
| แท็ก / Release | `v2.0.0-evolution`, `v2.0.1-evolution` · หน้า Release v2.0.1 แนบ wheel + sdist + SHA256SUMS แล้ว |
| Docker | ทดสอบจริงบน Docker Desktop 29.8.1 (Windows) ผ่าน 5/5 — [log](week15/evidence/docker_smoke_test.log) |
| Jira `SAM1` | nicky2011abcd.atlassian.net · Sprint 1–3 ปิด · Release `2.0.0-evolution` released 45/45 · `3.0` = Future Backlog 4 ใบ · Log Work จำลอง 169 ชม. |
| เอกสาร | week11–15 ครบใน `docs/` · Dossier `docs/Final_System_Maintenance_Dossier.md` · คู่มือ `docs/System_Operations_and_Maintenance_Manual.md` · export Jira ใน `project_archives/` |
| สไลด์ | https://claude.ai/artifact/NTXw24yjoxAdmHHu3LPz7L (15 หน้า · ดาวน์โหลด PPTX/PDF ได้จากหน้าสไลด์) · เนื้อหาตาม [Storyboard](week14/Final_Defense_Storyboard.md) |
| หลักฐานภาพ | `docs/week15/evidence/` — Jira (Summary/Velocity/Burnup/Burndown/CFD), GitHub Releases, CSV ใน LibreOffice |

ตัวเลข PM หลัก (แหล่งเดียว: `docs/data/project_metrics.json`): PV = EV = 50,550 · AC = 50,700 · CPI 0.997 · SPI ณ วันตามแผน 0.25/1.00/0.00 · Reserve 12 ชม. คืน 900 บาท · ROI payback 26.8 เดือน (1 ปี −55.3% · 3 ปี +34.2%)

## 3. งานที่ยังค้าง (ต้องใช้คน)

1. ลงนาม: ใบ UAT Sign-off · Technical Handover Certificate · Final Project Acceptance Certificate · Team Release & Peer Review
2. **Branch Protection** — เจ้าของ repo `PeawZaZa` เท่านั้นที่ทำได้ (บัญชีอื่นไม่มีสิทธิ์ admin) ขั้นตอนอยู่ใน [week15/README.md](week15/README.md) ข้อ 7 — ห้ามติ๊ก Required status checks จนกว่าจะเคลียร์ billing
3. GitHub Actions ติด billing → CI ไม่รัน ต้องให้เจ้าของบัญชีเคลียร์
4. ซ้อมสาธิตตาม [Live Demo Script](week15/Live_Demo_and_Defense_Script.md)
5. หลังนำเสนอ: Repository Ownership Transfer → Archive Jira

## 4. ข้อควรรู้ / กติกาความซื่อตรง

- **UAT เป็นแบบจำลองโดยทีม** ไม่ใช่ cross-team — ระบุไว้ทุกที่ ห้ามเขียนว่าเป็นของจริง
- **Worklog ใน Jira เป็นชั่วโมงประมาณการ** ทุกใบมีหมายเหตุ "⚠️ ชั่วโมงประมาณการ (จำลอง)"
- ห้ามปลอมลายเซ็นหรือกรอกชื่อผู้อนุมัติแทนคนจริง
- กราฟ Burnup/Burndown/Velocity ใน Jira แบนหรือว่าง (สถานะอัปเดตย้อนหลังวันเดียว · Estimation = Time ไม่มี estimate) → ใช้กราฟใน `docs/images/` ที่สร้างจาก commit/PR history เป็นหลัก
- SAM1-39 ค้างใน Sprint 3 ทำให้ Jira นับ Sprint 3 = 11 ใบ (ค่าถูกต้อง 10) — แก้ใน sprint ที่ปิดแล้วไม่ได้ บันทึกไว้ใน `project_archives/jira_sprints_and_release.md`
- merge เข้า `main` ทำตรงโดยไม่ผ่าน PR (ไม่มี gh CLI) — บันทึกใน Release Runbook
- ชื่อ branch ห้ามขึ้นต้น `test/` เพราะ remote มี branch ชื่อ `test` อยู่แล้ว (ชนกัน)

## 5. วิธีทำงาน (GitFlow)

แตก branch จาก `develop` (`docs/…`, `fix/…`, `chore/…`) → commit → `git merge --no-ff` เข้า `develop` → `git merge --ff-only develop` บน `main` → push ทั้งสอง
ถ้าเปิด Branch Protection แล้ว ต้องเปลี่ยนเป็นเปิด PR และให้สมาชิกอีกคนอนุมัติ
