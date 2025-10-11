from passlib.context import CryptContext
from passlib import pwd

# Force Passlib to use the pure-Python backend to avoid __about__ errors
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b",  # safest identifier
    bcrypt__backend="python"  # <<< force pure-Python backend
)

def get_password_hash(password: str) -> str:
    # truncate to 72 bytes to satisfy bcrypt
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    return pwd_context.hash(password_bytes)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    return pwd_context.verify(password_bytes, hashed_password)
