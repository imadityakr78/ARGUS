Write-Host "Starting ARGUS Mock Demo..." -ForegroundColor Cyan

$env:ARGUS_USE_MOCKS = "true"

Write-Host "Starting FastAPI Mock Server on port 8000..."
Start-Process pwsh -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\activate; cd services\api; uvicorn app.main:app --reload --port 8000"

Write-Host "Starting Vite Frontend on port 5173..."
cd apps\web
npm run dev
