const express = require('express');
const multer = require('multer');
const cors = require('cors');
const FormData = require('form-data');

const app = express();
const PORT = process.env.PORT || 2000;

const fetch = (...args) =>
  import('node-fetch').then(({ default: fetch }) => fetch(...args));

/* ✅ CORS */
app.use(cors({
  origin: 'https://crops-dieasese-detection-app.vercel.app',
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type']
}));

/* ✅ Multer */
const upload = multer({ storage: multer.memoryStorage() });

/* ✅ Python ML API */
const PYTHON_API_URL = 'https://crops-dieasese-detection-app-5.onrender.com/predict';

/* ✅ Upload Route */
app.post('/upload', upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const formData = new FormData();
    formData.append('file', req.file.buffer, {
      filename: 'image.jpg',
      contentType: req.file.mimetype
    });

    const response = await fetch(PYTHON_API_URL, {
      method: 'POST',
      body: formData,
      headers: formData.getHeaders()
    });

    if (!response.ok) {
      const text = await response.text();
      console.error('Python API error:', text);
      return res.status(500).json({ error: 'Python API failed' });
    }

    const result = await response.json();
    res.json(result);

  } catch (error) {
    console.error('❌ Upload error:', error);
    res.status(500).json({ error: 'Prediction failed' });
  }
});

/* ✅ Health Check */
app.get('/', (req, res) => {
  res.send('🚀 Node backend running successfully');
});

/* ✅ Start Server */
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Server running on port ${PORT}`);
});
