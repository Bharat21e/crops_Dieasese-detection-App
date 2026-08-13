const express = require('express');
const multer = require('multer');
const cors = require('cors');

const app = express();

const PORT = process.env.PORT || 2000;


/* =========================
   CORS
========================= */

app.use(cors({
  origin: 'https://crops-dieasese-detection-app.vercel.app',
  methods: ['GET', 'POST']
}));


/* =========================
   MULTER
========================= */

const upload = multer({
  storage: multer.memoryStorage()
});


/* =========================
   PYTHON API
========================= */

const PYTHON_API_URL =
  'https://crops-dieasese-detection-app-5.onrender.com/predict';


/* =========================
   UPLOAD ROUTE
========================= */

app.post('/upload', upload.single('image'), async (req, res) => {

  try {

    /* Check file */

    if (!req.file) {

      return res.status(400).json({
        error: 'No file uploaded'
      });

    }


    console.log(
      'File received:',
      req.file.originalname
    );

    console.log(
      'File type:',
      req.file.mimetype
    );

    console.log(
      'File size:',
      req.file.size
    );


    /* =========================
       CREATE NATIVE FORMDATA
    ========================= */

    const form = new FormData();


    /* Buffer -> Blob */

    const blob = new Blob(
      [req.file.buffer],
      {
        type: req.file.mimetype
      }
    );


    /* IMPORTANT
       Python expects "file"
    */

    form.append(
      'file',
      blob,
      req.file.originalname
    );


    console.log(
      'Sending image to Python API...'
    );


    /* =========================
       SEND TO PYTHON
    ========================= */

    const response = await fetch(
      PYTHON_API_URL,
      {
        method: 'POST',
        body: form
      }
    );


    console.log(
      'Python status:',
      response.status
    );


    /* Get response */

    const text = await response.text();


    console.log(
      'Python response:',
      text
    );


    /* =========================
       PYTHON ERROR
    ========================= */

    if (!response.ok) {

      return res.status(response.status).json({
        error: 'Python API failed',
        details: text
      });

    }


    /* =========================
       CONVERT JSON
    ========================= */

    const result = JSON.parse(text);


    console.log(
      'Prediction result:',
      result
    );


    return res.json(result);

  }


  catch (err) {

    console.error(
      '❌ Upload error:',
      err
    );


    return res.status(500).json({
      error: 'Prediction failed',
      details: err.message
    });

  }

});


/* =========================
   HEALTH CHECK
========================= */

app.get('/', (req, res) => {

  res.send(
    '🚀 Node backend running'
  );

});


/* =========================
   START SERVER
========================= */

app.listen(
  PORT,
  '0.0.0.0',
  () => {

    console.log(
      `✅ Server running on port ${PORT}`
    );

  }
);