// ===============================
// IMPORTS
// ===============================
const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');
const { execFile } = require('child_process');
const os = require('os');

// ===============================
// APP SETUP
// ===============================
const app = express();
const PORT = process.env.PORT || 2000;

// ===============================
// CORS CONFIG
// ===============================
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST']
}));

// ===============================
// STATIC FILES
// ===============================
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// ===============================
// MULTER CONFIG (MEMORY STORAGE)
// ===============================
const storage = multer.memoryStorage();
const upload = multer({ storage });

// ===============================
// PYTHON COMMAND (RENDER SAFE)
// ===============================
const PYTHON_CMD = "python"; // ✅ DO NOT USE python3 on Render

// ===============================
// UPLOAD & PREDICTION ROUTE
// ===============================
app.post('/upload', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  try {
    // Ensure uploads directory exists
    const uploadDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir);
    }

    // Save image
    const fileName = `${Date.now()}-image.jpg`;
    const filePath = path.join(uploadDir, fileName);
    await fs.promises.writeFile(filePath, req.file.buffer);

    console.log('✅ Image saved:', filePath);

    // Python script path
    const pythonScriptPath = path.join(
      __dirname,
      'wheatleaf_disease',
      'predictionscript.py'
    );

    console.log('🐍 Python script:', pythonScriptPath);

    // Execute Python
    execFile(PYTHON_CMD, [pythonScriptPath, filePath], (error, stdout, stderr) => {

      if (error) {
        console.error('❌ Python execution error:', error.message);
        cleanupFile(filePath);
        return res.status(500).json({ error: 'Python execution failed' });
      }

      if (stderr) {
        console.error('⚠️ Python stderr:', stderr);
      }

      try {
        // Extract JSON safely
        const output = stdout.trim();
        const start = output.indexOf('{');
        const end = output.lastIndexOf('}');

        if (start === -1 || end === -1) {
          throw new Error('Invalid JSON from Python');
        }

        const jsonString = output.substring(start, end + 1);
        const result = JSON.parse(jsonString);

        console.log('🎯 Prediction Result:', result);

        res.json({
          prediction: result.prediction,
          healthy: result.healthy,
          affected: result.affected,
          cause: result.cause,
          cure: result.cure
        });

      } catch (err) {
        console.error('❌ JSON parse error:', err.message);
        res.status(500).json({ error: 'Invalid response from Python' });
      } finally {
        cleanupFile(filePath);
      }
    });

  } catch (err) {
    console.error('❌ Server error:', err.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ===============================
// ROOT ROUTE
// ===============================
app.get('/', (req, res) => {
  res.send('🚀 Crop Disease Detection Backend is running');
});

// ===============================
// DELETE TEMP FILE
// ===============================
function cleanupFile(filePath) {
  fs.unlink(filePath, (err) => {
    if (err) {
      console.warn('⚠️ Temp file delete failed:', err.message);
    } else {
      console.log('🗑️ Temp file deleted:', filePath);
    }
  });
}

// ===============================
// START SERVER
// ===============================
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Server running on port ${PORT}`);
});
