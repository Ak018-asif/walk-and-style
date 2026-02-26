@echo off
set PATH=C:\Users\asifn\AppData\Local\Programs\Python\Python312;C:\Users\asifn\AppData\Local\Programs\Python\Python312\Scripts;%PATH%
echo Starting Walk n Style Backend...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not found in your PATH.
    echo Please install Python and check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Installing dependencies...
python -m pip install -r backend/requirements.txt

echo.
echo Seeding database...
python backend/seed.py

echo.
echo Starting Server...
echo The API will be available at http://localhost:8000
echo.
uvicorn backend.main:app --reload

pause
