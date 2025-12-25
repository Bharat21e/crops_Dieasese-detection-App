const express = require('express');
const multer = require('multer');
const cors = require('cors');
const FormData = require('form-data');

const app = express();
const PORT = 2000;

//const cors = require('cors');

app.use(cors({
    origin: 'https://crops-dieasese-detection-app.vercel.app', // frontend URL
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type']
}));


const upload = multer({ storage: multer.memoryStorage() });

const PYTHON_API_URL = 'https://crops-dieasese-detection-app-5.onrender.com/predict';

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
      headers: formData.getHeaders()
    });

    if (!response.ok) throw new Error('Python API error');

    const result = await response.json();
    res.json(result);

  } catch (err) {
    console.error('❌ Error:', err.message);
    res.status(500).json({ error: 'Prediction failed' });
  }
});

app.get('/', (req, res) => {
  res.send('🚀 Node server is running');
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Node server running on port http://localhost:${PORT}`);
});
