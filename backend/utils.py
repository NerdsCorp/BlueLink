# utils.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Ensure bcrypt max 72-byte limit
    if len(password) > 72:
        print("⚠️ Password longer than 72 characters, truncating to 72 bytes for bcrypt.")
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
