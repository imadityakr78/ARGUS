Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ARGUS Doctor — Environment Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ok = $true

# Python
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    $pyver = python --version 2>&1
    Write-Host "[OK] Python: $pyver" -ForegroundColor Green
} else {
    Write-Host "[MISSING] Python is not installed or not in PATH." -ForegroundColor Red
    $ok = $false
}

# Node
if (Get-Command "node" -ErrorAction SilentlyContinue) {
    $nodever = node --version 2>&1
    Write-Host "[OK] Node.js: $nodever" -ForegroundColor Green
} else {
    Write-Host "[MISSING] Node.js is not installed or not in PATH." -ForegroundColor Red
    $ok = $false
}

# npm
if (Get-Command "npm" -ErrorAction SilentlyContinue) {
    $npmver = npm --version 2>&1
    Write-Host "[OK] npm: $npmver" -ForegroundColor Green
} else {
    Write-Host "[MISSING] npm is not installed or not in PATH." -ForegroundColor Red
    $ok = $false
}

# Virtual environment
if (Test-Path "venv\Scripts\python.exe") {
    Write-Host "[OK] Python venv exists" -ForegroundColor Green
} else {
    Write-Host "[MISSING] venv not found. Run .\scripts\setup.ps1" -ForegroundColor Yellow
}

# Frontend node_modules
if (Test-Path "apps\web\node_modules") {
    Write-Host "[OK] Frontend node_modules installed" -ForegroundColor Green
} else {
    Write-Host "[MISSING] apps\web\node_modules not found. Run .\scripts\setup.ps1" -ForegroundColor Yellow
}

# .env file
if (Test-Path ".env") {
    Write-Host "[OK] .env file present" -ForegroundColor Green
} else {
    Write-Host "[INFO] No .env file. Copy .env.example to .env if needed." -ForegroundColor Yellow
}

# Mock data
if (Test-Path "mocks\investigations\inv_001.json") {
    Write-Host "[OK] Mock data seeded" -ForegroundColor Green
} else {
    Write-Host "[MISSING] Mock data not found. Run: python scripts\seed_demo.py" -ForegroundColor Yellow
}

Write-Host ""
if ($ok) {
    Write-Host "Environment looks ready." -ForegroundColor Green
} else {
    Write-Host "Some prerequisites are missing. See above." -ForegroundColor Red
}
