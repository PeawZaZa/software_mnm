# Maintenance Summary Report (ISO/IEC 14764)
## ENGSE225 สัปดาห์ที่ 12 · ชิ้นงานที่ 3 — สรุปกิจกรรมบำรุงรักษาสัปดาห์ที่ 8–12

| | |
|---|---|
| ระบบ | Mini Inventory System · `v1.0.0-baseline` → `v2.0.0-evolution` |
| มาตรฐาน | ISO/IEC 14764:2006 Software Engineering — Software Maintenance |
| ผู้จัดทำ | ปวริศ คูณศรี (PM) · พนาวุฒน์ อภิปสันติ (Tech Lead) |
| วันที่ | 2026-10-05 |
| คู่กับ | [CHANGELOG.md](../../CHANGELOG.md) — ไฟล์นั้นบอก *อะไรเปลี่ยน* เอกสารนี้บอก *เปลี่ยนเพราะอะไร และเป็นการบำรุงรักษาประเภทใด* |

---

## 1. ประเภทการบำรุงรักษาตาม ISO/IEC 14764

| ประเภท | นิยาม | ตัวอย่างในโครงการนี้ |
|---|---|---|
| **Corrective** | แก้ข้อบกพร่องที่**ผู้ใช้เจอแล้ว** | ตัดสต๊อกติดลบได้ · ข้อมูลเสียแถวเดียวเปิดโปรแกรมไม่ได้ |
| **Preventive** | แก้ข้อบกพร่องแฝง**ก่อนที่จะเกิดผล** | ลบ global `x` · atomic write · ชุดทดสอบอัตโนมัติ |
| **Perfective** | เพิ่มความสามารถ/คุณภาพตามความต้องการใหม่ | Barcode (CR-01) · CSV (CR-02) · แยกสถาปัตยกรรม |
| **Adaptive** | ปรับให้ทำงานในสภาพแวดล้อมที่เปลี่ยน | CSV แบบ `utf-8-sig` + `newline=""` ให้ Excel บน Windows อ่านได้ |

## 2. ทะเบียนกิจกรรมบำรุงรักษา

### 2.1 Sprint 1 — สัปดาห์ที่ 8 (v1.1)

| รหัส | เรื่อง | ประเภท | หลักฐาน |
|---|---|---|---|
| INV-4 | ลบ `global x` ส่ง `inventory` เป็นพารามิเตอร์ | Preventive | PR #3 |
| INV-5 | ตัวแปร `c` (qty) ชนกับคีย์ `"c"` (category) | Corrective | PR #6 · `78d638a` |
| INV-6 | พิมพ์ตัวอักษรในช่องตัวเลขแล้วโปรแกรมตาย | Corrective | PR #2 |
| INV-7 | ตัดสต๊อกด้วยค่าติดลบ/ศูนย์ได้ (สต๊อกเพิ่มขึ้น) | Corrective | PR #5 · `1abc4bb` |
| INV-8 | if/else ทำงานเหมือนกันทั้งสองทาง | Preventive | PR #4 · `9c80079` |
| INV-9 | เกณฑ์สต๊อกต่ำเมนู 3 (5) กับเมนู 4 (10) ไม่ตรงกัน | Corrective | PR #4 · `1a04a48` |
| INV-10 | ไฟล์ข้อมูลเสียแล้วโปรแกรมตาย | Corrective | PR #6 · `9b0ecc6` |
| INV-11 | บันทึกไฟล์แบบ atomic ผ่าน `.tmp` | Preventive | PR #6 · `3354f7d` |
| INV-12 | เปลี่ยนชื่อเมนู "Check Check" | Perfective | PR #6 · `083cbac` |
| INV-14 | Unit tests 37 เคส ล็อกพฤติกรรมก่อน refactor | Preventive | PR #1 |

### 2.2 Sprint 2 — สัปดาห์ที่ 9–10 (v2.0 → v2.1)

