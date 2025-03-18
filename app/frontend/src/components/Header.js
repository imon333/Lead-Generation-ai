import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="app-header">
      <div className="container d-flex justify-content-between align-items-center">
        <h1 className="m-0">
          <Link to="/" className="text-white text-decoration-none">
            <i className="fas fa-users me-2"></i>
            Lead Generation AI
          </Link>
        </h1>
        <nav>
          <ul className="nav">
            <li className="nav-item">
              <Link to="/" className="nav-link text-white">Home</Link>
            </li>
            <li className="nav-item">
              <Link to="/results" className="nav-link text-white">Results</Link>
            </li>
            <li className="nav-item">
              <Link to="/settings" className="nav-link text-white">Settings</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header; 