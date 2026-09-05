
import sys
import json
import os

from PIL import Image, ImageStat
import numpy as np
import tensorflow as tf


# =========================================================
# SETTINGS
# =========================================================

IMG_HEIGHT = 150
IMG_WIDTH = 150

# Minimum confidence required for a valid prediction.
# If confidence is lower, image is treated as Non_Leaf/Unknown.
CONFIDENCE_THRESHOLD = 0.60

# Difference between first and second prediction.
# Small difference means model is uncertain.
MARGIN_THRESHOLD = 0.10


# =========================================================
# CLASS NAMES
# IMPORTANT:
# This order MUST exactly match model training class_indices.
# =========================================================

class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",

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

    "Healthy",
    "Non_Leaf",

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

    "septoria",
    "stripe_rust"
]


# =========================================================
# DISEASE INFORMATION
# =========================================================

disease_data = {

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

    "Cherry___Powdery_mildew": {
        "cause": "Fungal infection favored by humid conditions.",
        "cure": "Improve air circulation and use an appropriate fungicide."
    },

    "Cherry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue standard crop management."
    },

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
        "cure": "Use crop rotation, resistant varieties and appropriate fungicide."
    },

    "Corn___healthy": {
        "cause": "No disease detected.",
        "cure": "Maintain balanced fertilization and proper irrigation."
    },

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

    "Orange___Haunglongbing_(Citrus_greening)": {
        "cause": "Citrus greening is a bacterial disease spread by psyllids.",
        "cure": "Control psyllids and remove severely infected trees."
    },

    "Peach___Bacterial_spot": {
        "cause": "Bacterial infection affecting leaves and fruits.",
        "cure": "Use resistant varieties and appropriate copper-based treatment."
    },

    "Peach___healthy": {
        "cause": "No disease detected.",
        "cure": "Maintain good orchard hygiene and crop care."
    },

    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacterial infection favored by warm and wet conditions.",
        "cure": "Use disease-free seeds and appropriate crop protection."
    },

    "Pepper,_bell___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue proper crop care."
    },

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

    "Raspberry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue normal crop management."
    },

    "Soybean___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue normal crop management."
    },

    "Squash___Powdery_mildew": {
        "cause": "Fungal infection causing white powdery growth.",
        "cure": "Improve air circulation and use appropriate fungicide."
    },

    "Strawberry___Leaf_scorch": {
        "cause": "Fungal infection causing leaf damage.",
        "cure": "Remove infected leaves and improve drainage."
    },

    "Strawberry___healthy": {
        "cause": "No disease detected.",
        "cure": "Continue regular crop management."
    },

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
        "cure": "Remove infected leaves, maintain good field hygiene and use appropriate fungicide when required."
    },

    "stripe_rust": {
        "cause": "Fungal rust disease affecting the leaf.",
        "cure": "Use resistant varieties and apply appropriate fungicide when required."
    }
}


# =========================================================
# LOAD MODEL
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "wheatleaf_disease",
    "crop_leaf_model.h5"
)

# If model is directly beside prediction.py,
# use this instead:
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(
        BASE_DIR,
        "crop_leaf_model.h5"
    )


try:
    print("Loading model...", file=sys.stderr)

    model = tf.keras.models.load_model(MODEL_PATH)

    print(
        f"Model loaded successfully: {MODEL_PATH}",
        file=sys.stderr
    )

except Exception as e:

    print(
        json.dumps({
            "error": f"Failed to load model: {str(e)}"
        })
    )

    sys.exit(1)


# =========================================================
# MODEL SAFETY CHECK
# =========================================================

model_class_count = model.output_shape[-1]

if model_class_count != len(class_names):

    print(
        json.dumps({
            "error": (
                f"Model has {model_class_count} output classes, "
                f"but class_names contains {len(class_names)}."
            )
        })
    )

    sys.exit(1)


# =========================================================
# IMAGE QUALITY CHECK
# =========================================================

def check_image_quality(image):

    width, height = image.size

    # Too small
    if width < 100 or height < 100:
        return False

    gray = image.convert("L")

    pixels = np.asarray(
        gray,
        dtype=np.float32
    )

    brightness = np.mean(pixels)
    contrast = np.std(pixels)

    # Very dark
    if brightness < 25:
        return False

    # Very bright
    if brightness > 245:
        return False

    # Almost no visual information
    if contrast < 12:
        return False

    return True


# =========================================================
# NON-LEAF RESPONSE
# =========================================================