| รหัส | เรื่อง | ประเภท | หลักฐาน |
|---|---|---|---|
| SAM1-28…43 | แยกเป็น 4 คลาสตาม Repository Pattern | Perfective (maintainability) | PR #23 · `dff022f` `3571b87` `1250324` `529eaf0` |
| CR-01 | Barcode + Reorder Point | Perfective | PR #24 · `74367ea` |
| CR-02 | Export CSV สำหรับ Excel | Perfective + Adaptive | PR #25 · `4169f2c` |
| DEF-01 (#20) | บาร์โค้ดซ้ำกันได้ | Corrective | PR #26 · `8cb3e25` |
| DEF-02 (#21) | Reorder point ติดลบถูกบันทึกแล้วถูกละเลย | Corrective | PR #26 · `8cb3e25` |
| DEF-03 (#22) | ข้อมูลเสียแถวเดียว → เปิดโปรแกรมไม่ได้ (High) | Corrective | PR #26 · `8cb3e25` |

### 2.3 Sprint 3 — สัปดาห์ที่ 11–12 (Hardening & Release)

| รหัส | เรื่อง | ประเภท | หลักฐาน |
|---|---|---|---|
| S3-01 | Flake8 270 → 0 | Preventive | `eabd642` |
| S3-03 | Code smells: Duplicate Code · Feature Envy · Long Conditional · Dead comments | Preventive | `44f6042` |
| S3-04 | Atomic write ด้วย `tempfile` + `fsync` | Preventive | `44f6042` |
| S3-04 | `save()` กลืน error แล้วตอบ `Done.` (ข้อมูลหายเงียบ) | Preventive — พบก่อนผู้ใช้เจอ | `44f6042` |
| S3-04 | `data.json` เป็น JSON array → crash | Preventive — พบก่อนผู้ใช้เจอ | `44f6042` |
| S3-05 | CI gates: flake8 · bandit · coverage ≥ 90% | Preventive | `dc03c3b` |
| UAT-DEF-01 | ไม่เตือนตอนขายเมื่อถึง reorder point > 10 | Corrective (พบใน UAT) | `3746f1b` |

## 3. สรุปตามประเภท

| ประเภท | จำนวนรายการ | สัดส่วน |
|---|---:|---:|
| Corrective | 9 | 39% |
| Preventive | 10 | 43% |
| Perfective | 4 | 17% |
| Adaptive | (1 — นับร่วมกับ CR-02) | — |
| **รวม** | **23** | 100% |

**ข้อสังเกต** — งาน Preventive มากกว่า Corrective หมายความว่าทีมใช้เวลากับการ*ป้องกัน*มากกว่า*ดับไฟ*
ซึ่งเป็นสัดส่วนที่ดีสำหรับระบบ legacy ข้อบกพร่อง 2 จุดใน Sprint 3 ถูกพบโดย hardening ก่อนผู้ใช้เจอ
จึงนับเป็น Preventive ตามนิยามของมาตรฐาน

## 4. การวิเคราะห์สาเหตุราก (RCA) ของข้อบกพร่องที่รุนแรงที่สุด — DEF-03

ใช้วิธี **5 Whys**

| # | ทำไม | คำตอบ |
|---|---|---|
| 1 | ทำไมเปิดโปรแกรมไม่ได้ | `Product.from_dict()` โยน `ValueError` ตอนแปลง `"q": "abc"` เป็น `int` |
| 2 | ทำไม error หลุดออกมาจนโปรแกรมตาย | `try/except` ใน `load()` ครอบแค่ `json.loads()` ไม่ได้ครอบการแปลงรายแถว |
| 3 | ทำไมครอบไม่ครบ | ตอน INV-10 (Sprint 1) ข้อมูลยังเป็น dict ดิบ ไม่มีการแปลงชนิด จึงพังได้แค่ตอน parse |
| 4 | ทำไมไม่มีใครเห็นตอนเพิ่ม `Product` ใน Sprint 2 | เทสต์ของ `load()` ทดสอบแค่ไฟล์เสียทั้งไฟล์ ไม่มีเคสไฟล์ดีแต่ค่าบางแถวผิด |
| 5 | ทำไมไม่มีเคสนั้น | ไม่มีขั้นตอนทบทวนว่า exception handling เดิมยังครอบคลุมหลังเปลี่ยนโครงสร้างข้อมูล |

**แก้ที่ราก** — ครอบการแปลงรายแถว (DEF-03) และในสัปดาห์ที่ 11 เปลี่ยนเป็นจับ exception ที่เจาะจง + ตรวจรูปร่าง JSON
**ป้องกันซ้ำ** — DoD เพิ่มข้อ "ทุกการเปลี่ยน data model ต้องมีเทสต์ไฟล์ที่ถูกไวยากรณ์แต่ค่าผิด"

## 5. ผลลัพธ์เชิงปริมาณ

| ตัวชี้วัด | v1.0.0-baseline | v2.0.0-evolution |
|---|---:|---:|
| Max Cyclomatic Complexity | 14 | 7 |
| ฟังก์ชัน/เมธอดที่ v(G) > 10 | 1 | 0 |
| Global mutable state | 1 | 0 |
| Automated tests | 0 | 173 |
| Coverage | — | 99% |
| Flake8 / Bandit | — | 0 / 0 |
| ข้อบกพร่องที่ทราบและยังเปิดอยู่ | 9 จุดเสี่ยง | 0 |
