@echo off
REM ═══════════════════════════════════════════════════════════════════
REM   KANCHIPURAM BOT - Setup Script for Windows
REM ═══════════════════════════════════════════════════════════════════

echo.
echo 🎮 KANCHIPURAM BOT - Setup Wizard
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if venv exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment exists
)

echo.
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 📚 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Dependencies installed

echo.
echo 📝 Checking .env file...
if not exist .env (
    echo ⚠️  .env file not found!
    echo.
    echo Creating .env from template...
    copy .env.template .env
    echo.
    echo 📋 .env file created - EDIT IT NOW with your values:
    echo    • BOT_TOKEN (from Discord Developer Portal)
    echo    • GOOGLE_CREDS (from Google Service Account)
    echo    • SHEET_NAME (your Google Sheet name)
    echo.
    echo Opening .env for editing...
    notepad .env
) else (
    echo ✅ .env file found
)

echo.
echo 🔐 Checking credentials...
if not exist credentials.json (
    if not defined GOOGLE_CREDS (
        echo ⚠️  No Google credentials found!
        echo.
        echo Option 1: Place credentials.json in this folder
        echo Option 2: Add GOOGLE_CREDS to .env
        echo.
        pause
    )
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo ✅ Setup complete!
echo.
echo 🚀 To start the bot, run:
echo    python bot.py
echo.
echo 📚 For help, see:
echo    • README.md - Overview and commands
echo    • HOSTING.md - Deployment guide
echo.
pause
