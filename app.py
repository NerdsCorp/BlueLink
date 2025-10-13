"""
BlueLink - Advanced Python + HTML Version
Features:
- PWM support for joysticks/triggers
- Stepper motor control
- Arduino firmware upload from UI
- Advanced pin configurations
"""

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
import serial
import serial.tools.list_ports
import subprocess
import os
import tempfile

# ============================================================================
# CONFIGURATION
# ============================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey-change-in-production")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bluelink.db")
JWT_EXPIRE_MINUTES = 60

# ============================================================================
# DATABASE MODELS
# ============================================================================
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

class Arduino(Base):
    __tablename__ = 'arduinos'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serial_port = Column(String, unique=True, nullable=False)
    board_type = Column(String, default="uno")  # uno, mega, nano, etc.

class Mapping(Base):
    __tablename__ = 'mappings'
    id = Column(Integer, primary_key=True, index=True)
    controller_input = Column(String, nullable=False)  # button, axis, trigger
    input_type = Column(String, default="digital")  # digital, analog, pwm
    arduino_id = Column(Integer, ForeignKey('arduinos.id'))
    arduino_pin = Column(String, nullable=False)
    pin_mode = Column(String, default="output")  # output, pwm, stepper
    
    # PWM settings
    min_value = Column(Integer, default=0)
    max_value = Column(Integer, default=255)
    invert = Column(Boolean, default=False)
    
    # Stepper settings
    stepper_steps = Column(Integer, default=200)  # steps per revolution
    stepper_speed = Column(Integer, default=60)   # RPM
    stepper_pin2 = Column(String, nullable=True)  # second pin for stepper
    stepper_pin3 = Column(String, nullable=True)  # third pin for stepper
    stepper_pin4 = Column(String, nullable=True)  # fourth pin for stepper
    
    arduino = relationship("Arduino")

# ============================================================================
# DATABASE SETUP
# ============================================================================
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# AUTHENTICATION
# ============================================================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401)
    return user

