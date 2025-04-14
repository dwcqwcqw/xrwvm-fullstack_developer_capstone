import React from 'react';
import './About.css';

function About() {
  return (
    <div className="container">
      <div className="about-content">
        <h2>About Us</h2>
        <p className="lead">
          Welcome to Dealership Review, your trusted platform for finding and reviewing car dealerships.
        </p>
        <div className="about-section">
          <h3>Our Mission</h3>
          <p>
            We aim to provide transparent and honest reviews of car dealerships to help you make informed decisions
            when purchasing your next vehicle. Our platform connects car buyers with dealerships and facilitates
            open communication through customer reviews and ratings.
          </p>
        </div>
        <div className="about-section">
          <h3>Why Choose Us</h3>
          <ul>
            <li>Verified dealer reviews from real customers</li>
            <li>Comprehensive dealership information</li>
            <li>Easy-to-use platform</li>
            <li>Unbiased and transparent feedback system</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default About; 