// HomePage.js
import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="container">
      <h2>Welcome to the Home Page</h2>

      {/* Button Container */}
      <div className="button-container">
        <Link to="/toxic-classifier" className="btn btn-primary redirect-button">
          Toxic Classifier
        </Link>
        <Link to="/topic-modeling" className="btn btn-success redirect-button">
          Topic Identification
        </Link>
      </div>
    </div>
  );
};

export default HomePage;
