```python
import serial
import serial.tools.list_ports
from time import sleep


class ArduinoManager:
def __init__(self):
self.connections = {}


def list_ports(self):
return [p.device for p in serial.tools.list_ports.comports()]


def connect(self, name, port):
ser = serial.Serial(port, 9600, timeout=1)
sleep(2)
self.connections[name] = ser


def send(self, name, command):
if name in self.connections:
self.connections[name].write(f"{command}\n".encode())
```
