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
const PORT = 2000;

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
// PYTHON COMMAND (CROSS PLATFORM)
// ===============================
const PYTHON_CMD = process.platform === "win32" ? "python" : "python3";

// ===============================
// UPLOAD & PREDICTION ROUTE
// ===============================
app.post('/upload', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  try {
    // Create uploads folder if not exists
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

    // Execute Python script
    execFile(PYTHON_CMD, [pythonScriptPath, filePath], (error, stdout, stderr) => {

      if (error) {
        console.error('❌ Python execution error:', error.message);
        cleanupFile(filePath);
        return res.status(500).json({ error: 'Python execution failed' });
      }

      if (stderr) {
        console.warn('⚠️ Python stderr:', stderr);
      }

      try {
        // Extract JSON from Python output
        const output = stdout.trim();
        const start = output.indexOf('{');
        const end = output.lastIndexOf('}');

        if (start === -1 || end === -1) {
          throw new Error('Invalid JSON output');
        }

        const jsonString = output.substring(start, end + 1);
        const result = JSON.parse(jsonString);

        console.log('🎯 Prediction Result:', result);

        // Send response
        res.json({
          prediction: result.prediction,
          healthy: result.healthy,
          affected: result.affected
        });

      } catch (parseError) {
        console.error('❌ JSON parse error:', parseError.message);
        res.status(500).json({ error: 'Invalid response from Python' });
      } finally {
        // Always delete temp file
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
  res.send(`🚀 Server running on http://${getLocalIP()}:${PORT}`);
});

// ===============================
// GET LOCAL IP
// ===============================
function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (let name in interfaces) {
    for (let net of interfaces[name]) {
      if (net.family === 'IPv4' && !net.internal) {
        return net.address;
      }
    }
  }
  return 'localhost';
}

// ===============================
// DELETE TEMP FILE
// ===============================
function cleanupFile(filePath) {
  fs.unlink(filePath, (err) => {
    if (err) {
      console.warn('⚠️ Failed to delete temp file:', err.message);
    } else {
      console.log('🗑️ Temp file deleted:', filePath);
    }
  });
}

// ===============================
// START SERVER
// ===============================
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Server running at http://${getLocalIP()}:${PORT}`);
});
