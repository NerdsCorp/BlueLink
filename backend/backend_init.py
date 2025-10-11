from .database import Base, engine, SessionLocal
from . import models, utils
import os


Base.metadata.create_all(bind=engine)


db = SessionLocal()
username = os.getenv("ADMIN_USERNAME", "admin")
password = os.getenv("ADMIN_PASSWORD", "admin123")


if not db.query(models.User).filter(models.User.username == username).first():
db.add(models.User(username=username, password_hash=utils.get_password_hash(password)))
db.commit()
print(f"✅ Created admin user: {username} / {password}")
else:
print("Admin user already exists.")
