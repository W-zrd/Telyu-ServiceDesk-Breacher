#!/bin/bash

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          Tel-U Service Desk CLI - Setup                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION found"

echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt --quiet

chmod +x cli.py telyu_cli/browser_login.py

echo ""
read -p "Create symlink to /usr/local/bin/telu-cli? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo ln -sf "$(pwd)/cli.py" /usr/local/bin/telu-cli
    echo "✓ Symlink created: telu-cli"
fi

echo ""
echo "╔═════════════════════════════════════════════════════════╗"
echo "║                     Setup Complete!                     ║"
echo "╚═════════════════════════════════════════════════════════╝"
echo ""
echo "Ready to use!"
echo ""
echo "Quick Start:"
echo ""
echo "1. Login:"
echo "   $ ./cli.py login"
echo ""
echo "2. Complete Microsoft SSO + OTP in the browser"
echo ""
echo "3. Use the CLI:"
echo "   $ ./cli.py tickets --username {username}"
echo "   $ ./cli.py tickets --username {username} --status new"
echo "   $ ./cli.py tickets --username {username} --status in-progress"
echo ""
echo "See README.md for full documentation"
echo ""
