


from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import tensorflow as tf
import io
import os

app = FastAPI()


# =========================================================
# HOME / HEALTH CHECK
# =========================================================

@app.get("/")
def root():
    return {
        "status": "Crop Disease Detection API is running"
    }


@app.head("/")
def root_head():
    return


# =========================================================
# CLASS NAMES
# IMPORTANT:
# This order MUST match your training class_indices
# =========================================================

class_names = [
    "Apple___Apple_scab",                         # 0
    "Apple___Black_rot",                          # 1
    "Apple___Cedar_apple_rust",                   # 2
    "Apple___healthy",                             # 3
    "Cherry___Powdery_mildew",                    # 4
    "Cherry___healthy",                           # 5
    "Corn___Cercospora_leaf_spot Gray_leaf_spot", # 6
    "Corn___Common_rust",                         # 7
    "Corn___Northern_Leaf_Blight",                # 8
    "Corn___healthy",                              # 9
    "Grape___Black_rot",                           # 10
    "Grape___Esca_(Black_Measles)",               # 11
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", # 12
    "Grape___healthy",                             # 13
    "Healthy",                                     # 14
    "Non_Leaf",                                    # 15
    "Orange___Haunglongbing_(Citrus_greening)",   # 16
    "Peach___Bacterial_spot",                     # 17
    "Peach___healthy",                             # 18
    "Pepper,_bell___Bacterial_spot",              # 19
    "Pepper,_bell___healthy",                     # 20
    "Potato___Early_blight",                      # 21
    "Potato___Late_blight",                       # 22
    "Potato___healthy",                            # 23
    "Raspberry___healthy",                         # 24
    "Soybean___healthy",                           # 25
    "Squash___Powdery_mildew",                    # 26
    "Strawberry___Leaf_scorch",                   # 27
    "Strawberry___healthy",                       # 28
    "Tomato___Bacterial_spot",                    # 29
    "Tomato___Early_blight",                      # 30
    "Tomato___Late_blight",                       # 31
    "Tomato___Leaf_Mold",                         # 32
    "Tomato___Septoria_leaf_spot",                # 33
    "Tomato___Spider_mites Two-spotted_spider_mite", # 34
    "Tomato___Target_Spot",                       # 35
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",     # 36
    "Tomato___Tomato_mosaic_virus",               # 37
    "Tomato___healthy",                            # 38
    "septoria",                                    # 39
    "stripe_rust"                                  # 40
]


# =========================================================
# DISEASE INFORMATION
# =========================================================

disease_data = {

    # -------------------------
    # Apple
    # -------------------------

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


    # -------------------------
    # Cherry
    # -------------------------

    "Cherry___Powdery_mildew": {
        "cause": "Fungal infection favored by humid conditions.",
        "cure": "Improve air circulation and use an appropriate fungicide."
    },

    "Cherry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue standard crop management."
    },


    # -------------------------
    # Corn
    # -------------------------

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


    # -------------------------
    # Grape
    # -------------------------

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


    # -------------------------
    # Orange
    # -------------------------

    "Orange___Haunglongbing_(Citrus_greening)": {
        "cause": "Citrus greening is a bacterial disease spread by psyllids.",
        "cure": "Control psyllids and remove severely infected trees."
    },


    # -------------------------
    # Peach
    # -------------------------

    "Peach___Bacterial_spot": {
        "cause": "Bacterial infection affecting leaves and fruits.",
        "cure": "Use resistant varieties and appropriate copper-based treatment."
    },

    "Peach___healthy": {
        "cause": "No disease detected.",
        "cure": "Maintain good orchard hygiene and crop care."
    },


    # -------------------------
    # Pepper
    # -------------------------

    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacterial infection favored by warm and wet conditions.",
        "cure": "Use disease-free seeds and appropriate crop protection."
    },

    "Pepper,_bell___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue proper crop care."
    },


    # -------------------------
    # Potato
    # -------------------------

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


    # -------------------------
    # Raspberry
    # -------------------------

    "Raspberry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue normal crop management."
    },


    # -------------------------
    # Soybean
    # -------------------------

    "Soybean___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue normal crop management."
    },


    # -------------------------
    # Squash
    # -------------------------

    "Squash___Powdery_mildew": {
        "cause": "Fungal infection causing white powdery growth.",
        "cure": "Improve air circulation and use appropriate fungicide."
    },


    # -------------------------
    # Strawberry
    # -------------------------

    "Strawberry___Leaf_scorch": {
        "cause": "Fungal infection causing leaf damage.",
        "cure": "Remove infected leaves and improve drainage."
    },

    "Strawberry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue regular crop management."
    },


    # -------------------------
    # Tomato
    # -------------------------

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


    # -------------------------
    # Other / Wheat Classes
    # -------------------------

    "Healthy": {
        "cause": "No disease detected.",
        "cure": "Continue proper crop care."
    },

    "Non_Leaf": {
        "cause": "The uploaded image does not appear to contain a recognizable crop leaf.",
        "cure": "Please upload a clear image of a crop leaf."
    },

    "septoria": {
        "cause": "Fungal leaf disease caused by Septoria.",
        "cure": "Remove infected leaves, maintain good field hygiene and use an appropriate fungicide when required."
    },

    "stripe_rust": {
        "cause": "Fungal rust disease affecting the leaf.",
        "cure": "Use resistant varieties and apply an appropriate fungicide when required."
    }
}