# ============================================================================
# ARDUINO MANAGER
# ============================================================================
class ArduinoManager:
    def __init__(self):
        self.connections = {}
    
    def list_ports(self):
        return [{"device": p.device, "description": p.description, "hwid": p.hwid} 
                for p in serial.tools.list_ports.comports()]
    
    def connect(self, name, port):
        try:
            ser = serial.Serial(port, 115200, timeout=1)
            self.connections[name] = ser
            return True
        except Exception as e:
            print(f"Error connecting to {port}: {e}")
            return False
    
    def disconnect(self, name):
        if name in self.connections:
            self.connections[name].close()
            del self.connections[name]
    
    def send(self, name, command):
        if name in self.connections:
            try:
                self.connections[name].write(f"{command}\n".encode())
                return True
            except Exception as e:
                print(f"Error sending to {name}: {e}")
                return False
        return False
    
    def upload_firmware(self, port, hex_file_path, board_type="arduino:avr:uno"):
        """Upload firmware to Arduino using avrdude"""
        try:
            # Check if arduino-cli is available
            result = subprocess.run(
                ["arduino-cli", "version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return {"success": False, "message": "arduino-cli not found. Please install it first."}
            
            # Upload the firmware
            upload_result = subprocess.run(
                ["arduino-cli", "upload", "-p", port, "-b", board_type, "-i", hex_file_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if upload_result.returncode == 0:
                return {"success": True, "message": "Firmware uploaded successfully!", "output": upload_result.stdout}
            else:
                return {"success": False, "message": "Upload failed", "error": upload_result.stderr}
                
        except subprocess.TimeoutExpired:
            return {"success": False, "message": "Upload timeout - Arduino may not be responding"}
        except Exception as e:
            return {"success": False, "message": f"Upload error: {str(e)}"}
    
    def compile_and_upload(self, port, ino_file_path, board_type="arduino:avr:uno"):
        """Compile and upload .ino file"""
        try:
            # Check arduino-cli
            result = subprocess.run(["arduino-cli", "version"], capture_output=True)
            if result.returncode != 0:
                return {"success": False, "message": "arduino-cli not found"}
            
            # Compile the sketch
            compile_result = subprocess.run(
                ["arduino-cli", "compile", "--fqbn", board_type, ino_file_path],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if compile_result.returncode != 0:
                return {"success": False, "message": "Compilation failed", "error": compile_result.stderr}
            
            # Upload
            upload_result = subprocess.run(
                ["arduino-cli", "upload", "-p", port, "--fqbn", board_type, ino_file_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if upload_result.returncode == 0:
                return {"success": True, "message": "Compiled and uploaded successfully!"}
            else:
                return {"success": False, "message": "Upload failed", "error": upload_result.stderr}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}

arduino_manager = ArduinoManager()

# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ArduinoCreate(BaseModel):
    name: str
    serial_port: str
    board_type: Optional[str] = "uno"

class MappingCreate(BaseModel):
    controller_input: str
    input_type: str = "digital"  # digital, analog, pwm
    arduino_id: int
    arduino_pin: str
    pin_mode: str = "output"  # output, pwm, stepper
    
    # PWM settings
    min_value: Optional[int] = 0
    max_value: Optional[int] = 255
    invert: Optional[bool] = False
    
    # Stepper settings
    stepper_steps: Optional[int] = 200
    stepper_speed: Optional[int] = 60
    stepper_pin2: Optional[str] = None
    stepper_pin3: Optional[str] = None
    stepper_pin4: Optional[str] = None

class PWMCommand(BaseModel):
    arduino_id: int
    pin: str
    value: int  # 0-255

class StepperCommand(BaseModel):
    arduino_id: int
    pins: list[str]  # [pin1, pin2, pin3, pin4]
    steps: int
    speed: int

# ============================================================================
# FASTAPI APP
# ============================================================================
app = FastAPI(title="BlueLink Advanced", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# STARTUP
# ============================================================================
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if not existing:
            admin = User(username="admin", password_hash=get_password_hash("admin123"))
            db.add(admin)
            db.commit()
            print("✅ Created default admin user (username: admin, password: admin123)")
        print("🚀 BlueLink Advanced server started!")
    finally:
        db.close()

# ============================================================================
# API ENDPOINTS
# ============================================================================
@app.post("/login", response_model=Token)
def login(form: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/ports")
def list_serial_ports(user = Depends(get_current_user)):
    return arduino_manager.list_ports()

@app.get("/api/arduinos")
def list_arduinos(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(Arduino).all()

@app.post("/api/arduinos")
def add_arduino(arduino: ArduinoCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    ar = Arduino(**arduino.dict())
    db.add(ar)
    db.commit()
    db.refresh(ar)
    arduino_manager.connect(ar.name, ar.serial_port)
    return ar

@app.delete("/api/arduinos/{arduino_id}")
def delete_arduino(arduino_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    ar = db.query(Arduino).filter(Arduino.id == arduino_id).first()
    if not ar:
        raise HTTPException(status_code=404, detail="Arduino not found")
    arduino_manager.disconnect(ar.name)
    db.query(Mapping).filter(Mapping.arduino_id == arduino_id).delete()
    db.delete(ar)
    db.commit()
    return {"message": "Arduino deleted"}

@app.get("/api/mappings")
def get_mappings(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(Mapping).all()

@app.post("/api/mappings")
def add_mapping(mapping: MappingCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    m = Mapping(**mapping.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@app.delete("/api/mappings/{mapping_id}")
def delete_mapping(mapping_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    m = db.query(Mapping).filter(Mapping.id == mapping_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mapping not found")
    db.delete(m)
    db.commit()
    return {"message": "Mapping deleted"}

@app.post("/api/test-pin")
def test_pin(data: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    arduino_id = data.get("arduino_id")
    pin = data.get("pin")
    
    ar = db.query(Arduino).filter(Arduino.id == arduino_id).first()
    if not ar:
        raise HTTPException(status_code=404, detail="Arduino not found")
    
    success = arduino_manager.send(ar.name, f"TEST:{pin}")
    return {"status": "sent" if success else "failed"}

@app.post("/api/pwm")
def send_pwm(cmd: PWMCommand, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """Send PWM value (0-255) to a pin"""
    ar = db.query(Arduino).filter(Arduino.id == cmd.arduino_id).first()
    if not ar:
        raise HTTPException(status_code=404, detail="Arduino not found")
    
    # Clamp value
    value = max(0, min(255, cmd.value))
    success = arduino_manager.send(ar.name, f"PWM:{cmd.pin}:{value}")
    return {"status": "sent" if success else "failed", "value": value}

@app.post("/api/stepper")
def control_stepper(cmd: StepperCommand, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """Control stepper motor"""
    ar = db.query(Arduino).filter(Arduino.id == cmd.arduino_id).first()
    if not ar:
        raise HTTPException(status_code=404, detail="Arduino not found")
    
    pins_str = ",".join(cmd.pins)
    success = arduino_manager.send(ar.name, f"STEPPER:{pins_str}:{cmd.steps}:{cmd.speed}")
    return {"status": "sent" if success else "failed"}

@app.post("/api/upload-firmware")
async def upload_firmware(
    file: UploadFile = File(...),
    port: str = None,
    board_type: str = "arduino:avr:uno",
    user = Depends(get_current_user)
):
    """Upload .ino or .hex file to Arduino"""
    if not port:
        raise HTTPException(status_code=400, detail="Port required")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        if file.filename.endswith('.ino'):
            result = arduino_manager.compile_and_upload(port, tmp_path, board_type)
        elif file.filename.endswith('.hex'):
            result = arduino_manager.upload_firmware(port, tmp_path, board_type)
        else:
            result = {"success": False, "message": "Only .ino or .hex files supported"}
        
        return result
    finally:
        os.unlink(tmp_path)

@app.get("/api/firmware/bluelink.ino")
def download_firmware():
    """Download the default BlueLink firmware"""
    firmware_path = "BlueLink.ino"
    if os.path.exists(firmware_path):
        return FileResponse(firmware_path, filename="BlueLink.ino", media_type="text/plain")
    raise HTTPException(status_code=404, detail="Firmware file not found")

# ============================================================================
# SERVE HTML FRONTEND
# ============================================================================
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            return HTMLResponse(content=f.read())
    
    return HTMLResponse(content="""
    <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>💙 BlueLink Advanced</h1>
        <p>Create an <code>index.html</code> file in the same directory as <code>app.py</code></p>
        <p>Or use the API directly at <code>/docs</code></p>
        <hr>
        <a href="/docs">📚 API Documentation</a>
    </body></html>
    """)

# ============================================================================
# RUN SERVER
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting BlueLink Server...")
    print("📍 Dashboard: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)