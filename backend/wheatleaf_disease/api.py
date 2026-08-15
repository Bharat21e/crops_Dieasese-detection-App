from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import tensorflow as tf
import io
import os

app = FastAPI()


# =========================
# HOME / HEALTH CHECK
# =========================

@app.get("/")
def root():
    return {
        "status": "Crop Disease Detection API is running"
    }


@app.head("/")
def root_head():
    return


# =========================
# CLASS NAMES
# =========================

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


# =========================
# DISEASE INFORMATION
# =========================

disease_data = {

    # Apple
    "Apple___Apple_scab": {
        "cause": "Fungal infection caused by Venturia inaequalis.",
        "cure": "Remove infected leaves and apply recommended fungicide."
    },

    "Apple___Black_rot": {
        "cause": "Fungal disease caused by Botryosphaeria obtusa.",
        "cure": "Prune infected branches and use recommended fungicides."
    },

    "Apple___Cedar_apple_rust": {
        "cause": "Fungal disease associated with cedar trees.",
        "cure": "Remove infected plant material and apply appropriate fungicide."
    },

    "Apple___healthy": {
        "cause": "No disease detected.",
        "cure": "Maintain proper irrigation, nutrition and crop care."
    },


    # Blueberry
    "Blueberry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue normal crop management."
    },


    # Cherry
    "Cherry___Powdery_mildew": {
        "cause": "Fungal infection favored by humid conditions.",
        "cure": "Improve air circulation and use an appropriate fungicide."
    },

    "Cherry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue standard crop management."
    },


    # Corn
    "Corn___Cercospora_leaf_spot Gray_leaf_spot": {
        "cause": "Fungal infection caused by Cercospora species.",
        "cure": "Use resistant hybrids, crop rotation and appropriate fungicide."
    },

    "Corn___Common_rust": {
        "cause": "Rust fungal infection favored by moist weather.",
        "cure": "Use resistant varieties and apply fungicide when required."
    },

    "Corn___Northern_Leaf_Blight": {
        "cause": "Fungal disease caused by Exserohilum turcicum.",
        "cure": "Use crop rotation, resistant varieties and fungicide."
    },

    "Corn___healthy": {
        "cause": "No disease detected.",
        "cure": "Maintain balanced fertilization and proper irrigation."
    },


    # Grape
    "Grape___Black_rot": {
        "cause": "Fungal infection affecting leaves and fruit.",
        "cure": "Remove infected plant parts and apply appropriate fungicide."
    },

    "Grape___Esca_(Black_Measles)": {
        "cause": "Fungal disease affecting grape vines.",
        "cure": "Prune affected vines and avoid unnecessary plant injuries."
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "cause": "Fungal leaf spot disease.",
        "cure": "Remove affected leaves and use protective fungicide."
    },

    "Grape___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue good vineyard management."
    },


    # Orange
    "Orange___Haunglongbing_(Citrus_greening)": {
        "cause": "Citrus greening is a bacterial disease spread by psyllids.",
        "cure": "Control psyllids and remove severely infected trees."
    },


    # Peach
    "Peach___Bacterial_spot": {
        "cause": "Bacterial infection affecting leaves and fruits.",
        "cure": "Use resistant varieties and appropriate copper-based treatment."
    },

    "Peach___healthy": {
        "cause": "No disease detected.",
        "cure": "Maintain good orchard hygiene and crop care."
    },


    # Pepper
    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacterial infection favored by warm and wet conditions.",
        "cure": "Use disease-free seeds and appropriate crop protection."
    },

    "Pepper,_bell___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue proper crop care."
    },


    # Potato
    "Potato___Early_blight": {
        "cause": "Fungal disease caused by Alternaria species.",
        "cure": "Use crop rotation and appropriate fungicide."
    },

    "Potato___Late_blight": {
        "cause": "Disease caused by Phytophthora infestans.",
        "cure": "Remove severely infected material and apply appropriate fungicide."
    },

    "Potato___healthy": {
        "cause": "No disease detected.",
        "cure": "Maintain proper soil fertility and irrigation."
    },


    # Raspberry
    "Raspberry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue normal crop management."
    },


    # Soybean
    "Soybean___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue normal crop management."
    },


    # Squash
    "Squash___Powdery_mildew": {
        "cause": "Fungal infection causing white powdery growth.",
        "cure": "Improve air circulation and use appropriate fungicide."
    },


    # Strawberry
    "Strawberry___Leaf_scorch": {
        "cause": "Fungal infection causing leaf damage.",
        "cure": "Remove infected leaves and improve drainage."
    },

    "Strawberry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue regular crop management."
    },


    # Tomato
    "Tomato___Bacterial_spot": {
        "cause": "Bacterial infection favored by wet conditions.",
        "cure": "Use resistant varieties and appropriate crop protection."
    },

    "Tomato___Early_blight": {
        "cause": "Fungal infection caused by Alternaria species.",
        "cure": "Use crop rotation and appropriate fungicide."
    },

    "Tomato___Late_blight": {
        "cause": "Serious disease caused by Phytophthora infestans.",
        "cure": "Remove severely infected plants and use appropriate fungicide."
    },

    "Tomato___Leaf_Mold": {
        "cause": "Fungal infection favored by high humidity.",
        "cure": "Reduce humidity and improve air circulation."
    },

    "Tomato___Septoria_leaf_spot": {
        "cause": "Fungal leaf spot disease.",
        "cure": "Remove infected leaves and use appropriate fungicide."
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "cause": "Spider mite infestation.",
        "cure": "Use appropriate mite control methods."
    },

    "Tomato___Target_Spot": {
        "cause": "Fungal disease affecting tomato leaves.",
        "cure": "Use resistant varieties and appropriate fungicide."
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "cause": "Viral disease commonly spread by whiteflies.",
        "cure": "Control whiteflies and remove severely infected plants."
    },

    "Tomato___Tomato_mosaic_virus": {
        "cause": "Viral infection.",
        "cure": "Remove infected plants and disinfect tools."
    },

    "Tomato___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue standard crop management."
    },


    # Wheat
    "wheat_Healthy": {
        "cause": "Healthy wheat crop.",
        "cure": "No treatment required."
    },

    "wheat_septoria": {
        "cause": "Fungal leaf disease caused by Septoria.",
        "cure": "Use crop rotation and appropriate fungicide."
    },

    "wheat_stripe_rust": {
        "cause": "Fungal rust disease.",
        "cure": "Use resistant varieties and apply appropriate fungicide when required."
    }
}


