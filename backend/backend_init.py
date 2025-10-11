from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from models import Base, User, Controller, Arduino, Mapping
from utils import get_password_hash

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bluelink.db")
DEFAULT_ADMIN_USER = os.getenv("DEFAULT_ADMIN_USER", "admin")
DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")

# --- Database setup ---
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# --- Create tables ---
print("📦 Creating tables...")
Base.metadata.create_all(bind=engine)

# --- Create default admin user ---
print(f"🔑 Creating default admin user '{DEFAULT_ADMIN_USER}'...")
existing_user = db.query(User).filter_by(username=DEFAULT_ADMIN_USER).first()

if not existing_user:
    admin_user = User(
        username=DEFAULT_ADMIN_USER,
        password_hash=get_password_hash(DEFAULT_ADMIN_PASSWORD)
    )
    db.add(admin_user)
    db.commit()
    print("✅ Admin user created")
else:
    print("ℹ️ Admin user already exists")

# --- Optional: initialize sample devices/mappings ---
print("📦 Initialization complete!")
db.close()
