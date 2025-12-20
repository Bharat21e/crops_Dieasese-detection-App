from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import tensorflow as tf
import io

app = FastAPI()

class_names = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry___Powdery_mildew", "Cherry___healthy",
    "Corn___Cercospora_leaf_spot Gray_leaf_spot", "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight", "Corn___healthy",
    "Grape___Black_rot", "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot",
    "Peach___healthy", "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy", "Potato___Early_blight",
    "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy",
    "Soybean___healthy", "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight",
    "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus", "Tomato___healthy",  "Healthy", "Brown_Rust", "Yellow_Rust"
]

sease_data = {
    "Healthy": {"cause": "No disease present.", "cure": "Maintain good cultural practices."},
    "Brown_Rust": {"cause": "Brown rust present.", "cure": "No update available."},
    "Yellow_Rust": {"cause": "Yellow rust present.", "cure": "No update available."}
    # ... add all other crop disease data from your original code ...
}

model = tf.keras.models.load_model("crop_leaf_model.h5")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((150, 150))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array)[0]
        index = int(np.argmax(predictions))
        label = class_names[index]

        healthy = round(float(predictions[index]) * 100, 2)
        affected = round(100 - healthy, 2)

        info = sease_data.get(label, {
            "cause": "Disease information not available.",
            "cure": "Check nearby agriculture doctor."
        })

        return {
            "prediction": label,
            "healthy": healthy,
            "affected": affected,
            "cause": info["cause"],
            "cure": info["cure"]
        }
    except Exception as e:
        return {"error": str(e)}
