# CLAUDE.md

- ตอบผู้ใช้เป็นภาษาไทยเสมอ
- อ่าน [docs/HANDOFF.md](docs/HANDOFF.md) ก่อนเริ่มงาน — สถานะล่าสุด งานค้าง และกติกาความซื่อตรง (UAT/worklog เป็นแบบจำลอง ห้ามปลอมลายเซ็น)
- เทสต์: `python -m pytest -q` (195 passed) · lint: `flake8` · ความปลอดภัย: `bandit` ตามคำสั่งใน `.github/workflows/pytest.yml`
- ตัวเลข PM ทุกตัวมาจาก `docs/data/project_metrics.json` ผ่าน `tools/pm_metrics.py` — แก้ที่แหล่งเดียว
- ทำงานแบบ GitFlow: branch จาก `develop` → merge `--no-ff` เข้า `develop` → fast-forward `main`
