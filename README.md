\# 💙 BlueLink Advanced - Simple Python + HTML Version



\*\*No build tools. No npm. No Vite. Just Python and HTML!\*\*



\*\*NEW in v2.0:\*\*

\- 🎚️ \*\*PWM Support\*\* - Control joysticks and triggers with analog values

\- ⚙️ \*\*Stepper Motors\*\* - Full 4-wire stepper motor control

\- 📤 \*\*Firmware Upload\*\* - Flash Arduino directly from the web UI

\- 🔧 \*\*Advanced Mappings\*\* - Complex controller-to-hardware configurations



---



\## 🚀 Quick Start



\### 1. Install Dependencies

```bash

pip install -r requirements.txt

```



\### 2. Run the Server

```bash

python app.py

```



\### 3. Open Your Browser

```

http://localhost:8000

```



\### 4. Login

\- \*\*Username:\*\* `admin`

\- \*\*Password:\*\* `admin123`



---



\## 📁 File Structure



```

BlueLink/

├── app.py              # Single Python file - entire backend!

├── index.html          # Single HTML file - entire frontend!

├── requirements.txt    # Python dependencies

├── BlueLink.ino        # Arduino firmware

└── bluelink.db         # SQLite database (auto-created)

```



\*\*That's it! Just 2 files to edit.\*\*



---



\## 🎛️ How to Use



\### Step 1: Flash Your Arduino

1\. Open `BlueLink.ino` in Arduino IDE

2\. Upload to your Arduino board

3\. Note the serial port (e.g., `/dev/ttyUSB0` or `COM3`)



\### Step 2: Connect Arduino

1\. Go to \*\*Add Arduino\*\* section

2\. Click \*\*🔄 Refresh\*\* to scan ports

3\. Select your Arduino's port

4\. Give it a name (e.g., "Main Board")

5\. Click \*\*Add Arduino\*\*



\### Step 3: Test Pins

1\. Go to \*\*Pin Tester\*\* section

2\. Select your Arduino

3\. Enter a pin number (e.g., `5` or `A0`)

4\. Click \*\*Test Pin\*\* - the pin will blink!



\### Step 4: Create Mappings

1\. Go to \*\*Create Mapping\*\* section

2\. Enter controller button name (e.g., `A`, `B`, `START`)

3\. Select Arduino

4\. Enter pin number (e.g., `13`)

5\. Click \*\*Create Mapping\*\*



Now when you press that button, it will trigger that pin!



---



\## 🔧 Configuration



Create a `.env` file (optional):



```env

SECRET\_KEY=your-secret-key-here

DATABASE\_URL=sqlite:///./bluelink.db

```



---



\## 🎮 Arduino Commands



The Arduino firmware accepts these commands:



\- `SET:5:1` - Set pin 5 HIGH

\- `SET:5:0` - Set pin 5 LOW

\- `TEST:5` - Test pin 5 (blink)

\- `INFO` - Get pin information



---



\## 🐛 Troubleshooting



\### Port Permission Issues (Linux)

```bash

sudo usermod -a -G dialout $USER

\# Then logout and login again

```



\### Arduino Not Detected

1\. Check USB cable is connected

2\. Click \*\*🔄 Refresh Ports\*\*

3\. Make sure Arduino has firmware flashed

4\. Try unplugging and plugging back in



\### Can't Login

\- Default credentials: `admin` / `admin123`

\- Check browser console for errors

\- Make sure server is running on port 8000



---



\## 🔒 Security Note



\*\*Change the default password in production!\*\*



You can modify the startup code in `app.py` or create a new user through the API.



---



\## 📡 API Endpoints



Visit \*\*http://localhost:8000/docs\*\* for interactive API documentation!



Key endpoints:

\- `POST /login` - Get auth token

\- `GET /api/arduinos` - List Arduinos

\- `POST /api/arduinos` - Add Arduino

\- `GET /api/mappings` - List mappings

\- `POST /api/mappings` - Create mapping

\- `POST /api/test-pin` - Test a pin



---



\## 🎨 Customization



\### Change Colors

Edit the CSS in `index.html`:

```css

background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

```



\### Add Features

Everything is in one file, so just edit `app.py` to add new endpoints!



---



\## 📦 What This Does



BlueLink lets you:

1\. \*\*Connect multiple Arduinos\*\* to your computer

2\. \*\*Map controller buttons\*\* to Arduino pins

3\. \*\*Test pins\*\* with a single click

4\. \*\*Control hardware\*\* through a web interface



Perfect for:

\- 🎮 Game controller projects

\- 🤖 Robot control systems

\- 🏠 Home automation

\- 💡 LED controllers

\- 🔊 Audio projects



---



\## ❤️ Credits



Built with simplicity in mind by \*\*NerdsCorp\*\*



\*\*Technologies:\*\*

\- FastAPI (Python web framework)

\- SQLAlchemy (Database)

\- PySerial (Arduino communication)

\- Vanilla JavaScript (No frameworks!)



---



\## 📝 License



MIT License - Free to use and modify!



---



\*\*Need help?\*\* Check the API docs at `/docs` or look at the code - it's all in one place! 🚀

