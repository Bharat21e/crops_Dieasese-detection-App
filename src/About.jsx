import React from 'react';
import { Link } from 'react-router-dom';
import './About.css';
import './Homapage.css';
const About = () => {
  return (
    <div className="about-page">
      {/* Navbar */}
      <nav className="navbarA">
        <div className="navbar-containerA">
          <ul className="nav-links">
            <li><Link to="/homepage" className="nav-link">Home</Link></li>
            <li><Link to="/prediction" className="nav-link">Disease Detection</Link></li>
            <li><Link to="/about" className="nav-link active">About</Link></li>
            <li><Link to="/cropsinfromation" className="nav-link active1">Guide</Link></li>
          </ul>
        </div>
      </nav>

      {/* About Content */}
      <section className="hero1">
        <div className="image-box">
          <img src="/leaf.png" alt="Leaf" className="about-image" />
          <p>
            Welcome to [Your Website Name], an intelligent platform designed to help 
            farmers and agricultural experts detect crop diseases early and accurately. 
            Our mission is to leverage the power of Artificial Intelligence and Machine Learning
            to ensure healthy crops, reduce losses, and promote sustainable farming.
          </p><br /><br />
          <p>
            Using advanced image recognition techniques, our system analyzes
            pictures of crops and identifies potential diseases affecting wheat, rice, and pulses.
            Whether you're in the field or at home, simply upload or capture an image of your
            crop, and our system will provide a quick diagnosis along with useful suggestions for
          </p><br /><br />
          <p>
            Real-time crop disease detection using AI
            
            📷 Camera and file upload support for easy image input
            
            📊 Instant prediction results with accuracy indicators
            
            💡 Expert suggestions for disease management
            
            📚 Educational insights on crop care and disease prevention
          </p>
        </div>

        <div className="details-box">
          <h2>Contact Us</h2>
          <p>For any questions and feedback:</p><br /><br />
          <p><strong>Phone:</strong> 000-000-0000</p><br /><br />
          <p><strong>Email:</strong> djfjsnflsdds@gmail.com</p><br /><br />

       
        </div>
      </section>
    </div>
  );
};

export default About;
