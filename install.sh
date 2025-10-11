#!/bin/bash
set -e

echo "🚀 Installing BlueLink with autostart..."

# --- System update & dependencies ---
sudo apt update && sudo apt install -y python3 python3-venv python3-pip npm git curl

# --- Clone or update repo ---
if [ ! -d "BlueLink" ]; then
  git clone https://github.com/NerdsCorp/BlueLink.git
  cd BlueLink
else
  cd BlueLink
  git pull
fi

# --- Backend setup ---
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend_init.py
deactivate
cd ..

# --- Frontend setup ---
echo "🎨 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# --- Create systemd service ---
SERVICE_PATH="/etc/systemd/system/bluelink.service"
echo "🧰 Creating systemd service at $SERVICE_PATH"

sudo bash -c "cat > $SERVICE_PATH" <<'EOF'
[Unit]
Description=BlueLink Controller Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/$USER/BlueLink/backend
ExecStart=/home/$USER/BlueLink/backend/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
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

echo "✅ BlueLink installed and running!"
echo "🌐 Access the web UI at: http://$(hostname -I | awk '{print $1}'):8000"
