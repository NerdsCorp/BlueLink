import React, { useEffect, useRef } from 'react';
export default function MappingCanvas({ mappings }) {
const canvasRef = useRef(null);
useEffect(() => {
const ctx = canvasRef.current.getContext('2d');
ctx.fillStyle = '#111';
ctx.fillRect(0, 0, 800, 400);
ctx.fillStyle = '#0f0';
mappings.forEach((m, i) => {
ctx.fillText(`${m.controller_button} -> ${m.arduino_pin}`, 20, 40 + i * 20);
});
}, [mappings]);
return (
<canvas ref={canvasRef} width="800" height="400" className="border border-gray-700 rounded" />
);
}
