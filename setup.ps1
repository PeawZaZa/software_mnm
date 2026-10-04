# setup.ps1 — ติดตั้ง Inventory System บน Windows PowerShell ด้วยคำสั่งเดียว
#
#   powershell -ExecutionPolicy Bypass -File setup.ps1            ติดตั้ง + dev tools + smoke test
#   powershell -ExecutionPolicy Bypass -File setup.ps1 -Runtime   ติดตั้งเฉพาะที่จำเป็นต่อการรัน
param([switch]$Runtime)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "--- Starting Clean Environment Setup ---"

python -c "import sys; assert sys.version_info >= (3, 10), 'Python >= 3.10 required'"
if ($LASTEXITCODE -ne 0) { throw "Python >= 3.10 is required" }
Write-Host "[1/5] Python: $(python --version)"

python -m venv .venv
. .\.venv\Scripts\Activate.ps1
Write-Host "[2/5] Virtual environment: .venv"

python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
if (-not $Runtime) { python -m pip install --quiet -r requirements-dev.txt }
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }
Write-Host "[3/5] Dependencies installed"

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "[4/5] Created .env from .env.example"
} else {
    Write-Host "[4/5] Keeping existing .env"
}

if (-not $Runtime) {
    python -m pytest -m smoke -q
    if ($LASTEXITCODE -ne 0) { throw "Smoke test failed" }
    Write-Host "[5/5] Smoke test passed"
} else {
    Write-Host "[5/5] Skipped smoke test (-Runtime)"
}

Write-Host "--- Installation Completed Successfully ---"
Write-Host "Run the program:  .\.venv\Scripts\Activate.ps1 ; python app_v2.py"
