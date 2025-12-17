import { useState, useRef, useLayoutEffect, useEffect } from 'react';
import { animateLoadingText } from './loding.js';
import gsap from 'gsap';
import './prdiction.css';
import { Link } from 'react-router-dom';

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
  },
    "Apple___Apple_scab": {
        "cause": "Fungus Venturia inaequalis. Favorable conditions are cool, wet weather.",
        "cure": "Use fungicides and resistant apple varieties. Prune and destroy infected leaves."
    },
    "Apple___Black_rot": {
        "cause": "Caused by the fungus Botryosphaeria obtusa.",
        "cure": "Prune and remove infected areas. Apply fungicides during the growing season."
    },
    "Apple___Cedar_apple_rust": {
        "cause": "Fungus Gymnosporangium juniperi-virginianae. Requires junipers as an alternate host.",
        "cure": "Remove nearby juniper hosts. Use resistant varieties and fungicides."
    },
    "Apple___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Background_without_leaves": {
        "cause": "No disease or plant detected.",
        "cure": "Not applicable."
    },
    "Blueberry___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Cherry___Powdery_mildew": {
        "cause": "Fungus Podosphaera clandestina.",
        "cure": "Apply sulfur-based or fungicide treatments. Ensure good air circulation."
    },
    "Cherry___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Corn___Cercospora_leaf_spot Gray_leaf_spot": {
        "cause": "Fungus Cercospora zeae-maydis.",
        "cure": "Use resistant hybrids and fungicide sprays."
    },
    "Corn___Common_rust": {
        "cause": "Fungus Puccinia sorghi.",
        "cure": "Apply fungicides and plant resistant varieties."
    },
    "Corn___Northern_Leaf_Blight": {
        "cause": "Fungus Exserohilum turcicum.",
        "cure": "Use resistant varieties and fungicides."
    },
    "Corn___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Grape___Black_rot": {
        "cause": "Fungus Guignardia bidwellii.",
        "cure": "Prune infected areas and apply fungicides."
    },
    "Grape___Esca_(Black_Measles)": {
        "cause": "Fungal complex including Phaeomoniella chlamydospora.",
        "cure": "Remove infected wood. Avoid injuries to vines."
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "cause": "Fungus Pseudocercospora vitis.",
        "cure": "Apply fungicides and manage vineyard hygiene."
    },
    "Grape___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "cause": "Bacterium Candidatus Liberibacter spp. Spread by psyllid insects.",
        "cure": "Control psyllid population and remove infected trees."
    },
    "Peach___Bacterial_spot": {
        "cause": "Bacterium Xanthomonas campestris pv. pruni.",
        "cure": "Use resistant varieties and copper-based bactericides."
    },
    "Peach___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacterium Xanthomonas campestris pv. vesicatoria.",
        "cure": "Use copper-based bactericides and resistant varieties."
    },
    "Pepper,_bell___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Potato___Early_blight": {
        "cause": "Fungus Alternaria solani.",
        "cure": "Apply fungicides and practice crop rotation."
    },
    "Potato___Late_blight": {
        "cause": "Pathogen Phytophthora infestans.",
        "cure": "Use resistant varieties and fungicides."
    },
    "Potato___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Raspberry___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Soybean___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Squash___Powdery_mildew": {
        "cause": "Fungal pathogens including Erysiphe cichoracearum.",
        "cure": "Apply sulfur-based fungicides and maintain good air circulation."
    },
    "Strawberry___Leaf_scorch": {
        "cause": "Fungus Diplocarpon earlianum.",
        "cure": "Remove infected leaves and apply fungicides."
    },
    "Strawberry___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Tomato___Bacterial_spot": {
        "cause": "Bacterium Xanthomonas spp.",
        "cure": "Apply copper-based bactericides and practice crop rotation."
    },
    "Tomato___Early_blight": {
        "cause": "Fungus Alternaria solani.",
        "cure": "Apply fungicides and remove infected leaves."
    },
    "Tomato___Late_blight": {
        "cause": "Pathogen Phytophthora infestans.",
        "cure": "Use resistant varieties and fungicides."
    },
    "Tomato___Leaf_Mold": {
        "cause": "Fungus Passalora fulva.",
        "cure": "Apply fungicides and ensure good ventilation."
    },
    "Tomato___Septoria_leaf_spot": {
        "cause": "Fungus Septoria lycopersici.",
        "cure": "Remove infected leaves and apply fungicides."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "cause": "Spider mites Tetranychus urticae.",
        "cure": "Use miticides or insecticidal soaps."
    },
    "Tomato___Target_Spot": {
        "cause": "Fungus Corynespora cassiicola.",
        "cure": "Apply fungicides and ensure good air circulation."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "cause": "Virus spread by whiteflies.",
        "cure": "Control whitefly population and use resistant varieties."
    },
    "Tomato___Tomato_mosaic_virus": {
        "cause": "Virus transmitted through contact and contaminated tools.",
        "cure": "Remove infected plants and sterilize tools."
    },
    "Tomato___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
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
    if (loading) {
      document.title = 'Predicting...';
      animateLoadingText();
    } else {
      document.title = 'Disease Prediction';
    }
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
      if (blob) {
        const previewUrl = URL.createObjectURL(blob);
        setImageUrl(previewUrl);

        const formData = new FormData();
        formData.append('image', blob, 'capture.jpg');

        setLoading(true);

        try {
          const response = await fetch('http://localhost:2000/upload', {
            method: 'POST',
            body: formData,
          });

          const data = await response.json();
          const trimmed = data.prediction?.trim() || '';
          setPrediction(trimmed);
          setHealthyPercentage(data.healthy || '');
          setAffectedPercentage(data.affected || '');
        } catch (error) {
          console.error('Error sending captured image:', error);
        } finally {
          setLoading(false);
        }
      }
    }, 'image/jpeg');
  };

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    stopCamera();
    const previewUrl = URL.createObjectURL(file);
    setImageUrl(previewUrl);
    setLoading(true);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://localhost:2000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      const trimmed = data.prediction?.trim() || '';
      setPrediction(trimmed);
      setHealthyPercentage(data.healthy || '');
      setAffectedPercentage(data.affected || '');
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
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
           <h1 className='h1'>Crops Disease Detection
          </h1>
          <div className='linkk'>
            <ul className="nav-links">
              <li><Link to="/homepage" className="nav-link">Home</Link></li>
              <li><Link to="/prediction" className="nav-link">Disease Detection</Link></li>
              <li><Link to="/about" className="nav-link">About</Link></li>
              <li><Link to="/cropsinfromation" className="nav-link active1">Guide</Link></li>
            </ul>
          </div>
           
        </div>
      </nav>

      <div className="container">
        <h1 id="heading">Upload Image or Click Image</h1>

        <div className="video-container" style={{ display: streaming ? 'block' : 'none' }}>
          <video ref={videoRef} autoPlay playsInline muted />
        </div>

        <div className="controls">
          <button onClick={() => { resetState(); startCamera(); }} disabled={streaming} id="cameraBtn" style={{ display: 'none' }}>
            <i className="fa-solid fa-camera"></i>
          </button>
          <label htmlFor="cameraBtn" className="camera-label"><i className="fa-solid fa-camera"></i></label>

          <input type="file" accept="image/*" id="fileInput" onClick={resetState} onChange={handleImageUpload} style={{ display: 'none' }} />
          <label htmlFor="fileInput" className="uploade-icon"><i className="fa-solid fa-image"></i></label>
        </div>

        {(imageUrl || loading || prediction) && (
          <div className="prediction">
            {imageUrl && (
              <img
                src={imageUrl}
                alt="Uploaded or Captured"
                style={{ width: '200px', height: '200px', marginBottom: '10px', borderRadius: '20px' }}
              />
            )}

            {loading && (
              <div className="loader">
                <h4>Predicting <span className="loding">...............</span></h4>
              </div>
            )}

            {!loading && prediction && (
              <>
                <h5 className="Loader">Prediction: {trimmedPrediction}</h5>
                {healthyPercentage && <h5 className="Loader">Healthy Percentage: {healthyPercentage}%</h5>}
                {affectedPercentage && <h5 className="Loader">Affected Percentage: {affectedPercentage}%</h5>}

                {diseaseInfo[trimmedPrediction] && (
                  <>
                    <h5 className="Loader">Cause: {diseaseInfo[trimmedPrediction].cause}</h5>
                    <h5 className="Loader">Cure: {diseaseInfo[trimmedPrediction].cure}</h5>
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

