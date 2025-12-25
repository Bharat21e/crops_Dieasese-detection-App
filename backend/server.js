const express = require('express');
const multer = require('multer');
const cors = require('cors');
const { fetch, FormData, Blob } = require('undici');

const app = express();
const PORT = process.env.PORT || 2000;

/* ✅ CORS */
app.use(cors({
  origin: 'https://crops-dieasese-detection-app.vercel.app',
  methods: ['GET', 'POST']
}));

/* ✅ Multer */
const upload = multer({ storage: multer.memoryStorage() });

/* ✅ Python API URL */
const PYTHON_API_URL =
  'https://crops-dieasese-detection-app-5.onrender.com/predict';

/* ✅ Upload Route */
app.post('/upload', upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const form = new FormData();
    const blob = new Blob([req.file.buffer], {
      type: req.file.mimetype
    });

    form.append('file', blob, 'image.jpg');

    const response = await fetch(PYTHON_API_URL, {
      method: 'POST',
      body: form
      // ❌ DO NOT SET HEADERS
    });

    if (!response.ok) {
      const text = await response.text();
      console.error('Python API Error:', text);
      return res.status(500).json({ error: 'Python API failed' });
    }

    const result = await response.json();
    res.json(result);

  } catch (err) {
    console.error('❌ Upload error:', err);
    res.status(500).json({ error: 'Prediction failed' });
  }
});

/* ✅ Health check */
app.get('/', (req, res) => {
  res.send('🚀 Node backend running');
});

/* ✅ Start server */
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Server running on port ${PORT}`);
});
