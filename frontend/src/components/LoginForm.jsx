import React, { useState } from 'react';
import axios from 'axios';


export default function LoginForm({ setToken }) {
const [username, setUsername] = useState('');
const [password, setPassword] = useState('');


const login = async (e) => {
e.preventDefault();
const res = await axios.post('/login', { username, password });
localStorage.setItem('token', res.data.access_token);
setToken(res.data.access_token);
};


return (
<div className="flex flex-col items-center justify-center h-screen">
<form onSubmit={login} className="bg-gray-800 p-6 rounded-lg shadow-lg w-80">
<h2 className="text-xl mb-4 text-center">Login</h2>
<input className="w-full mb-3 p-2 rounded" placeholder="Username" onChange={(e)=>setUsername(e.target.value)} />
<input className="w-full mb-3 p-2 rounded" placeholder="Password" type="password" onChange={(e)=>setPassword(e.target.value)} />
<button className="bg-blue-500 hover:bg-blue-600 w-full p-2 rounded">Login</button>
</form>
</div>
);
}
