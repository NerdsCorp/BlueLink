# 💙 BlueLink

**BlueLink** is an open-source cross-platform controller-to-Arduino mapping system designed to run seamlessly on **Raspberry Pi**, **Steam Deck**, and desktop Linux.  
It connects **Bluetooth controllers** and **multiple configurable Arduinos** to control any hardware project — with a **React + Tailwind web UI** for drag-and-drop mapping, live testing, authentication, and browser-based remote control.

---

## ✨ Core Features

### 🎮 Controller Integration
- Supports most Bluetooth gamepads (Xbox, PS, Switch, etc.)
- Real-time input detection and event streaming
- Multi-controller management with custom profiles

### 🔌 Arduino Connectivity
- Connect multiple Arduinos via USB or Bluetooth
- Auto-detect and register new boards
- Send mapped controller events to Arduino pins
- Full pin control (digital/analog) + test buttons

### 🌐 Web Interface
- Beautiful React + Tailwind dashboard
- Canvas-based visual mapping editor  
  → drag a controller button onto an Arduino pin  
- Live event log and replay system  
- Configurable mappings, triggers, and macros  

### 🔐 Authentication & API
- Username + password login  
- Token-based API authentication  
- Protected configuration endpoints  

### 💾 Persistence
- SQLite storage for users, devices, mappings, and logs  
- Auto-migration and local backups  

### ⚙️ Backend
- Python FastAPI server with REST + WebSocket support  
- Bluetooth + serial communication drivers  
- OTA-ready structure for remote updates  

### 🧭 Frontend
- React + Vite + TailwindCSS  
- Real-time updates over WebSockets  
- Canvas mapping editor with drag-and-drop events  
- Responsive layout for desktop and mobile browsers  

---

## 🖥️ Architecture Overview

[ Bluetooth Controller(s) ]
↓
[ BlueLink Core ]
(FastAPI + SQLite)
↓
[ Web UI / API / Auth Layer ]
↓
[ Arduino(s) via USB/Bluetooth ]



- **Frontend:** React + Tailwind (Vite build)  
- **Backend:** FastAPI (Python 3.10+)  
- **Database:** SQLite  
- **Communication:** WebSocket + REST  
- **Deployment:** Docker or direct install  

---

## ⚡ One-Line Install

Just paste this into your terminal:

```bash
bash <(curl -s https://raw.githubusercontent.com/NerdsCorp/BlueLink/main/install.sh)
```

This will:

Install all dependencies

Clone the repo

Build frontend and backend

Launch the app

🧰 Manual Installation
bash
Copy code
git clone https://github.com/NerdsCorp/BlueLink.git
cd BlueLink

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
bash
Copy code
# Frontend
cd ../frontend
npm install
npm run build
Then open your browser at:
👉 http://localhost:8000

⚙️ Configuration
Edit .env in the backend/ folder:

env
Copy code
APP_ENV=production
APP_PORT=8000
ENABLE_AUTH=true
JWT_SECRET=supersecretkey
DATABASE_URL=sqlite:///bluelink.db
ALLOWED_ORIGINS=http://localhost:5173
🧩 Arduino Setup
Flash your Arduino with the included firmware (/firmware/BlueLink_Arduino.ino)

Connect via USB or Bluetooth serial

Add the device in the Web UI → Devices

Use the Mapping Editor to assign controller inputs to Arduino pins

🌍 Web UI
Login with your created account

Manage controllers and Arduinos

Drag buttons → pin mapping on the canvas

Save configurations to SQLite

Replay past events to verify setups

🐳 Docker Deployment
bash
Copy code
docker compose up -d
This runs:

backend (FastAPI + SQLite)

frontend (React build served via FastAPI)

🔒 Authentication
Login required for all UI and API access

Token-based authentication for automation

Example API call:

bash
Copy code
curl -H "Authorization: Bearer <your_token>" http://localhost:8000/api/mappings
🧠 Database Schema Overview
Table	Description
users	Authenticated users
controllers	Registered Bluetooth devices
arduinos	Connected Arduino boards
mappings	Controller→pin bindings
events	Logged/replayed input events

🧑‍💻 Development
bash
Copy code
# Backend dev
cd backend
uvicorn app:app --reload

# Frontend dev
cd frontend
npm run dev
Frontend runs on http://localhost:5173, backend on http://localhost:8000.

🧩 Systemd Auto-Start (Optional)
Once installed, BlueLink can auto-start at boot:

```bash

sudo systemctl enable bluelink
sudo systemctl start bluelink
```
📦 Repository Structure
```lua
BlueLink/
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── database.py
│   ├── requirements.txt
│   ├── .env
│   └── ...
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── firmware/
│   └── BlueLink_Arduino.ino
├── install.sh
├── docker-compose.yml
└── README.md

```
📜 License
Released under the MIT License — free for personal, educational, and commercial use.

💬 Credits
Built with ❤️ by NerdsCorp
Empowering creators with open hardware, software, and innovation.
