
import { Link } from 'react-router-dom';
import './cropInfo.css';

export default function CropsInformation() {
 

  return (
    <>
      <nav className="navbar">
        <div className="nav-brand">
          <h1>Guide</h1>
        </div>
        <ul className="nav-links">
          <li><Link to="/homepage" className="nav-link">Home</Link></li>
          <li><Link to="/prediction" className="nav-link">Disease Detection</Link></li>
          <li><Link to="/about" className="nav-link">About</Link></li>
          <li><Link to="/cropsInfromation" className="nav-link active1">Guide</Link></li>
        </ul>
      </nav>
      <div className="informstion">
        <h1>How to use  this website</h1>
        <br /><br /><br />
        <h3>1.First cut one leaf form tree or plant</h3>
        <img src="/cut_leaf.jpg" alt="img" />
        <br /><br /><br />
        <h3>2.Wash the leaves thoroughly with clean water</h3>
        <img src="/wash_leaf.jpg" alt="img" />
        <br /><br /><br />
        <h3>3.Than clike image directly or <br />
        save image in Gallary and select from gallary</h3>
        <img src="/upoaldess.jpg" alt="img" />
      </div>
     
    </>
  );
}
