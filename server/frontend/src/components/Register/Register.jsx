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

    try {
      const res = await fetch("/djangoapp/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          userName,
          password,
          email
        }),
      });

      if (!res.ok) {
        const text = await res.text();
        console.error('Registration failed:', text);
        throw new Error(`Registration failed: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      if (data.status === "Authenticated") {
        sessionStorage.setItem('username', data.userName);
        navigate('/');
        window.location.reload();
      } else {
        if (data.error === "Already Registered") {
          setError("This username is already registered. Please try another one.");
        } else {
          setError(data.error || "Registration failed. Please try again.");
        }
      }
    } catch (err) {
      console.error('Error:', err);
      setError("An error occurred during registration. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-box">
        <h2>Create Account</h2>
        <p className="subtitle">Please fill in the details to register</p>

        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={register}>
          <div className="input-group">
            <img src={user_icon} alt="Username" className="input-icon" />
            <input
              type="text"
              placeholder="Username"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              required
              className="form-input"
              minLength="3"
            />
          </div>

          <div className="input-group">
            <img src={email_icon} alt="Email" className="input-icon" />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
              minLength="6"
            />
          </div>

          <button
            type="submit"
            className="register-button"
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div className="login-link">
          Already have an account? <a href="/login">Sign in</a>
        </div>
      </div>
    </div>
  );
};

export default Register; 