import { useState, useRef, useLayoutEffect, useEffect } from 'react';
import { animateLoadingText } from './loding.js';
import gsap from 'gsap';
import './prdiction.css';
import { Link } from 'react-router-dom';

const BACKEND_URL = "https://crops-dieasese-detection-app-4.onrender.com";

const diseaseInfo = {
  "Healthy": {
    cause: "No disease present.",
    cure: "Maintain proper watering and nutrient levels."
  },
  "Brown Rust": {
    cause: "Fungus Puccinia triticina, favored by cool, moist conditions.",
    cure: "Use resistant wheat varieties and apply fungicides."
  },
  "Yellow Rust": {
    cause: "Fungus Puccinia striiformis, common in cool weather.",
    cure: "Use resistant varieties, remove infected debris, and spray fungicides."
  },
  "Disease": {
    cause: "Unidentified disease symptoms.",
    cure: "Consult agricultural expert and follow general crop hygiene practices."
  }
};

function Prediction() {
  const videoRef = useRef(null);
  const [streaming, setStreaming] = useState(false);
  const [prediction, setPrediction] = useState('');
  const [healthyPercentage, setHealthyPercentage] = useState('');
  const [affectedPercentage, setAffectedPercentage] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".h1", { y: 50, opacity: 0, duration: 1.5 });
      gsap.from(".camera-label", { y: 50, opacity: 0, duration: 1.5 });
      gsap.from(".uploade-icon", { y: 50, opacity: 0, duration: 1.5 });
    });
    return () => ctx.revert();
  }, []);

  useEffect(() => {
    document.title = loading ? 'Predicting...' : 'Disease Prediction';
    if (loading) animateLoadingText();
  }, [loading]);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        await videoRef.current.play();
        setStreaming(true);
        setTimeout(() => {
          captureAndSendImage();
          stopCamera();
        }, 4000);
      }
    } catch (error) {
      console.error('Error accessing camera:', error);
    }
  };

  const captureAndSendImage = async () => {
    if (!videoRef.current) return;

    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      setImageUrl(URL.createObjectURL(blob));
      setLoading(true);

      const formData = new FormData();
      formData.append('image', blob, 'capture.jpg');

      try {
        const response = await fetch(`${BACKEND_URL}/upload`, {
          method: 'POST',
          body: formData
        });
        const data = await response.json();

        setPrediction(data.prediction?.trim() || '');
        setHealthyPercentage(data.healthy || '');
        setAffectedPercentage(data.affected || '');
      } catch (error) {
        console.error('Error sending captured image:', error);
      } finally {
        setLoading(false);
      }
    }, 'image/jpeg');
  };

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    stopCamera();
    setImageUrl(URL.createObjectURL(file));
    setLoading(true);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch(`${BACKEND_URL}/upload`, {
        method: 'POST',
        body: formData
      });
      const data = await response.json();

      setPrediction(data.prediction?.trim() || '');
      setHealthyPercentage(data.healthy || '');
      setAffectedPercentage(data.affected || '');
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setStreaming(false);
    }
  };

  const resetState = () => {
    setPrediction('');
    setHealthyPercentage('');
    setAffectedPercentage('');
    setImageUrl('');
  };

  const trimmedPrediction = prediction.trim();

  return (
    <>
      <nav className="navbar4">
        <div className="navbar-container4">
          <h1 className='h1'>Crops Disease Detection</h1>
          <ul className="nav-links">
            <li><Link to="/homepage">Home</Link></li>
            <li><Link to="/prediction">Disease Detection</Link></li>
            <li><Link to="/about">About</Link></li>
            <li><Link to="/cropsinfromation">Guide</Link></li>
          </ul>
        </div>
      </nav>

      <div className="container">
        <h1 id="heading">Upload Image or Click Image</h1>

        <div className="video-container" style={{ display: streaming ? 'block' : 'none' }}>
          <video ref={videoRef} autoPlay playsInline muted />
        </div>

        <div className="controls">
          <button
            onClick={() => { resetState(); startCamera(); }}
            disabled={streaming}
            id="cameraBtn"
            style={{ display: 'none' }}
          >
            📷
          </button>

          <label htmlFor="cameraBtn" className="camera-label">📷</label>

          <input
            type="file"
            accept="image/*"
            id="fileInput"
            onClick={resetState}
            onChange={handleImageUpload}
            style={{ display: 'none' }}
          />

          <label htmlFor="fileInput" className="uploade-icon">🖼️</label>
        </div>

        {(imageUrl || loading || prediction) && (
          <div className="prediction">
            {imageUrl && (
              <img
                src={imageUrl}
                alt="Uploaded"
                style={{ width: '200px', height: '200px', borderRadius: '20px' }}
              />
            )}

            {loading && (
              <div className="loader">
                <h4>Predicting <span className="loding">...........</span></h4>
              </div>
            )}

            {!loading && prediction && (
              <>
                <h5 className="Loader">Prediction: {trimmedPrediction}</h5>
                {healthyPercentage && <h5 className="Loader">Healthy: {healthyPercentage}%</h5>}
                {affectedPercentage && <h5 className="Loader">Affected: {affectedPercentage}%</h5>}

                {diseaseInfo[trimmedPrediction] && (
                  <>
                    <h5 className="Loader">
                      Cause: {diseaseInfo[trimmedPrediction].cause}
                    </h5>
                    <h5 className="Loader">
                      Cure: {diseaseInfo[trimmedPrediction].cure}
                    </h5>
                  </>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </>
  );
}

export default Prediction;
