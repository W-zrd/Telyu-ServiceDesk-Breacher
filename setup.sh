#!/bin/bash

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       Tel-U Service Desk Breacher - Setup Script          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "✓ Python $PYTHON_VERSION found"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "❌ Python 3.7+ required (current: $PYTHON_VERSION)"
    exit 1
fi

if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null && ! command -v chromium &> /dev/null; then
    echo "⚠️  Chrome/Chromium not detected (required for automated login)"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Chrome/Chromium detected"
fi

echo ""
read -p "Create virtual environment? (y/n) " -n 1 -r
echo
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    echo "✓ Dependencies installed in virtual environment"
    USING_VENV=true
else
    if ! command -v pip3 &> /dev/null; then
        echo "❌ pip3 required"
        exit 1
    fi
    pip3 install -r requirements.txt --user --quiet
    echo "✓ Dependencies installed"
    USING_VENV=false
fi

chmod +x cli.py telyu_cli/browser_login.py

echo ""
echo "╔═════════════════════════════════════════════════════════════╗"
echo "║                     ✅ Setup Complete!                      ║"
echo "╚═════════════════════════════════════════════════════════════╝"
echo ""

if [ "$USING_VENV" = true ]; then
    echo "📌 To activate virtual environment in future sessions:"
    echo "   $ source venv/bin/activate"
    echo ""
fi

echo "🚀 Quick Start:"
echo ""
echo "1. Login:              ./cli.py login"
echo "2. View tickets:       ./cli.py tickets"
echo "3. Create ticket:      ./cli.py create-ticket"
echo "4. Comment on ticket:  ./cli.py comment"
echo "5. View ticket detail: ./cli.py ticket --id {id}"
echo ""
