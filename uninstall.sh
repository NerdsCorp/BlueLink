#!/bin/bash
# BlueLink Advanced Uninstall Script
# WARNING: This will delete BlueLink files, venv, and database!

echo "⚠️  BlueLink Advanced Uninstall Script"
echo "This will remove BlueLink components including the database, venv, and project files."
read -p "Are you sure you want to continue? [y/N]: " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Aborted."
    exit 0
fi

# --- Stop and remove systemd service if it exists ---
if systemctl is-active --quiet bluelink.service; then
    echo "🛑 Stopping BlueLink service..."
    sudo systemctl stop bluelink.service
    sudo systemctl disable bluelink.service
    sudo rm -f /etc/systemd/system/bluelink.service
    sudo systemctl daemon-reload
    echo "✅ Service removed"
fi

# --- Remove virtual environment ---
if [ -d "./venv" ]; then
    echo "🗑️  Removing virtual environment..."
    rm -rf ./venv
fi

# --- Remove database file ---
if [ -f "./bluelink.db" ]; then
    echo "🗑️  Removing database file..."
    rm -f ./bluelink.db
fi

# --- Remove __pycache__ ---
if [ -d "./__pycache__" ]; then
    echo "🗑️  Removing Python cache..."
    rm -rf ./__pycache__
fi

# --- Remove uploaded firmware files if any ---
if [ -d "./uploads" ]; then
    echo "🗑️  Removing uploaded files..."
    rm -rf ./uploads
fi

# --- Optional: Remove arduino-cli ---
read -p "Do you want to remove arduino-cli? [y/N]: " remove_cli

if [[ "$remove_cli" == "y" || "$remove_cli" == "Y" ]]; then
    if [ -f "$HOME/bin/arduino-cli" ]; then
        echo "🗑️  Removing arduino-cli..."
        rm -f "$HOME/bin/arduino-cli"
        echo "✅ arduino-cli removed"
    else
        echo "ℹ️  arduino-cli not found in $HOME/bin"
    fi
fi

# --- Remove project files (optional) ---
read -p "Do you want to delete the entire BlueLink project folder? [y/N]: " delproj
if [[ "$delproj" == "y" || "$delproj" == "Y" ]]; then
    cd ..
    echo "🗑️  Deleting BlueLink project folder..."
    rm -rf ./BlueLink
    echo "✅ BlueLink completely removed!"
else
    echo "✅ BlueLink uninstalled (project files kept)"
fi

echo ""
echo "Done! BlueLink has been uninstalled."
echo ""
echo "If you want to reinstall, run:"
echo "  bash install.sh"