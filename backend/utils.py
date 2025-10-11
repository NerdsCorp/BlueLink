# utils.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash a password with bcrypt.
    Bcrypt has a 72-byte limit, so truncate if necessary.
    """
    # Convert to bytes to check length
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        print("⚠️ Password longer than 72 bytes, truncating to 72 bytes for bcrypt.")
        password_bytes = password_bytes[:72]
    return pwd_context.hash(password_bytes)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
