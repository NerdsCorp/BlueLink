# utils.py
# BlueLink utility functions for authentication and hashing

from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------
# Hash a password
# -----------------------------
def get_password_hash(password: str) -> str:
    # bcrypt has a 72-byte limit, truncate if longer
    password = password[:72]
    return pwd_context.hash(password)

# -----------------------------
# Verify a password
# -----------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
