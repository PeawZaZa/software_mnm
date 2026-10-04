# Release Runbook — `v2.0.0-evolution`
## ENGSE225 สัปดาห์ที่ 12 · ชิ้นงานที่ 2 และ 4 — การส่งมอบสู่ Production ตาม ISO/IEC/IEEE 12207

| | |
|---|---|
| Release candidate | สาขา `release/v2.0.0-evolution` (แตกจาก `develop` @ `8ce53e3`) |
| เป้าหมาย | `main` → Gold Master + Annotated Tag `v2.0.0-evolution` |
| ผู้รับผิดชอบ | พนาวุฒน์ อภิปสันติ (Tech Lead) |
| Release notes | [Release_Notes_v2.0.0-evolution.md](Release_Notes_v2.0.0-evolution.md) |

---

## 1. สถานะเงื่อนไขก่อนรวมเข้า `main` (Transition Gate)

| # | เงื่อนไข | สถานะ | หลักฐาน |
|---|---|---|---|
| 1 | UAT Sign-off ลงนามครบ | ⬜ **รอลงนาม** | [UAT Sheet ข้อ 6](UAT_Test_Scenarios_and_Signoff.md#6-ใบรับรองการตรวจรับงาน-uat-sign-off-certificate) — รอบซ้อมภายในผ่าน 8/8 |
| 2 | Full Regression PyTest 100% | ✅ ผ่าน (บนเครื่อง) | [`evidence/regression_release_candidate.txt`](evidence/regression_release_candidate.txt) — 173 passed · 99% |
| 3 | Tech Lead อนุมัติบน Pull Request | ⬜ รอเปิด PR | ขั้นที่ 3 ด้านล่าง |
| — | CI บน GitHub Actions เขียว | ⚠️ ไม่สามารถรันได้ | บัญชีติด billing — ใช้ผลรันบนเครื่องแทน และบันทึกไว้ใน PR |

> **ทำไมยังไม่ merge เข้า `main` ให้เสร็จในเครื่องเลย** — ถ้า merge แล้ว push ตรง จะเป็นการข้ามขั้น Pull Request
> และ Tech Lead review ซึ่งเป็นปัญหาเดียวกับที่พบใน Sprint 2 (PR merge โดยผู้เปิดเองภายใน 1 นาที)
> การ release จึงต้องผ่าน PR บน GitHub ตามขั้นที่ 3

---

## 2. Push สาขา release ขึ้น GitHub

```bash
git push origin develop
git push origin release/v2.0.0-evolution
```

## 3. เปิด Final Pull Request → `main`

GitHub → **Pull requests** → **New pull request**

| ช่อง | ค่า |
|---|---|
| base | `main` |
| compare | `release/v2.0.0-evolution` |
| Title | `Release v2.0.0-evolution: Refactored Architecture + CR-01 + CR-02` |
| Description | คัดลอกจาก [Release_Notes_v2.0.0-evolution.md](Release_Notes_v2.0.0-evolution.md) แล้วแนบผลรัน `pytest` จาก [`evidence/regression_release_candidate.txt`](evidence/regression_release_candidate.txt) |
| Reviewer | พนาวุฒน์ อภิปสันติ (Tech Lead) — **ผู้เปิด PR ต้องไม่ใช่คนกด merge** |

Tech Lead ตรวจ แล้วกด **Approve** → **Create a merge commit** (ไม่ใช้ squash เพื่อเก็บประวัติ Sprint ไว้ครบ)

## 4. สร้าง Annotated Tag บน `main`

```bash
git checkout main
git pull origin main
git tag -a v2.0.0-evolution -m "Production Release v2.0.0: Refactored Repository Pattern, Barcode Support, Reorder Point Alerts, and CSV Reporting."
git push origin v2.0.0-evolution
git show v2.0.0-evolution --stat | head -5     # ต้องเห็น Tagger + วันที่ + ข้อความ
```

`-a` สร้าง **Annotated Tag** ที่เก็บชื่อผู้สร้าง วันเวลา และข้อความไว้ถาวร
ต่างจาก lightweight tag ที่เป็นแค่ชื่อชี้ไปที่ commit

## 5. สร้าง GitHub Release

GitHub → **Releases** → **Draft a new release**

| ช่อง | ค่า |
|---|---|
| Tag | `v2.0.0-evolution` |
| Title | `Mini Inventory System v2.0.0` |
| Body | คัดลอกจาก [Release_Notes_v2.0.0-evolution.md](Release_Notes_v2.0.0-evolution.md) |
| ☑ | **Set as the latest release** |

ตรวจหน้า Releases ว่ามีป้ายสีเขียว **Latest** และ GitHub สร้าง Source code `.zip` / `.tar.gz` ให้อัตโนมัติ
แคปหน้าจอเก็บไว้ที่ `docs/week12/evidence/github_release.png`

## 6. Sync `main` กลับเข้า `develop` (GitFlow)

```bash
git checkout develop
git merge --no-ff main -m "Merge main back into develop after v2.0.0-evolution"
git push origin develop
```

---

## 7. แผนถอยกลับ (Rollback) ถ้า Release มีปัญหา

```bash
git checkout main
git revert -m 1 <merge-commit-ของ-PR>     # สร้าง commit ย้อนกลับ ไม่ลบประวัติ
git push origin main
```

**ห้ามใช้ `git reset --hard` + `push --force` บน `main`** — ลบประวัติที่คนอื่น pull ไปแล้ว
รายละเอียดการซ้อมอยู่ในงานสัปดาห์ที่ 14

---

## 8. Checklist

- [x] CHANGELOG.md มีหัวข้อ `[2.0.0-evolution]` ครบ Added / Changed / Removed / Fixed
- [x] README อัปเดตเวอร์ชันและจำนวนเทสต์
- [x] Regression 173/173 ผ่านบน release candidate
- [x] UAT รอบซ้อมภายใน 8/8
- [ ] UAT Sign-off ลงนาม
- [ ] Push `develop` และ `release/v2.0.0-evolution`
- [ ] PR → `main` ได้ Approve จาก Tech Lead และ merge
- [ ] Tag `v2.0.0-evolution` ถูก push
- [ ] GitHub Release ขึ้นป้าย Latest
- [ ] Merge `main` กลับเข้า `develop`
