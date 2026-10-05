# Definition of Done — แม่แบบ (ฉบับมีกลไกบังคับ)

> บทเรียนจากโครงการ Inventory System: DoD ฉบับแรกเขียนไว้ครบทุกข้อ แต่ไม่มีข้อไหนถูกบังคับด้วยเครื่องมือ
> ผลคือ PR ที่เทสต์แดงถูก merge, `main` เสีย 2 เดือน และ PR ถูก merge โดยไม่มีคนรีวิว
> **กติกา: ข้อไหนบังคับด้วยเครื่องมือไม่ได้ ต้องระบุชื่อคนตรวจ**

## งานโค้ด (Task / Bug / CR)

| # | เกณฑ์ | กลไกบังคับ | ตั้งค่าที่ |
|---|---|---|---|
| 1 | เทสต์ทั้งหมดผ่าน (ไม่ใช่แค่เทสต์ใหม่) | Required status check `PyTest CI` | GitHub → Settings → Branches |
| 2 | Coverage ไม่ต่ำกว่า __ % | `pytest --cov-fail-under=__` ใน CI | workflow |
| 3 | Lint 0 · Security scan ไม่มี Medium+ | `flake8` · `bandit -ll` ใน CI | workflow |
| 4 | มีผู้อนุมัติ 1 คนที่**ไม่ใช่ผู้เปิด PR** | Require approvals: 1 · Do not allow bypassing | Branch protection |
| 5 | ทุก input ใหม่มีเทสต์ค่าติดลบและค่าผิดชนิด | ผู้รีวิวตรวจ — ชื่อ: ________ | PR template |
| 6 | ทุกการเปลี่ยน data model มีเทสต์อ่านไฟล์เก่า + ไฟล์ค่าผิด | ผู้รีวิวตรวจ — ชื่อ: ________ | PR template |
| 7 | Commit อ้างเลขงาน `[KEY-123]` | commit-msg hook / ผู้รีวิว | `.githooks/` |
| 8 | Log Work ใน Jira แล้ว | PM ตรวจก่อนย้ายการ์ดเป็น Done — ชื่อ: ________ | Jira workflow |

## Sprint

| # | เกณฑ์ | กลไกบังคับ |
|---|---|---|
| 1 | Burndown ลด ≥ 40% ภายในวันที่ 7 | PM ตรวจใน Standup วันที่ 7 — ไม่ถึงให้ตัดขอบเขต |
| 2 | WIP ช่อง In Review ≤ 3 | Jira column limit |
| 3 | ไม่มีการ์ดค้าง In Progress ข้าม sprint | Jira Sprint Report ตอน Complete Sprint |

## Release

| # | เกณฑ์ | กลไกบังคับ |
|---|---|---|
| 1 | UAT sign-off ลงนามแล้ว | มีฉบับสแกน (เก็บนอก repo) ก่อนเปิด PR เข้า `main` |
| 2 | ติดตั้งจาก `git clone` ลงโฟลเดอร์ว่างผ่าน | `setup.sh` + smoke test — แนบ log ใน PR |
| 3 | มีแท็ก annotated + CHANGELOG | ผู้รีวิว PR release |
| 4 | แท็กก่อนหน้ายังรันเทสต์ผ่าน (จุด rollback) | รันใน `git worktree` แนบผลใน PR |
