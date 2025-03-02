import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// Login Component
function Login({ setIsAuthenticated }) {
    const navigate = useNavigate();
    const [credentials, setCredentials] = useState({
      username: '',
      password: ''
    });
  
    const handleLogin = async (e) => {
      e.preventDefault();
      try {
        const response = await axios.post('/api/login/', credentials);
        localStorage.setItem('token', response.data.token);
        setIsAuthenticated(true);
        navigate('/search');
      } catch (error) {
        console.error('Login failed:', error);
      }
    };
  
    return (
      <div className='register-page'>
        <div className="auth-form">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Username"
            required
            onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
          />
          <input
            type="password"
            placeholder="Password"
            required
            onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
          />
          <button type="submit">Login</button>
        </form>
      </div>
      </div>
      
    );
  }


  export default Login;