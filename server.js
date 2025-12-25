const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fetch = require('node-fetch');
const FormData = require('form-data');

const app = express();
const PORT = 2000;

app.use(cors({ origin: "http://localhost:3000" }));

const upload = multer({ storage: multer.memoryStorage() });

const PYTHON_API_URL = "http://127.0.0.1:8000/predict";

app.post('/upload', upload.single('image'), async (req, res) => {
  try {
    const formData = new FormData();
    formData.append("file", req.file.buffer, "image.jpg");

    const response = await fetch(PYTHON_API_URL, {
      method: "POST",
      body: formData,
      headers: formData.getHeaders()
    });

    const result = await response.json();
    res.json(result);

  } catch (err) {
    res.status(500).json({ error: "Prediction failed" });
  }
});

app.get('/', (req, res) => {
  res.send("🚀 Node server running");
});

app.listen(PORT, () => {
  console.log(`✅ Node server: http://localhost:${PORT}`);
});
