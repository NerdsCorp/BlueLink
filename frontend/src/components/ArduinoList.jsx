```jsx
import React from 'react';
export default function ArduinoList({ arduinos }) {
return (
<div className="mb-4">
<h2 className="text-lg mb-2">Connected Arduinos</h2>
<ul className="bg-gray-800 rounded p-2">
{arduinos.map((a) => (
<li key={a.id}>{a.name} ({a.port})</li>
))}
</ul>
</div>
);
}
```
