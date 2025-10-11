#!/bin/bash
# BlueLink Complete Uninstall Script
# WARNING: This will delete BlueLink files, venv, database, and packages!

echo "⚠️  BlueLink Uninstall Script"
echo "This will remove all BlueLink components including the database, venv, and project files."
read -p "Are you sure you want to continue? [y/N]: " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Aborted."
    exit 0
fi

# 1️⃣ Remove virtual environment
if [ -d "./backend/venv" ]; then
    echo "🗑️  Removing virtual environment..."
    rm -rf ./backend/venv
fi

# 2️⃣ Remove database file
if [ -f "./backend/bluelink.db" ]; then
    echo "🗑️  Removing database file..."
    rm -f ./backend/bluelink.db
fi

# 3️⃣ Remove installed Python packages globally (only if you installed them globally)
echo "🗑️  Removing global BlueLink-related Python packages..."
pip uninstall -y fastapi uvicorn sqlalchemy pydantic pyserial python-dotenv python-jose passlib bcrypt

# 4️⃣ Remove project files (optional)
read -p "Do you want to delete the entire BlueLink project folder as well? [y/N]: " delproj
if [[ "$delproj" == "y" || "$delproj" == "Y" ]]; then
    cd ..
    echo "🗑️  Deleting BlueLink project folder..."
    rm -rf ./BlueLink
fi

echo "✅ BlueLink uninstall complete."
