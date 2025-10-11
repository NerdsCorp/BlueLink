from fastapi import FastAPI, Depends, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models, schemas, utils, auth, arduinos, controllers
import os


app = FastAPI()
Base.metadata.create_all(bind=engine)


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


@app.post("/login", response_model=schemas.Token)
def login(form: schemas.UserLogin, db: Session = Depends(get_db)):
user = auth.authenticate_user(db, form.username, form.password)
if not user:
raise HTTPException(status_code=400, detail="Invalid credentials")
token = auth.create_access_token({"sub": user.username})
return {"access_token": token, "token_type": "bearer"}


@app.get("/arduinos")
def list_arduinos(db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
return db.query(models.Arduino).all()


@app.post("/arduinos")
def add_arduino(a: schemas.ArduinoCreate, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
ar = models.Arduino(**a.dict())
db.add(ar)
db.commit()
db.refresh(ar)
return ar


@app.get("/mappings")
def get_mappings(db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
return db.query(models.Mapping).all()


@app.post("/mappings")
def add_mapping(m: schemas.MappingCreate, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
mapping = models.Mapping(**m.dict())
db.add(mapping)
db.commit()
db.refresh(mapping)
return mapping


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
await controllers.controller_handler(websocket)


if os.path.exists("frontend_build"):
app.mount("/", StaticFiles(directory="frontend_build", html=True), name="frontend")
@app.get("/{path:path}")
async def serve_frontend():
return FileResponse("frontend_build/index.html")
