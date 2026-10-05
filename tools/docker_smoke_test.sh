#!/usr/bin/env bash
# docker_smoke_test.sh — build image แล้วทดสอบว่า container ใช้งานได้จริงและข้อมูลอยู่รอดใน volume
# รัน:  bash tools/docker_smoke_test.sh  (ต้องมี Docker Engine ทำงานอยู่)
set -u
IMAGE=mini-inventory:v2.0.1
VOLUME=mini-inventory-smoke-data
EXPORTS="$(pwd)/exports_smoke"
FAIL=0

check() {  # check <label> <pattern> <text>
    if grep -q -- "$2" <<<"$3"; then echo "PASS  $1"; else echo "FAIL  $1"; FAIL=1; fi
}

echo "== docker version"; docker version --format 'client {{.Client.Version}} / server {{.Server.Version}}'
echo "== build"; docker build -t "$IMAGE" . || exit 1
docker image ls "$IMAGE"

docker volume rm -f "$VOLUME" >/dev/null 2>&1
rm -rf "$EXPORTS"; mkdir -p "$EXPORTS"

echo "== run 1: เพิ่มสินค้า + ตัดสต๊อกถึง reorder point + export CSV"
OUT1=$(printf '2\nP100\nMilk\n10\n25\nDairy\n885123456789\n5\n3\nP100\n5\n7\nstock_report.csv\n5\n' |
    MSYS_NO_PATHCONV=1 docker run -i --rm -v "$VOLUME:/app/data" -v "$EXPORTS:/app/exports" "$IMAGE")
echo "$OUT1"
check "เพิ่มสินค้าสำเร็จ" "Done." "$OUT1"
check "เตือน reorder point (UAT-DEF-01)" "REORDER POINT REACHED" "$OUT1"
check "ไฟล์ CSV ถูกสร้างใน volume exports" "stock_report.csv" "$(ls "$EXPORTS")"

echo "== run 2: container ใหม่ อ่านข้อมูลเดิมจาก volume"
OUT2=$(printf '1\n5\n' |
    MSYS_NO_PATHCONV=1 docker run -i --rm -v "$VOLUME:/app/data" "$IMAGE")
echo "$OUT2"
check "ข้อมูลอยู่รอดหลังลบ container" "Name: Milk | Stock: 5" "$OUT2"

echo "== user ใน container"
USER_NAME=$(MSYS_NO_PATHCONV=1 docker run --rm "$IMAGE" whoami)
check "ไม่รันด้วย root" "appuser" "$USER_NAME"

docker volume rm -f "$VOLUME" >/dev/null
rm -rf "$EXPORTS"
[ "$FAIL" -eq 0 ] && echo "RESULT: ALL PASS" || echo "RESULT: FAILED"
exit "$FAIL"