# =========================================================
# LOAD MODEL
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "crop_leaf_model.h5"
)

print("Loading model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully")
print("Model output shape:", model.output_shape)
print("Number of classes:", len(class_names))


# =========================================================
# MODEL / CLASS SAFETY CHECK
# =========================================================

try:
    model_class_count = model.output_shape[-1]

    if model_class_count != len(class_names):
        raise ValueError(
            f"Model has {model_class_count} output classes, "
            f"but class_names contains {len(class_names)} classes."
        )

    print("Class count check: OK")

except Exception as e:
    print("Class count check failed:", str(e))


# =========================================================
# IMAGE QUALITY CHECK
# =========================================================

def check_image_quality(image):
    """
    Basic check for very small, too dark, too bright,
    or very low-contrast/blurry images.
    """
    width, height = image.size

    if width < 100 or height < 100:
        return False

    gray = image.convert("L")
    pixels = np.array(gray, dtype=np.float32)

    brightness = np.mean(pixels)
    contrast = np.std(pixels)

    # Reject extremely dark, extremely bright,
    # or very low-contrast images.
    if brightness < 30 or brightness > 245:
        return False

    if contrast < 15:
        return False

    return True


UPLOAD_MESSAGE = (
    "Please upload a clear crop leaf image with good lighting "
    "and keep the leaf fully visible."
)


# =========================================================
# PREDICTION
# =========================================================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    try:

        # -------------------------
        # Read uploaded image
        # -------------------------

        image_bytes = await file.read()

        if not image_bytes:
            return {
                "error": "Uploaded file is empty."
            }

        # -------------------------
        # Open image
        # -------------------------

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        # -------------------------
        # Check image quality
        # -------------------------

        if not check_image_quality(image):
            return {
                "prediction": "Non_Leaf",
                "confidence": 0,
                "healthy": 0,
                "affected": 0,
                "cause": "The uploaded image is unclear or does not contain a recognizable crop leaf.",
                "cure": "Please upload a clear image of a crop leaf.",
                "message": UPLOAD_MESSAGE
            }

        # -------------------------
        # Resize
        # -------------------------

        image = image.resize((150, 150))

        # -------------------------
        # Convert to NumPy
        # -------------------------

        image_array = np.array(
            image,
            dtype=np.float32
        )

        # -------------------------
        # Normalize
        # -------------------------

        image_array = image_array / 255.0

        # -------------------------
        # Add batch dimension
        # -------------------------

        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # -------------------------
        # Prediction
        # -------------------------

        predictions = model.predict(
            image_array,
            verbose=0
        )[0]

        # -------------------------
        # Check model output
        # -------------------------

        if len(predictions) != len(class_names):
            return {
                "error": (
                    f"Model returned {len(predictions)} classes, "
                    f"but API has {len(class_names)} class names."
                )
            }

        # -------------------------
        # Highest probability
        # -------------------------

        index = int(
            np.argmax(predictions)
        )

        # -------------------------
        # Predicted label
        # -------------------------

        label = class_names[index]

        # -------------------------
        # Confidence
        # -------------------------

        confidence = float(
            predictions[index]
        ) * 100

        confidence = round(
            confidence,
            2
        )

        # -------------------------
        # NON-LEAF CHECK
        # -------------------------

        if label == "Non_Leaf":
            return {
                "prediction": "Non_Leaf",
                "confidence": confidence,
                "healthy": 0,
                "affected": 0,
                "cause": "The uploaded image does not appear to contain a recognizable crop leaf.",
                "cure": "Please upload a clear image of a crop leaf.",
                "message": UPLOAD_MESSAGE
                
            }

        # -------------------------
        # Disease information
        # -------------------------

        info = disease_data.get(label)

        if info:

            cause = info["cause"]
            cure = info["cure"]

        else:

            cause = "Disease information not available."
            cure = "Please consult an agriculture expert."

        # -------------------------
        # Healthy / affected
        # -------------------------

        is_healthy = (
            label.lower() == "healthy"
            or "healthy" in label.lower()
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

        # -------------------------
        # Final response
        # -------------------------

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
