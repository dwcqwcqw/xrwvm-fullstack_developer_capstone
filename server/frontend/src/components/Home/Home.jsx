import React from 'react';
import './Home.css';

function Home() {
  return (
    <div className="container">
      <div className="jumbotron">
        <h1 className="display-4">Welcome to Dealership Review</h1>
        <p className="lead">Find the best car dealerships and read reviews from real customers.</p>
        <hr className="my-4" />
        <p>Browse through our list of dealerships and find the perfect one for your needs.</p>
        <a className="btn btn-primary btn-lg" href="/dealers" role="button">View Dealers</a>
      </div>
    </div>
  );
}

export default Home; 