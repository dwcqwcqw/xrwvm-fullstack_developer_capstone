import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Register.css";
import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const register = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (!userName || !password || !email) {
      setError("Please fill in all fields");
      setLoading(false);
      return;
    }

    try {
      const res = await fetch("/djangoapp/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userName,
          password,
          email
        }),
      });

      let data;
      const contentType = res.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        data = await res.json();
      } else {
        const text = await res.text();
        throw new Error(text || 'Server error');
      }
      
      if (res.ok && data.status === "Authenticated") {
        sessionStorage.setItem('username', data.userName);
        navigate('/');
        window.location.reload();
      } else {
        if (data.error === "Already Registered") {
          setError("This username is already registered. Please try another one.");
        } else if (data.error) {
          setError(data.error);
        } else {
          setError("Registration failed. Please try again.");
        }
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.message || "An error occurred during registration. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-header">
        <h2>Create Account</h2>
        <p>Please fill in the details to register</p>
      </div>

      {error && (
        <div className="error-message">
          <i className="fas fa-exclamation-circle"></i>
          {error}
        </div>
      )}

      <form onSubmit={register} className="register-form">
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <i className="fas fa-user"></i>
          <input
            type="text"
            id="username"
            placeholder="Enter your username"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            required
            minLength="3"
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <i className="fas fa-envelope"></i>
          <input
            type="email"
            id="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <i className="fas fa-lock"></i>
          <input
            type="password"
            id="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength="6"
          />
        </div>

        <button
          type="submit"
          className="register-btn"
          disabled={loading}
        >
          {loading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>

      <div className="login-link">
        Already have an account? <a href="/login">Sign in</a>
      </div>
    </div>
  );
};

export default Register; 