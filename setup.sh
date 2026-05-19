#!/bin/bash

# ═══════════════════════════════════════════════════════════════════
# KANCHIPURAM BOT - Setup Script for Linux/Mac
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "🎮 KANCHIPURAM BOT - Setup Wizard"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "📝 Checking .env file..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "Creating .env from template..."
    cp .env.template .env
    echo ""
    echo "📋 .env file created - EDIT IT NOW with your values:"
    echo "   • BOT_TOKEN (from Discord Developer Portal)"
    echo "   • GOOGLE_CREDS (from Google Service Account)"
    echo "   • SHEET_NAME (your Google Sheet name)"
    echo ""
    echo "Opening .env for editing (nano)..."
    nano .env
else
    echo "✅ .env file found"
fi

echo ""
echo "🔐 Checking credentials..."
if [ ! -f "credentials.json" ] && [ -z "$GOOGLE_CREDS" ]; then
    echo "⚠️  No Google credentials found!"
    echo ""
    echo "Option 1: Place credentials.json in this folder"
    echo "Option 2: Add GOOGLE_CREDS to .env"
    echo ""
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the bot, run:"
echo "   source venv/bin/activate"
echo "   python bot.py"
echo ""
echo "📚 For help, see:"
echo "   • README.md - Overview and commands"
echo "   • HOSTING.md - Deployment guide"
echo ""
