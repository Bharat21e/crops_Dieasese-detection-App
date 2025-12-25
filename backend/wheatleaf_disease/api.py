from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import tensorflow as tf
import io
import os

app = FastAPI()


@app.get("/")
def root():
    return {"status": "Crop Disease Detection API is running"}

class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",

    "Blueberry___healthy",

    "Cherry___Powdery_mildew",
    "Cherry___healthy",

    "Corn___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",

    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",

    "Orange___Haunglongbing_(Citrus_greening)",

    "Peach___Bacterial_spot",
    "Peach___healthy",

    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",

    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",

    "Raspberry___healthy",

    "Soybean___healthy",

    "Squash___Powdery_mildew",

    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",

    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",

    "wheat_Healthy",
    "wheat_septoria",
    "wheat_stripe_rust"
]


sease_data = {

    # 🍎 Apple
    "Apple___Apple_scab": {
        "cause": "Fungal infection caused by Venturia inaequalis.",
        "cure": "Remove infected leaves and apply fungicide spray."
    },
    "Apple___Black_rot": {
        "cause": "Fungal disease caused by Botryosphaeria obtusa.",
        "cure": "Prune infected branches and use recommended fungicides."
    },
    "Apple___Cedar_apple_rust": {
        "cause": "Fungal disease spread from cedar trees.",
        "cure": "Remove nearby cedar trees and apply fungicide."
    },
    "Apple___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain proper irrigation and nutrition."
    },

    # 🍒 Cherry
    "Cherry___Powdery_mildew": {
        "cause": "Fungal infection due to humid conditions.",
        "cure": "Improve air circulation and apply sulfur fungicide."
    },
    "Cherry___healthy": {
        "cause": "No disease present.",
        "cure": "Continue standard crop management."
    },

    # 🌽 Corn
    "Corn___Cercospora_leaf_spot Gray_leaf_spot": {
        "cause": "Fungal infection due to Cercospora species.",
        "cure": "Use resistant hybrids and crop rotation."
    },
    "Corn___Common_rust": {
        "cause": "Rust fungus infection favored by moist weather.",
        "cure": "Apply fungicide and use resistant varieties."
    },
    "Corn___Northern_Leaf_Blight": {
        "cause": "Fungal disease caused by Exserohilum turcicum.",
        "cure": "Crop rotation and fungicide spray."
    },
    "Corn___healthy": {
        "cause": "No disease detected.",
        "cure": "Maintain balanced fertilization."
    },

    # 🍇 Grape
    "Grape___Black_rot": {
        "cause": "Fungal infection affecting leaves and fruit.",
        "cure": "Remove infected plant parts and apply fungicide."
    },
    "Grape___Esca_(Black_Measles)": {
        "cause": "Fungal trunk disease.",
        "cure": "Prune affected vines and avoid injuries."
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "cause": "Fungal leaf spot disease.",
        "cure": "Use protective fungicides."
    },
    "Grape___healthy": {
        "cause": "Healthy plant.",
        "cure": "Continue good vineyard practices."
    },

    # 🍊 Orange
    "Orange___Haunglongbing_(Citrus_greening)": {
        "cause": "Bacterial disease spread by psyllids.",
        "cure": "Control insects and remove infected trees."
    },

    # 🍑 Peach
    "Peach___Bacterial_spot": {
        "cause": "Bacterial infection affecting leaves and fruits.",
        "cure": "Use resistant varieties and copper sprays."
    },
    "Peach___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain orchard hygiene."
    },

    # 🌶 Pepper
    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacterial infection in warm, wet conditions.",
        "cure": "Use disease-free seeds and copper fungicide."
    },
    "Pepper,_bell___healthy": {
        "cause": "Healthy crop.",
        "cure": "Continue proper crop care."
    },

    # 🥔 Potato
    "Potato___Early_blight": {
        "cause": "Fungal disease caused by Alternaria.",
        "cure": "Crop rotation and fungicide application."
    },
    "Potato___Late_blight": {
        "cause": "Fungal disease caused by Phytophthora infestans.",
        "cure": "Immediate fungicide spray required."
    },
    "Potato___healthy": {
        "cause": "No disease detected.",
        "cure": "Maintain soil fertility."
    },

    # 🍓 Strawberry
    "Strawberry___Leaf_scorch": {
        "cause": "Fungal infection causing leaf damage.",
        "cure": "Remove infected leaves and improve drainage."
    },
    "Strawberry___healthy": {
        "cause": "Healthy plant.",
        "cure": "Follow regular crop practices."
    },

    # 🍅 Tomato
    "Tomato___Bacterial_spot": {
        "cause": "Bacterial infection due to wet conditions.",
        "cure": "Use resistant varieties and copper spray."
    },
    "Tomato___Early_blight": {
        "cause": "Fungal infection due to Alternaria.",
        "cure": "Crop rotation and fungicide spray."
    },
    "Tomato___Late_blight": {
        "cause": "Severe fungal disease.",
        "cure": "Destroy infected plants and apply fungicide."
    },
    "Tomato___Leaf_Mold": {
        "cause": "Fungal infection in high humidity.",
        "cure": "Reduce humidity and apply fungicide."
    },
    "Tomato___Septoria_leaf_spot": {
        "cause": "Fungal leaf spot disease.",
        "cure": "Remove infected leaves and spray fungicide."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "cause": "Mite infestation.",
        "cure": "Use neem oil or approved insecticides."
    },
    "Tomato___Target_Spot": {
        "cause": "Fungal disease.",
        "cure": "Use resistant varieties and fungicide."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "cause": "Virus spread by whiteflies.",
        "cure": "Control whiteflies and remove infected plants."
    },
    "Tomato___Tomato_mosaic_virus": {
        "cause": "Viral infection.",
        "cure": "Remove infected plants and disinfect tools."
    },
    "Tomato___healthy": {
        "cause": "Healthy crop.",
        "cure": "Continue standard practices."
    },

    # 🌾 Wheat
    "wheat_Healthy": {
        "cause": "Healthy wheat crop.",
        "cure": "No treatment required."
    },
    "wheat_septoria": {
        "cause": "Fungal leaf disease caused by Septoria.",
        "cure": "Apply fungicide and crop rotation."
    },
    "wheat_stripe_rust": {
        "cause": "Fungal rust disease.",
        "cure": "Early sowing and fungicide application."
    }
}


MODEL_PATH = os.path.join(os.path.dirname(__file__), "crop_leaf_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

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
