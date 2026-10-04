# Procurement & Reserve Close-out Sheet (ฉบับปิดโครงการ)
## ENGSE202 สัปดาห์ที่ 15 · ชิ้นงานที่ 3

| | |
|---|---|
| ผู้จัดทำ | ปวริศ คูณศรี (PM) |
| วันที่ปิดบัญชี | 2026-10-05 |
| ฉบับละเอียด | [สัปดาห์ที่ 11](../week11/Procurement_Reconciliation.md) · [สัปดาห์ที่ 12](../week12/Procurement_Closeout_and_Reserve_Settlement.md) |

## 1. ต้นทุนรวมโครงการ

| รายการ | Baseline (PV) | Actual (AC) | Variance |
|---|---:|---:|---:|
| ค่าแรง Sprint 1 | 19,200 | 19,350 🔶 | −150 |
| ค่าแรง Sprint 2 (รวม CR-02 + DEF) | 20,100 | 20,100 🔶 | 0 |
| ค่าแรง Sprint 3 (รวม UAT-DEF-01) | 11,250 | 11,250 🔶 | 0 |
| ค่าเครื่องมือ (Jira · GitHub · Actions · OSS · Cloud) | 0 | 0 | 0 |
| **รวม** | **50,550** | **50,700** | **−150** |

🔶 ค่าแรงจริงประมาณจากหลักฐานใน git (ยังไม่มี Jira Log Work) · อัตรา 300 บาท/ชม.

## 2. ปิดสัญญาเครื่องมือ

| เครื่องมือ | สถานะสุดท้าย | หนี้ค้าง |
|---|---|---|
| Jira Software Cloud (Free) | Archive project หลังลงนาม Final Acceptance | ไม่มี |
| GitHub Repository (Public) | โอนสิทธิ์ให้ Sponsor ([Handover Certificate ข้อ 4](Technical_Handover_Certificate.md#4-repository-ownership-transfer-เจ้าของบัญชี-peawzaza-ทำ)) | ไม่มีจากโครงการ · ⚠️ บัญชีติด billing lock ต้องให้เจ้าของตรวจ |
| GitHub Actions | ใช้ 0 นาที | ไม่มี |
| Cloud / Database | ไม่เคยเช่า | ไม่มี |

**Zero Debt จากโครงการ** ✅

## 3. Reserve Return Settlement

| | ชม. | บาท |
|---|---:|---:|
| เงินสำรองตั้งต้น | 12.0 | 3,600 |
| เบิกจ่าย — CR-02 · DEF-01/02/03 · UAT-DEF-01 · ชดเชยงานทำซ้ำ Sprint 1 | 9.0 | 2,700 |
| **คงเหลือสุทธิคืน Sponsor** | **3.0** | **900** 🟢 |

## 4. ลงนามปิดบัญชี

| บทบาท | ชื่อ | ลายมือชื่อ | วันที่ |
|---|---|---|---|
| Project Manager | ปวริศ คูณศรี | | |
| Project Sponsor (รับคืนเงินสำรอง 900 บาท) | | | |
