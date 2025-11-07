#!/bin/bash
# BlueLink Advanced Uninstall Script
# WARNING: This will delete BlueLink files, venv, and database!

echo "⚠️  BlueLink Advanced Uninstall Script"
echo "This will remove BlueLink components including the database, venv, and project files."

# --- Determine script directory ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="$(basename "$SCRIPT_DIR")"

# Check if we're in a BlueLink directory
if [ ! -f "$SCRIPT_DIR/app.py" ]; then
    echo "❌ Error: This script must be run from the BlueLink project directory"
    echo "   Expected to find app.py in: $SCRIPT_DIR"
    exit 1
fi

echo "📍 Working in: $SCRIPT_DIR"
echo "📁 Project name: $PROJECT_NAME"
echo ""

read -p "Are you sure you want to continue? [y/N]: " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Aborted."
    exit 0
fi

cd "$SCRIPT_DIR"

# --- Stop and remove systemd service if it exists ---
if systemctl is-active --quiet bluelink.service 2>/dev/null; then
    echo "🛑 Stopping BlueLink service..."
    sudo systemctl stop bluelink.service
    sudo systemctl disable bluelink.service
    sudo rm -f /etc/systemd/system/bluelink.service
    sudo systemctl daemon-reload
    echo "✅ Service removed"
elif systemctl is-enabled --quiet bluelink.service 2>/dev/null; then
    echo "🛑 Removing BlueLink service (not running)..."
    sudo systemctl disable bluelink.service
    sudo rm -f /etc/systemd/system/bluelink.service
    sudo systemctl daemon-reload
    echo "✅ Service removed"
else
    echo "ℹ️  No systemd service found"
fi

# --- Backup database if it exists ---
if [ -f "$SCRIPT_DIR/bluelink.db" ]; then
    read -p "Do you want to backup the database before removing? [Y/n]: " backup_db
    if [[ "$backup_db" != "n" && "$backup_db" != "N" ]]; then
        BACKUP_NAME="bluelink_backup_$(date +%Y%m%d_%H%M%S).db"
        echo "💾 Creating backup: $BACKUP_NAME"
        cp "$SCRIPT_DIR/bluelink.db" "$SCRIPT_DIR/$BACKUP_NAME"
        echo "✅ Backup saved to: $SCRIPT_DIR/$BACKUP_NAME"
    fi
    echo "🗑️  Removing database file..."
    rm -f "$SCRIPT_DIR/bluelink.db"
fi

# --- Remove virtual environment ---
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "🗑️  Removing virtual environment..."
    rm -rf "$SCRIPT_DIR/venv"
fi

# --- Remove __pycache__ ---
if [ -d "$SCRIPT_DIR/__pycache__" ]; then
    echo "🗑️  Removing Python cache..."
    rm -rf "$SCRIPT_DIR/__pycache__"
fi

# --- Remove uploaded firmware files if any ---
if [ -d "$SCRIPT_DIR/uploads" ]; then
    echo "🗑️  Removing uploaded files..."
    rm -rf "$SCRIPT_DIR/uploads"
fi

# --- Remove any .pyc files ---
if find "$SCRIPT_DIR" -name "*.pyc" -type f 2>/dev/null | grep -q .; then
    echo "🗑️  Removing compiled Python files..."
    find "$SCRIPT_DIR" -name "*.pyc" -type f -delete
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
read -p "Do you want to delete the entire project folder? [y/N]: " delproj
if [[ "$delproj" == "y" || "$delproj" == "Y" ]]; then
    PARENT_DIR="$(dirname "$SCRIPT_DIR")"
    echo "⚠️  About to delete: $SCRIPT_DIR"
    read -p "This will PERMANENTLY delete the entire folder. Continue? [y/N]: " final_confirm

    if [[ "$final_confirm" == "y" || "$final_confirm" == "Y" ]]; then
        cd "$PARENT_DIR"
        echo "🗑️  Deleting project folder: $PROJECT_NAME"
        rm -rf "$SCRIPT_DIR"
        echo "✅ BlueLink completely removed!"
        exit 0
    else
        echo "Aborted project deletion."
        echo "✅ BlueLink uninstalled (project files kept)"
    fi
else
    echo "✅ BlueLink uninstalled (project files kept)"
fi

echo ""
echo "Done! BlueLink has been uninstalled."
echo ""
echo "If you want to reinstall, run:"
echo "  bash install.sh"