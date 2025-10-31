# Quick Installation Script
# Run this in PowerShell to set up gdrive-toolkit

Write-Host "=" -NoNewline; Write-Host ("=" * 68)
Write-Host "gdrive-toolkit - Quick Setup" -ForegroundColor Cyan
Write-Host "=" -NoNewline; Write-Host ("=" * 68)
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check if in correct directory
if (-not (Test-Path "setup.py")) {
    Write-Host "  ✗ Please run this script from gdrive-toolkit root directory" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Installing gdrive-toolkit in development mode..." -ForegroundColor Yellow
pip install -e .

Write-Host ""
Write-Host "Running installation test..." -ForegroundColor Yellow
python tests\test_install.py

Write-Host ""
Write-Host "=" -NoNewline; Write-Host ("=" * 68)
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline; Write-Host ("=" * 68)
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Setup credentials: python setup_credentials.py"
Write-Host "2. Read quick start: docs\QUICK_START.md"
Write-Host "3. Try examples: python examples\basic_usage.py"
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  - Quick Start: docs\QUICK_START.md"
Write-Host "  - API Reference: docs\API_REFERENCE.md"
Write-Host "  - Credentials: docs\CREDENTIALS_SETUP.md"
Write-Host "  - Commands: COMMANDS.md"
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
