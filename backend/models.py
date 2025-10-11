# models.py
# BlueLink SQLAlchemy models

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# -----------------------------
# User Table
# -----------------------------
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

# -----------------------------
# Controller Table
# -----------------------------
class Controller(Base):
    __tablename__ = 'controllers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=True)
    serial_id = Column(String, unique=True, nullable=True)

# -----------------------------
# Arduino Table
# -----------------------------
class Arduino(Base):
    __tablename__ = 'arduinos'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serial_port = Column(String, unique=True, nullable=True)

# -----------------------------
# Mapping Table
# -----------------------------
class Mapping(Base):
    __tablename__ = 'mappings'

    id = Column(Integer, primary_key=True, index=True)
    controller_id = Column(Integer, ForeignKey('controllers.id'))
    arduino_id = Column(Integer, ForeignKey('arduinos.id'))
    controller_button = Column(String, nullable=False)
    arduino_pin = Column(String, nullable=False)

    controller = relationship("Controller")
    arduino = relationship("Arduino")
