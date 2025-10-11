from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from . import models, utils
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def authenticate_user(db: Session, username: str, password: str):
user = db.query(models.User).filter(models.User.username == username).first()
if not user or not utils.verify_password(password, user.password_hash):
return None
return user


def create_access_token(data: dict):
to_encode = data.copy()
expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
to_encode.update({"exp": expire})
return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
try:
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
username: str = payload.get("sub")
if username is None:
raise HTTPException(status_code=401)
except JWTError:
raise HTTPException(status_code=401)
user = db.query(models.User).filter(models.User.username == username).first()
if user is None:
raise HTTPException(status_code=401)
return user
