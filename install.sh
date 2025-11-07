#!/bin/bash
set -e

echo "🚀 Installing BlueLink Advanced (Simplified Version)..."

# --- Determine installation directory ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR=""

# Check if we're already in the BlueLink directory
if [ -f "$SCRIPT_DIR/app.py" ] && [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "✅ Running from BlueLink directory"
    INSTALL_DIR="$SCRIPT_DIR"
    cd "$INSTALL_DIR"
else
    echo "❌ Error: This script must be run from the BlueLink project directory"
    echo "   Expected to find app.py and requirements.txt in: $SCRIPT_DIR"
    exit 1
fi

# --- System update & dependencies ---
echo "📦 Installing system dependencies..."
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git curl

# --- Validate required files exist ---
echo "🔍 Validating project files..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    exit 1
fi

if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found!"
    exit 1
fi

if [ ! -f "index.html" ]; then
    echo "⚠️  Warning: index.html not found. Web UI may not work properly."
fi

# --- Setup Python virtual environment ---
echo "🐍 Setting up Python virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists, recreating..."
    rm -rf venv
fi
python3 -m venv venv
source venv/bin/activate

# --- Install Python dependencies ---
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install Python dependencies"
    exit 1
fi

# --- Test run ---
echo "✅ Installation complete!"
echo ""
echo "To start BlueLink manually:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""

# --- Optional: Install arduino-cli ---
read -p "Do you want to install arduino-cli for firmware upload? [y/N]: " install_cli

if [[ "$install_cli" == "y" || "$install_cli" == "Y" ]]; then
    echo "📥 Installing arduino-cli..."
    curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
    export PATH=$PATH:$HOME/bin
    
    echo "📦 Installing Arduino AVR boards..."
    arduino-cli core update-index
    arduino-cli core install arduino:avr
    
    echo "✅ arduino-cli installed!"
    echo "💡 Add this to your ~/.bashrc or ~/.zshrc:"
    echo "   export PATH=\$PATH:\$HOME/bin"
fi

# --- Optional: Create systemd service ---
read -p "Do you want to enable autostart on boot? [y/N]: " autostart

if [[ "$autostart" == "y" || "$autostart" == "Y" ]]; then
    SERVICE_PATH="/etc/systemd/system/bluelink.service"
    
    echo "🧰 Creating systemd service at $SERVICE_PATH"
    
    sudo bash -c "cat > $SERVICE_PATH" <<EOF
[Unit]
Description=BlueLink Advanced Controller Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/app.py
Restart=always
User=$USER
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

    # --- Reload & enable service ---
    echo "🔄 Enabling BlueLink autostart..."
    sudo systemctl daemon-reload
    sudo systemctl enable bluelink.service
    sudo systemctl start bluelink.service
    
    echo "✅ BlueLink is now running as a service!"
    echo "🌐 Access the web UI at: http://$(hostname -I | awk '{print $1}'):8000"
    echo ""
    echo "Useful commands:"
    echo "  sudo systemctl status bluelink    # Check status"
    echo "  sudo systemctl stop bluelink      # Stop service"
    echo "  sudo systemctl restart bluelink   # Restart service"
    echo "  sudo journalctl -u bluelink -f    # View logs (follow mode)"
    echo "  sudo journalctl -u bluelink -n 50 # View last 50 log lines"
else
    echo ""
    echo "To start BlueLink now:"
    echo "  source venv/bin/activate"
    echo "  python app.py"
    echo ""
    echo "Then visit: http://localhost:8000"
fi

echo ""
echo "📝 Default credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🎉 Happy building!"
echo ""
echo "💡 Features:"
echo "   ✅ PWM Control (joysticks, triggers)"
echo "   ✅ Stepper Motor Support"
echo "   ✅ Firmware Upload from UI"
echo "   ✅ Advanced Mappings"
echo ""