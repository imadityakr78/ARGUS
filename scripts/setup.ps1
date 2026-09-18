Write-Host "Setting up ARGUS Skeleton..." -ForegroundColor Cyan

# Check Python
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# Install dependencies
Write-Host "Installing Python dependencies..."
.\venv\Scripts\activate
pip install -r services\api\requirements.txt
pip install pytest

Write-Host "Generating contracts..."
$env:PYTHONPATH = "packages\contracts\python"
python scripts\generate_schemas.py

Write-Host "Seeding mock data..."
python scripts\seed_demo.py

# Check npm
if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) {
    Write-Error "npm is not installed or not in PATH."
    exit 1
}

# Setup Frontend
Write-Host "Installing Frontend dependencies..."
cd apps\web
npm install
cd ..\..

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Run '.\scripts\run_mock_demo.ps1' to start the demo."
