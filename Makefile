.PHONY: setup dev test validate mock-demo clean

setup:
	pwsh -ExecutionPolicy Bypass -File scripts/setup.ps1

dev:
	pwsh -ExecutionPolicy Bypass -Command "Start-Process pwsh -ArgumentList '-NoExit', '-Command', 'cd services/api; uvicorn app.main:app --reload'; Start-Process pwsh -ArgumentList '-NoExit', '-Command', 'cd apps/web; npm run dev'"

test:
	pytest
	cd apps/web && npm test

validate:
	pwsh -ExecutionPolicy Bypass -File scripts/validate.ps1

mock-demo:
	pwsh -ExecutionPolicy Bypass -File scripts/run_mock_demo.ps1

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf apps/web/node_modules
	rm -rf venv
