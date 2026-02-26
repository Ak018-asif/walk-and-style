@echo off
echo Starting Walk n Style Frontend...
echo.

echo Installing dependencies...
cmd /c "npm install"

echo.
echo Starting Development Server...
cmd /c "npm run dev"

pause
