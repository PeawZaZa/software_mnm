"""
run_uat.py — รัน UAT Scenarios กับโปรแกรมจริงผ่านหน้าจอ CLI (ไม่ได้เรียกคลาสตรง ๆ)

จำลองผู้ใช้พิมพ์เมนูทีละขั้นด้วยการป้อน stdin ให้ `python app_v2.py`
ในโฟลเดอร์ชั่วคราว (ไม่แตะ data.json จริง) แล้วตรวจข้อความบนหน้าจอและไฟล์ผลลัพธ์

รัน:  python tools/run_uat.py [label]
ผล:   พิมพ์ transcript + ตาราง PASS/FAIL และคืน exit code 1 ถ้ามีเคสไม่ผ่าน
"""

import csv
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app_v2.py"


def run_cli(workdir, keystrokes):
    """ป้อนปุ่มที่ผู้ใช้กดให้โปรแกรม แล้วคืนข้อความทั้งหมดที่แสดงบนหน้าจอ"""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run(  # nosec B603 — รันไฟล์โปรแกรมของโปรเจกต์เอง ไม่รับ input ภายนอก
        [sys.executable, str(APP)], input="\n".join(keystrokes) + "\n",
        capture_output=True, text=True, encoding="utf-8", cwd=workdir, env=env, timeout=30,
    )
    return result.stdout + result.stderr


def add(pid, name, qty, price, cat, barcode, reorder):
    return ["2", pid, name, str(qty), str(price), cat, barcode, str(reorder)]


def scenarios(workdir):
    csv_path = Path(workdir) / "uat_report.csv"
    return [
        {
            "id": "UAT-SC01", "role": "Inventory Manager",
            "action": "รับสินค้าเข้า: Milk (P100) บาร์โค้ด 885123456789 สต๊อก 10 Reorder Point 5",
            "expected": "บันทึกสำเร็จ ไม่ crash และเห็นสินค้าในเมนู 1",
            "keys": add("P100", "Milk", 10, 20, "Dairy", "885123456789", 5) + ["1", "5"],
            "check": lambda out: "Done." in out and "Name: Milk | Stock: 10" in out,
        },
        {
            "id": "UAT-SC02", "role": "Store Cashier",
            "action": "ขาย Milk ออก 6 ชิ้น (เหลือ 4 ≤ Reorder Point 5)",
            "expected": "ขึ้นข้อความเตือนทันทีหลังตัดสต๊อก",
            "keys": ["3", "P100", "6", "5"],
            "check": lambda out: "!!!" in stock_out_reply(out),
        },
        {
            "id": "UAT-SC02-B", "role": "Store Cashier",
            "action": ("สินค้าขายเร็ว: Water (P200) สต๊อก 40 Reorder Point 30 "
                       "→ ขายออก 12 (เหลือ 28 ≤ 30)"),
            "expected": "ขึ้นข้อความเตือนว่าถึงจุดสั่งซื้อทันทีหลังตัดสต๊อก",
            "keys": add("P200", "Water", 40, 10, "Drink", "885000000200", 30)
            + ["3", "P200", "12", "5"],
            "check": lambda out: "REORDER" in stock_out_reply(out).upper(),
        },
        {
            "id": "UAT-SC03", "role": "Purchasing Officer",
            "action": "เมนู 7 Export CSV แล้วเปิดไฟล์ตรวจ",
            "expected": ("ไฟล์มีคอลัมน์ barcode / reorder_point และข้อมูล Milk ถูกต้อง "
                         "เปิดใน Excel ได้ (มี BOM)"),
            "keys": ["7", str(csv_path), "5"],
            "check": lambda out: check_csv(csv_path),
        },
        {
            "id": "UAT-SC04", "role": "Store Owner",
            "action": "เมนู 4 Inventory Summary — ยืนยันฟังก์ชันเดิมยังคำนวณถูก",
            "expected": "มูลค่ารวม = 1,540 (default) + Milk 4×20 + Water 28×10 = 1,900 บาท",
            "keys": ["4", "5"],
            "check": lambda out: "Total inventory value: 1900.0 THB" in out,
        },
        {
            "id": "UAT-EC01", "role": "กรรมการ (edge case)",
            "action": "ตัดสต๊อกเกินจำนวนที่มี: Milk ขอออก 999",
            "expected": "ปฏิเสธพร้อมข้อความ ไม่ crash สต๊อกไม่เปลี่ยน",
            "keys": ["3", "P100", "999", "1", "5"],
            "check": lambda out: "Not enough stock" in out and "Name: Milk | Stock: 4" in out,
        },
        {
            "id": "UAT-EC02", "role": "กรรมการ (edge case)",
            "action": "กรอกราคาเป็น 'abc' และราคาติดลบ",
            "expected": "ปฏิเสธทั้งสองกรณี ไม่ crash",
            "keys": ["2", "X1", "Bad", "1", "abc"] + add("X2", "Bad", 1, -5, "T", "", 0) + ["5"],
            "check": lambda out: "must be numbers" in out and "must not be negative" in out
            and "Traceback" not in out,
        },
        {
            "id": "UAT-EC03", "role": "กรรมการ (edge case)",
            "action": "Export CSV ซ้ำสองรอบติดกันไปที่ไฟล์เดิม",
            "expected": "ไฟล์ถูกเขียนทับสมบูรณ์ ไม่มีแถวซ้ำ ไม่เสียหาย",
            "keys": ["7", str(csv_path), "7", str(csv_path), "5"],
            "check": lambda out: out.count("Exported 5 products") == 2 and check_csv(csv_path),
        },
    ]


def stock_out_reply(out):
    """ข้อความที่ระบบตอบกลับหลังผู้ใช้ตัดสต๊อก (ไม่ปนกับข้อความเมนู)"""
    marker = "How many items out?: "
    if marker not in out:
        return ""
    return out.rsplit(marker, 1)[1].splitlines()[0]


def check_csv(path):
    if not path.exists() or path.read_bytes()[:3] != b"\xef\xbb\xbf":
        return False
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    ids = [r["id"] for r in rows]
    milk = next((r for r in rows if r["id"] == "P100"), None)
    return (len(ids) == len(set(ids)) and milk is not None
            and milk["barcode"] == "885123456789" and milk["qty"] == "4"
            and milk["reorder_point"] == "5")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    label = sys.argv[1] if len(sys.argv) > 1 else "run"
    results = []
    with tempfile.TemporaryDirectory() as workdir:
        for sc in scenarios(workdir):
            out = run_cli(workdir, sc["keys"])
            ok = bool(sc["check"](out))
            results.append((sc, ok))
            print(f"\n{'=' * 70}\n{sc['id']} · {sc['role']} · {'PASS' if ok else 'FAIL'}")
            print(f"Action  : {sc['action']}\nExpected: {sc['expected']}\n--- screen ---")
            print("\n".join(line for line in out.splitlines()
                            if line.strip() and not line.startswith(("1.", "2.", "3.", "4.",
                                                                     "5.", "6.", "7.", "==="))))
    passed = sum(ok for _, ok in results)
    print(f"\n{'=' * 70}\nUAT {label}: {passed}/{len(results)} passed")
    for sc, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {sc['id']}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
