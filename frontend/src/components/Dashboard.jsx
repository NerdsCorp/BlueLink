import React, { useEffect, useState } from 'react';
import axios from 'axios';
import MappingCanvas from './MappingCanvas';
import ArduinoList from './ArduinoList';


export default function Dashboard({ token }) {
const [arduinos, setArduinos] = useState([]);
const [mappings, setMappings] = useState([]);


useEffect(() => {
const headers = { Authorization: `Bearer ${token}` };
axios.get('/arduinos', { headers }).then((r) => setArduinos(r.data));
axios.get('/mappings', { headers }).then((r) => setMappings(r.data));
}, [token]);


return (
<div className="p-4">
<h1 className="text-2xl font-bold mb-4">Arduino Controller Dashboard</h1>
<ArduinoList arduinos={arduinos} />
<MappingCanvas mappings={mappings} />
</div>
);
}
