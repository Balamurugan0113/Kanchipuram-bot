#!/bin/bash

# ═══════════════════════════════════════════════════════════════════
# KANCHIPURAM BOT - Run Script (Linux/Mac)
# Uses Python 3.11 (compatible version)
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "🎮 Starting Kanchipuram Bot..."
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ ERROR: .env file not found!"
    echo ""
    echo "Please create a .env file with your Discord token:"
    echo ""
    echo "Example .env:"
    echo "  BOT_TOKEN=your_discord_token_here"
    echo "  SHEET_NAME=Kanchipuram FiveM Logs"
    echo "  MANAGER_ROLE=Server Developers"
    echo "  MEMBER_ROLE=KPM Recycle"
    echo ""
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
fi

# Try Python 3.11 first, then fall back to python3
echo "🔍 Checking Python version..."
if command -v python3.11 &> /dev/null; then
    echo "✅ Running with Python 3.11"
    python3.11 bot.py
elif command -v python3 &> /dev/null; then
    echo "⚠️  Using default Python 3"
    python3 bot.py
else
    echo "❌ Python 3 not found!"
    exit 1
fi
