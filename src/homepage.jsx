import React from 'react';
import { Link } from 'react-router-dom';
import './Homapage.css';
//import './i18n';
const Homepage = () => {
  return (
    <div className="aboutpage">
           <nav className="navbar">
        <div className="navbar-container2">
          <ul className="nav-links">
            <li>
              <Link to="/homepage" className="nav-link">Home</Link>
            </li>
            <li>
              <Link to="/prediction" className="nav-link">Disease Detection</Link>
            </li>
            <li>
              <Link to="/about" className="nav-link">About</Link>
            </li>
             <li><Link to="/cropsinfromation" className="nav-link active1">Guide</Link></li>            
          </ul>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="hero">
         <h1 className="hero-title">
              Crop Disease <br /> Detection
            </h1>
        <div className="hero-container">
          
          <div className="hero-content">
           
            <p className="hero-description">
              Accelerate better, timely and accurate detection at short notice.
            </p>
            <Link to="/prediction">
              <button className="get-started-btn">Get Started</button>
            </Link>
          </div>

          {/* <div className="hero-image">
            <img
              src="/hello.jpg" // Make sure this image is in the public folder
              alt="Farm Field"
              className="image"
            />
          </div> */}
        </div>
      </div>
    </div>

  );
};

export default Homepage;
