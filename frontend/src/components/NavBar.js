// NavBar.js
import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav className="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
      <Link className="navbar-brand" to="/">Home Page</Link>
      <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse"
        aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarCollapse">
        <ul className="navbar-nav mr-auto">
          <li className="nav-item">
            <Link className="nav-link" to="/toxic-classifier">Toxic Classifier</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/topic-modeling">Topic Identification</Link>
          </li>
          {/* Add more navigation items as needed */}
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
