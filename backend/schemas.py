```python
from pydantic import BaseModel


class Token(BaseModel):
access_token: str
token_type: str


class UserLogin(BaseModel):
username: str
password: str


class ArduinoBase(BaseModel):
name: str
port: str


class ArduinoCreate(ArduinoBase):
pass


class ArduinoResponse(ArduinoBase):
id: int
class Config:
orm_mode = True


class MappingBase(BaseModel):
controller_button: str
arduino_id: int
arduino_pin: str
action: str


class MappingCreate(MappingBase):
pass


class MappingResponse(MappingBase):
id: int
class Config:
orm_mode = True
```
