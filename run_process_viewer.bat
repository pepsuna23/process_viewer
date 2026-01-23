@echo off
rem Change directory to the script's location
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found! Please ensure 'venv' is created in this directory.
    pause
    exit /b
)

echo Starting Flask Server...
echo The browser should open automatically.
echo Keep this window open to keep the server running.
echo To stop the server, press Ctrl+C or close this window.

.\venv\Scripts\python.exe app.py