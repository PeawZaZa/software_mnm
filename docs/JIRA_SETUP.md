# คู่มือตั้งค่า Jira สำหรับสิ่งส่งมอบสัปดาห์ที่ 9–10

เอกสารนี้สรุปขั้นตอนที่**ต้องกดเองใน Jira UI** เพราะ API ทำแทนไม่ได้
พร้อมบอกว่าขั้นไหนทำอัตโนมัติไปแล้ว

| Jira site | https://nicky2011abcd.atlassian.net |
|---|---|
| Project | `SAM1` — Billing System Dev (team-managed) |

---

## ทำไมต้องตั้งค่าเพิ่ม

`SAM1` เป็น **team-managed project** ที่ยัง**ไม่ได้เปิดฟีเจอร์ Sprints**
ตรวจสอบจาก field metadata ของ issue type `Task` พบ 20 fields แต่**ไม่มี Sprint field**
ตราบใดที่ยังไม่เปิด จะไม่มี sprint ให้ใส่งาน และ Reports จะไม่มี Burndown Chart ให้ดู

---

## ขั้นที่ 1 — เปิดฟีเจอร์ Sprints ✅ **ทำแล้ว**

1. เปิด project `SAM1`
2. เมนูซ้ายล่าง → **Project settings**
3. เลือก **Features**
4. เปิดสวิตช์ **Sprints** (ระบบจะเปิด **Backlog** ให้อัตโนมัติด้วย)

> ✅ ยืนยันแล้วว่า Sprint field (`customfield_10020`) โผล่ในระบบ และ Jira สร้าง `SAM1 Sprint 1` (id 1) ให้แล้ว

---

## ขั้นที่ 2 — สร้าง Sprint ที่ 2 ⬜ **ยังเหลือ**

ตอนนี้มีแค่ `SAM1 Sprint 1` — ต้องสร้างอันที่สองเอง

1. เมนูซ้าย → **Backlog**
2. กด **+ Add sprint**
3. เปลี่ยนชื่อให้อ่านง่าย (กดที่ชื่อ sprint แล้วพิมพ์ทับ)
   - `Sprint 1 — Refactor & Bug Fixes`
   - `Sprint 2 — Class-Based Architecture + CR`

> ตรวจแล้วว่า sprint id 2 **ยังไม่มี** (API ตอบ "We could not find the sprint")
> พอสร้างเสร็จแจ้งได้ เดี๋ยวใส่งานที่เหลือ 19 ใบให้ครบ

---

## ขั้นที่ 3 — ใส่งานเข้า Sprint

| Sprint | Issues | จำนวน | สถานะ |
|---|---|---|---|
| Sprint 1 (id 1) | SAM1-11 … SAM1-26 | 16 ใบ | ✅ **ใส่ครบแล้ว** |
| Sprint 2 (ยังไม่มี) | SAM1-28 … SAM1-48 | 19 ใบ | ⬜ รอสร้าง sprint ก่อน |

งาน 19 ใบที่รออยู่ ได้แก่ SAM1-28…43 (Sprint 2 เดิม) และที่สร้างใหม่รอบนี้:

| Issue | เรื่อง |
|---|---|
| SAM1-44 | CR-01 Barcode + Reorder Point |
| SAM1-45 | CR-02 Export CSV |
| SAM1-46 | DEF-03 ข้อมูลเสียแถวเดียวทำให้เปิดโปรแกรมไม่ได้ (High) |
| SAM1-47 | DEF-01 Barcode ซ้ำ |
| SAM1-48 | DEF-02 Reorder point ติดลบ |

---

## ขั้นที่ 4 — Start Sprint ⬜

**สำคัญ:** ต้องใส่วันที่**ย้อนหลังให้ตรงกับที่ทำงานจริง** ไม่งั้น Burndown Chart จะไม่สื่อความหมาย

| Sprint | Start date | End date | ที่มาของวันที่ |
|---|---|---|---|
| Sprint 1 | 2026-06-29 | 2026-07-13 | วันที่สร้าง issue ทั้งหมดใน Jira / รอบ sprint 2 สัปดาห์ |
| Sprint 2 | 2026-08-10 | 2026-09-07 | วันที่สร้าง issue ชุด SAM1-28…43 / วันส่งงาน |

วิธีทำ: ที่ Backlog กด **Start sprint** ที่ sprint นั้น → กรอกวันที่ → **Start**

---

## ขั้นที่ 5 — แคปหน้าจอสำหรับส่งงาน ⬜

### สัปดาห์ที่ 9 ชิ้นงานที่ 4 — Active Sprint

1. เมนูซ้าย → **Board**
2. ให้เห็นชื่อ sprint และการ์ดงานเรียงในคอลัมน์ To Do / In Progress / In Review / Done
3. แคปทั้งหน้าจอให้เห็นชื่อ sprint ชัดเจน

### สัปดาห์ที่ 10 ชิ้นงานที่ 4 — Burndown Chart

1. เมนูซ้าย → **Reports**
2. เลือก **Burndown Chart**
3. เลือก Sprint 2 ที่ dropdown ด้านบน
4. แคปหน้าจอให้เห็นทั้งเส้นแนวทางในอุดมคติ (สีเทา) และเส้นงานจริง (สีแดง)

> เส้นงานจริงจะดิ่งลงตรงช่วงท้าย ซึ่งตรงกับที่วิเคราะห์ไว้ใน
> [`Sprint1_Retrospective.md`](Sprint1_Retrospective.md) ข้อ M1 — ใช้ประกอบคำอธิบายได้เลย

---

## Checklist สรุป

- [x] เปิดฟีเจอร์ Sprints ใน Project settings → Features
- [x] ใส่งาน 16 ใบเข้า Sprint 1
- [ ] กด **+ Add sprint** สร้าง Sprint 2 ใน Backlog
- [ ] แจ้งให้ใส่งานอีก 19 ใบเข้า Sprint 2
- [ ] Start sprint ทั้งสองอันด้วยวันที่ย้อนหลัง
- [ ] แคป Active Sprint (สัปดาห์ที่ 9)
- [ ] แคป Burndown Chart (สัปดาห์ที่ 10)

---

## หมายเหตุอื่น

**project นี้ไม่มี issue type `Bug`** มีแค่ Epic / Task / Story / Subtask
ข้อบกพร่องจาก Bug Bashing จึงสร้างเป็น `Task` แล้วติด label `bug` แทน

**ยังไม่ได้เปิด Story Points** ถ้าต้องการให้ Burndown Chart คิดตาม story point
แทนจำนวน issue ต้องเปิด **Estimation** ใน Project settings → Features ด้วย
