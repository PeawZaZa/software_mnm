#!/usr/bin/env bash
# setup.sh — ติดตั้ง Inventory System บนเครื่องใหม่ด้วยคำสั่งเดียว (macOS / Linux / Git Bash บน Windows)
#
#   ./setup.sh            ติดตั้ง runtime + dev tools แล้วรัน smoke test
#   ./setup.sh --runtime  ติดตั้งเฉพาะที่จำเป็นต่อการรันโปรแกรม
set -euo pipefail
cd "$(dirname "$0")"

echo "--- Starting Clean Environment Setup ---"

PYTHON="${PYTHON:-python3}"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON=python
"$PYTHON" -c 'import sys; assert sys.version_info >= (3, 10), "Python >= 3.10 required"'
echo "[1/5] Python: $("$PYTHON" --version)"

"$PYTHON" -m venv .venv
if [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate          # macOS / Linux
else
    # shellcheck disable=SC1091
    source .venv/Scripts/activate      # Git Bash บน Windows
fi
echo "[2/5] Virtual environment: .venv"

python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
if [ "${1:-}" != "--runtime" ]; then
    python -m pip install --quiet -r requirements-dev.txt
fi
echo "[3/5] Dependencies installed"

if [ ! -f .env ]; then
    cp .env.example .env
    echo "[4/5] Created .env from .env.example"
else
    echo "[4/5] Keeping existing .env"
fi

if [ "${1:-}" != "--runtime" ]; then
    python -m pytest -m smoke -q
    echo "[5/5] Smoke test passed"
else
    echo "[5/5] Skipped smoke test (--runtime)"
fi

echo "--- Installation Completed Successfully ---"
echo "Run the program:  source .venv/bin/activate  (Windows: source .venv/Scripts/activate)"
echo "                  python app_v2.py"
