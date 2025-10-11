```python
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
__tablename__ = 'users'
id = Column(Integer, primary_key=True, index=True)
username = Column(String, unique=True, index=True)
password_hash = Column(String)


class Arduino(Base):
__tablename__ = 'arduinos'
id = Column(Integer, primary_key=True, index=True)
name = Column(String)
port = Column(String)


class Mapping(Base):
__tablename__ = 'mappings'
id = Column(Integer, primary_key=True, index=True)
controller_button = Column(String)
arduino_id = Column(Integer, ForeignKey('arduinos.id'))
arduino_pin = Column(String)
action = Column(String)
config = Column(JSON, default={})
arduino = relationship('Arduino')
```
