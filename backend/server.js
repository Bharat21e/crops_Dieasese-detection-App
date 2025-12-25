// server.js
const express = require('express');
const multer = require('multer');
const cors = require('cors');
const FormData = require('form-data');
const fetch = require('node-fetch'); // Use node-fetch v2 for CommonJS

const app = express();
const PORT = process.env.PORT || 2000; // Use Render port if available

// CORS configuration
app.use(cors({
  origin: 'https://crops-dieasese-detection-app.vercel.app', // your frontend URL
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type']
}));

// Multer setup for memory storage
const upload = multer({ storage: multer.memoryStorage() });

// Python API URL
const PYTHON_API_URL = 'https://crops-dieasese-detection-app-5.onrender.com/predict';

// Upload endpoint
app.post('/upload', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  try {
    const formData = new FormData();
    formData.append('file', req.file.buffer, {
      filename: 'image.jpg',
      contentType: req.file.mimetype
    });

    const response = await fetch(PYTHON_API_URL, {
      method: 'POST',
      body: formData,
      headers: formData.getHeaders() // important for multipart/form-data
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Python API error: ${response.status} ${text}`);
    }

    const result = await response.json();
    res.json(result);

  } catch (err) {
    console.error('❌ Error:', err.message);
    res.status(500).json({ error: 'Prediction failed', details: err.message });
  }
});

// Health check endpoint
app.get('/', (req, res) => {
  res.send('🚀 Node server is running');
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Node server running on port ${PORT}`);
});
