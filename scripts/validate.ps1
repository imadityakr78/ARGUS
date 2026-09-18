Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ARGUS Validation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$failed = $false

# Stage 1: Contracts
Write-Host "[1/5] Validating contracts..." -ForegroundColor Yellow
$env:PYTHONPATH = "packages\contracts\python"
python -c "from argus_contracts import *; print('  Contracts import OK')"
if ($LASTEXITCODE -ne 0) { $failed = $true; Write-Error "  Contract import failed." }

# Stage 2: Python tests
Write-Host "[2/5] Running Python tests..." -ForegroundColor Yellow
pytest --tb=short -q
if ($LASTEXITCODE -ne 0) { $failed = $true; Write-Error "  Python tests failed." }

# Stage 3: API startup check
Write-Host "[3/5] Validating API routes..." -ForegroundColor Yellow
# API tests are included in pytest via services/api/tests
Write-Host "  (Covered by pytest)" -ForegroundColor DarkGray

# Stage 4: Frontend TypeScript + build
Write-Host "[4/5] Building frontend..." -ForegroundColor Yellow
Push-Location apps\web
npm run build 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    $failed = $true
    Write-Error "  Frontend build failed."
    npm run build
} else {
    Write-Host "  Frontend build OK" -ForegroundColor DarkGray
}
Pop-Location

# Stage 5: Repository hygiene
Write-Host "[5/5] Repository hygiene..." -ForegroundColor Yellow
$secrets = Select-String -Path (Get-ChildItem -Recurse -Include *.py,*.ts,*.tsx,*.json -Exclude node_modules,venv,.git,dist,build,package-lock.json | Where-Object { $_.FullName -notmatch 'node_modules|venv|\.git|dist|build|package-lock' }) -Pattern "AKIA|password\s*=" -ErrorAction SilentlyContinue
if ($secrets) {
    $failed = $true
    Write-Error "  Potential secrets found!"
    $secrets | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
} else {
    Write-Host "  No secrets detected" -ForegroundColor DarkGray
}

# Result
Write-Host ""
if ($failed) {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ARGUS VALIDATION FAILED" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    exit 1
} else {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ARGUS VALIDATION PASSED" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
}
