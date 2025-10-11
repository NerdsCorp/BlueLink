import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import Dashboard from './components/Dashboard';


export default function App() {
const [token, setToken] = useState(localStorage.getItem('token'));


return (
<div className="min-h-screen bg-gray-900 text-white">
{!token ? (
<LoginForm setToken={setToken} />
) : (
<Dashboard token={token} />
)}
</div>
);
}
