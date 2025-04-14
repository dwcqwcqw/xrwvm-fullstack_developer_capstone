import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "./Login.css";
import user_icon from "../assets/person.png";
import password_icon from "../assets/password.png";

const Login = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const login = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("/djangoapp/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          userName,
          password
        }),
      });

      if (!res.ok) {
        const text = await res.text();
        console.error('Login failed:', text);
        throw new Error(`Login failed: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      
      if (data.status === "Authenticated") {
        sessionStorage.setItem('username', data.userName);
        navigate('/');
        window.location.reload();
      } else {
        setError("Invalid username or password");
      }
    } catch (err) {
      console.error('Login error:', err);
      setError("An error occurred during login. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Welcome Back</h2>
        <p className="subtitle">Please sign in to continue</p>
        
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={login}>
          <div className="input-group">
            <img src={user_icon} alt="Username" className="input-icon" />
            <input
              type="text"
              placeholder="Username"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              required
              className="form-input"
            />
          </div>

          <div className="input-group">
            <img src={password_icon} alt="Password" className="input-icon" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="form-input"
            />
          </div>

          <button 
            type="submit" 
            className="login-button" 
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="register-link">
          Don't have an account? <a href="/register">Register now</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
