import { Routes, Route } from 'react-router-dom';
import Homepage from './homepage';
import Prediction from './prediction';
import About from './About';
import CropInfo from './cropsInfromation';
function App() {
  return (
    <Routes>
      <Route path="/" element={<Homepage />} />
      <Route path="/homepage" element={<Homepage />} />
      <Route path="/prediction" element={<Prediction />} />
      <Route path="/About" element={<About />} />
      <Route path="/cropsInfromation" element={< CropInfo />} />
    </Routes>
  );
}

export default App;