def non_leaf_response(confidence=0):

    return {
        "prediction": "Non_Leaf",
        "confidence": round(float(confidence), 2),
        "healthy": 0,
        "affected": 0,
        "cause": (
            "The uploaded image does not appear to contain "
            "a recognizable crop leaf."
        ),
        "cure": (
            "Please upload a clear image of a crop leaf "
            "with good lighting."
        ),
        "message": (
            "Please upload a clear crop leaf image."
        )
    }


# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_leaf_disease(image_path):

    try:

        # ---------------------------------------------
        # Open image
        # ---------------------------------------------

        image = Image.open(
            image_path
        ).convert("RGB")


        # ---------------------------------------------
        # Basic image quality check
        # ---------------------------------------------

        if not check_image_quality(image):

            return json.dumps(
                non_leaf_response()
            )


        # ---------------------------------------------
        # Resize
        # ---------------------------------------------

        image = image.resize(
            (IMG_WIDTH, IMG_HEIGHT)
        )


        # ---------------------------------------------
        # Convert to numpy
        # ---------------------------------------------

        image_array = np.asarray(
            image,
            dtype=np.float32
        )


        # ---------------------------------------------
        # Normalize
        # ---------------------------------------------

        image_array /= 255.0


        # ---------------------------------------------
        # Add batch dimension
        # ---------------------------------------------

        image_array = np.expand_dims(
            image_array,
            axis=0
        )


        # ---------------------------------------------
        # Model prediction
        # ---------------------------------------------

        predictions = model.predict(
            image_array,
            verbose=0
        )[0]


        # ---------------------------------------------
        # Safety check
        # ---------------------------------------------

        if len(predictions) != len(class_names):

            return json.dumps({
                "error": (
                    f"Model returned {len(predictions)} outputs "
                    f"but {len(class_names)} classes are configured."
                )
            })


        # ---------------------------------------------
        # Get top predictions
        # ---------------------------------------------

        sorted_indices = np.argsort(
            predictions
        )[::-1]

        top_index = int(
            sorted_indices[0]
        )

        second_index = int(
            sorted_indices[1]
        )


        top_probability = float(
            predictions[top_index]
        )

        second_probability = float(
            predictions[second_index]
        )


        confidence = top_probability * 100

        margin = (
            top_probability -
            second_probability
        )


        predicted_class = class_names[
            top_index
        ]


        # ---------------------------------------------
        # NON-LEAF / UNCERTAIN CHECK
        # ---------------------------------------------

        # Case 1:
        # Model itself selected Non_Leaf

        if predicted_class == "Non_Leaf":

            return json.dumps(
                non_leaf_response(
                    confidence
                )
            )


        # Case 2:
        # Confidence too low

        if top_probability < CONFIDENCE_THRESHOLD:

            return json.dumps(
                non_leaf_response(
                    confidence
                )
            )


        # Case 3:
        # Top two predictions are too close

        if margin < MARGIN_THRESHOLD:

            return json.dumps(
                non_leaf_response(
                    confidence
                )
            )


        # ---------------------------------------------
        # Disease information
        # ---------------------------------------------

        info = disease_data.get(
            predicted_class,
            {
                "cause": "Disease information not available.",
                "cure": "Please consult an agriculture expert."
            }
        )


        # ---------------------------------------------
        # Healthy check
        # ---------------------------------------------

        is_healthy = (
            "healthy" in predicted_class.lower()
            or predicted_class == "Healthy"
        )


        if is_healthy:

            healthy_percentage = confidence
            affected_percentage = 100 - confidence

        else:

            healthy_percentage = 100 - confidence
            affected_percentage = confidence


        # ---------------------------------------------
        # Final response
        # ---------------------------------------------

        result = {

            "prediction": predicted_class,

            "confidence": round(
                confidence,
                2
            ),

            "healthy": round(
                healthy_percentage,
                2
            ),

            "affected": round(
                affected_percentage,
                2
            ),

            "cause": info["cause"],

            "cure": info["cure"]
        }


        return json.dumps(
            result
        )


    except Exception as e:

        return json.dumps({
            "error": str(e)
        })


# =========================================================
# CLI
# =========================================================

def main():

    if len(sys.argv) < 2:

        print(
            json.dumps({
                "error": "Image path required."
            })
        )

        return


    image_path = sys.argv[1]


    if not os.path.exists(image_path):

        print(
            json.dumps({
                "error": "Image file does not exist."
            })
        )

        return


    result = predict_leaf_disease(
        image_path
    )

    print(result)


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()