# =========================
# LOAD MODEL
# =========================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "crop_leaf_model.h5"
)

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully")
print("Number of classes:", len(class_names))


# =========================
# PREDICTION
# =========================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    try:

        # Read image
        image_bytes = await file.read()

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        # Resize
        image = image.resize((150, 150))

        # Convert to numpy
        image_array = np.array(image, dtype=np.float32)

        # Normalize
        image_array = image_array / 255.0

        # Add batch dimension
        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # Model prediction
        predictions = model.predict(
            image_array,
            verbose=0
        )[0]

        # Find highest probability
        index = int(np.argmax(predictions))

        # Safety check
        if index >= len(class_names):
            return {
                "error": "Model output classes do not match class_names."
            }

        # Predicted label
        label = class_names[index]

        # Confidence
        confidence = float(predictions[index]) * 100

        confidence = round(
            confidence,
            2
        )

        # Get disease information
        info = disease_data.get(label)

        # If information exists
        if info:

            cause = info["cause"]
            cure = info["cure"]

        else:

            cause = "Disease information not available."
            cure = "Please consult an agriculture expert."

        # Check healthy class
        is_healthy = (
            "healthy" in label.lower()
        )

        if is_healthy:

            healthy_percentage = confidence
            affected_percentage = round(
                100 - confidence,
                2
            )

        else:

            affected_percentage = confidence
            healthy_percentage = round(
                100 - confidence,
                2
            )

        # Final response
        return {
            "prediction": label,
            "confidence": confidence,
            "healthy": healthy_percentage,
            "affected": affected_percentage,
            "cause": cause,
            "cure": cure
        }

    except Exception as e:

        return {
            "error": str(e)
        }