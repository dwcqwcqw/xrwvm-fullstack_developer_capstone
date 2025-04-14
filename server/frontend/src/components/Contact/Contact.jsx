import React from 'react';
import './Contact.css';

function Contact() {
  return (
    <div className="container">
      <h2>Contact Us</h2>
      <div className="contact-form">
        <form>
          <div className="mb-3">
            <label htmlFor="name" className="form-label">Name</label>
            <input type="text" className="form-control" id="name" placeholder="Enter your name" />
          </div>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">Email</label>
            <input type="email" className="form-control" id="email" placeholder="Enter your email" />
          </div>
          <div className="mb-3">
            <label htmlFor="message" className="form-label">Message</label>
            <textarea className="form-control" id="message" rows="5" placeholder="Enter your message"></textarea>
          </div>
          <button type="submit" className="btn btn-primary">Send Message</button>
        </form>
      </div>
    </div>
  );
}

export default Contact; 