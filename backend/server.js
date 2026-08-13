const express = require('express');
const multer = require('multer');
const cors = require('cors');
const { fetch } = require('undici');
const FormData = require('form-data');

const app = express();
const PORT = process.env.PORT || 2000;

/* CORS */
app.use(cors({
  origin: 'https://crops-dieasese-detection-app.vercel.app',
  methods: ['GET', 'POST']
}));

/* Multer */
const upload = multer({
  storage: multer.memoryStorage()
});

/* Python API URL */
const PYTHON_API_URL =
  'https://crops-dieasese-detection-app-5.onrender.com/predict';

/* Upload Route */
app.post('/upload', upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        error: 'No file uploaded'
      });
    }

    console.log('File received:', req.file.originalname);
    console.log('File type:', req.file.mimetype);
    console.log('File size:', req.file.size);

    const form = new FormData();

    form.append('file', req.file.buffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype
    });

    console.log('Sending image to Python API...');

    const response = await fetch(PYTHON_API_URL, {
      method: 'POST',
      body: form,
      headers: form.getHeaders()
    });

    console.log('Python status:', response.status);

    const text = await response.text();

    console.log('Python response:', text);

    if (!response.ok) {
      return res.status(500).json({
        error: 'Python API failed',
        details: text
      });
    }

    const result = JSON.parse(text);

    console.log('Prediction result:', result);

    res.json(result);

  } catch (err) {
    console.error('❌ Upload error:', err);

    res.status(500).json({
      error: 'Prediction failed',
      details: err.message
    });
  }
});

/* Health check */
app.get('/', (req, res) => {
  res.send('🚀 Node backend running');
});

/* Start server */
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Server running on port ${PORT}`);
});