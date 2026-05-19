@echo off
REM ═══════════════════════════════════════════════════════════════════
REM   KANCHIPURAM BOT - Run Script (Windows)
REM   Uses Python 3.11 (compatible version)
REM ═══════════════════════════════════════════════════════════════════

echo.
echo 🎮 Starting Kanchipuram Bot...
echo.

REM Check if .env file exists
if not exist .env (
    echo ❌ ERROR: .env file not found!
    echo.
    echo Please create a .env file with your Discord token:
    echo.
    echo Example .env:
    echo   BOT_TOKEN=your_discord_token_here
    echo   SHEET_NAME=Kanchipuram FiveM Logs
    echo   MANAGER_ROLE=Server Developers
    echo   MEMBER_ROLE=KPM Recycle
    echo.
    pause
    exit /b 1
)

REM Run bot with Python 3.11
echo Checking Python 3.11...
py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Python 3.11 not found. Trying default Python...
    python bot.py
) else (
    echo ✅ Running with Python 3.11
    py -3.11 bot.py
)

pause
