```python
import asyncio
import evdev
from fastapi import WebSocket


connected_clients = []


async def controller_handler(websocket: WebSocket):
await websocket.accept()
connected_clients.append(websocket)
try:
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
if 'controller' in device.name.lower():
async for event in device.async_read_loop():
await websocket.send_json({'code': event.code, 'value': event.value})
except Exception as e:
print(f"Error: {e}")
finally:
connected_clients.remove(websocket)
```
