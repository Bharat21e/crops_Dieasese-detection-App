# from fastapi import FastAPI, UploadFile, File
# from PIL import Image
# import numpy as np
# import tensorflow as tf
# import io

# app = FastAPI()

# class_names = [
#     "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
#     "Blueberry___healthy", "Cherry___Powdery_mildew", "Cherry___healthy",
#     "Corn___Cercospora_leaf_spot Gray_leaf_spot", "Corn___Common_rust",
#     "Corn___Northern_Leaf_Blight", "Corn___healthy",
#     "Grape___Black_rot", "Grape___Esca_(Black_Measles)",
#     "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
#     "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot",
#     "Peach___healthy", "Pepper,_bell___Bacterial_spot",
#     "Pepper,_bell___healthy", "Potato___Early_blight",
#     "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy",
#     "Soybean___healthy", "Squash___Powdery_mildew",
#     "Strawberry___Leaf_scorch", "Strawberry___healthy",
#     "Tomato___Bacterial_spot", "Tomato___Early_blight",
#     "Tomato___Late_blight", "Tomato___Leaf_Mold",
#     "Tomato___Septoria_leaf_spot",
#     "Tomato___Spider_mites Two-spotted_spider_mite",
#     "Tomato___Target_Spot",
#     "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
#     "Tomato___Tomato_mosaic_virus", "Tomato___healthy",  
#     "_Healthy", "Brown_Rust", "Yellow_Rust"
# ]

# sease_data = {
#     "Healthy": {"cause": "No disease present.", "cure": "Maintain good cultural practices."},
#     "Brown_Rust": {"cause": "Brown rust present.", "cure": "No update available."},
#     "Yellow_Rust": {"cause": "Yellow rust present.", "cure": "No update available."}
#     # ... add all other crop disease data from your original code ...
# }

# model = tf.keras.models.load_model("crop_leaf_model.h5")

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     try:
#         image_bytes = await file.read()
#         image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#         image = image.resize((150, 150))
#         image_array = np.array(image) / 255.0
#         image_array = np.expand_dims(image_array, axis=0)

#         predictions = model.predict(image_array)[0]
#         index = int(np.argmax(predictions))
#         label = class_names[index]

#         healthy = round(float(predictions[index]) * 100, 2)
#         affected = round(100 - healthy, 2)

#         info = sease_data.get(label, {
#             "cause": "Disease information not available.",
#             "cure": "Check nearby agriculture doctor."
#         })

#         return {
#             "prediction": label,
#             "healthy": healthy,
#             "affected": affected,
#             "cause": info["cause"],
#             "cure": info["cure"]
#         }
#     except Exception as e:
#         return {"error": str(e)}



from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf
import io

# ✅ FastAPI app
app = FastAPI()

# ✅ ADD: CORS (VERY IMPORTANT for React + Node)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:2000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Class names
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


# ✅ Disease info
sease_data = {
    "Apple___Apple_scab": {
        "cause": "Fungal infection by Venturia inaequalis.",
        "cure": "Plant resistant varieties, remove fallen leaves, and apply appropriate fungicides early in season."  # general
    },
    "Apple___Black_rot": {
        "cause": "Fungal disease leading to fruit and leaf rot.",
        "cure": "Remove and destroy infected branches and fruit; appropriate fungicide sprays may help; maintain sanitation."  # general
    },
    "Apple___Cedar_apple_rust": {
        "cause": "Rust fungus requiring apple and cedar hosts.",
        "cure": "Remove nearby junipers; plant resistant cultivars; apply rust-specific fungicides."  # general
    },
    "Apple___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good tree vigor; pruning and proper watering prevent stress."  # general
    },
    "Cherry___Powdery_mildew": {
        "cause": "Fungal powdery mildew infection.",
        "cure": "Improve air circulation, avoid high humidity, and apply sulfur or other fungicides."  # general
    },
    "Cherry___healthy": {
        "cause": "No disease.",
        "cure": "Standard orchard care."  # general
    },
    "Corn___Cercospora_leaf_spot Gray_leaf_spot": {
        "cause": "Fungal leaf spot disease aggravated by warm, humid conditions.",
        "cure": "Crop rotation, residue management, and fungicide application if severe."  # general
    },
    "Corn___Common_rust": {
        "cause": "Rust fungus producing pustules on leaves.",
        "cure": "Resistant hybrids, timely fungicide application; good field sanitation."  # general
    },
    "Corn___Northern_Leaf_Blight": {
        "cause": "Fungal disease favored by moisture.",
        "cure": "Rotation, resistant varieties, fungicides when outbreaks start."  # general
    },
    "Corn___healthy": {
        "cause": "No disease.",
        "cure": "Standard crop care."  # general
    },
    "Grape___Black_rot": {
        "cause": "Fungus causing black spots and fruit rot.",
        "cure": "Sanitation, resistant varieties, fungicides at proper timing."  # general
    },
    "Grape___Esca_(Black_Measles)": {
        "cause": "Fungal trunk disease complex.",
        "cure": "Remove infected wood; proper pruning and fungicides."  # general
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "cause": "Fungal leaf spot disease.",
        "cure": "Improve ventilation; treat with fungicides if needed."  # general
    },
    "Grape___healthy": {
        "cause": "No disease.",
        "cure": "Good vineyard practices."  # general
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "cause": "Bacterial disease spread by psyllid insects.",
        "cure": "Remove infected trees; control insect vectors."  # general
    },
    "Peach___Bacterial_spot": {
        "cause": "Bacterial infection causing black spots.",
        "cure": "Protective copper sprays; avoid overhead watering."  # general
    },
    "Peach___healthy": {
        "cause": "No disease.",
        "cure": "Standard orchard management."  # general
    },
    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacterial infection of leaves and fruit.",
        "cure": "Copper-based sprays; crop rotation."  # general
    },
    "Pepper,_bell___healthy": {
        "cause": "No disease.",
        "cure": "Good cultural practices."  # general
    },
    "Potato___Early_blight": {
        "cause": "Fungal disease common in wet weather.",
        "cure": "Fungicides, resistant cultivars, crop rotation."  # general
    },
    "Potato___Late_blight": {
        "cause": "Serious fungal-like pathogen (Phytophthora).",
        "cure": "Fungicides like chlorothalonil or copper sprays."  # general
    },
    "Potato___healthy": {
        "cause": "No disease.",
        "cure": "Good agronomy."  # general
    },
    "Raspberry___healthy": {
        "cause": "No disease.",
        "cure": "General management."  # general
    },
    "Soybean___healthy": {
        "cause": "No disease.",
        "cure": "Good crop care."  # general
    },
    "Squash___Powdery_mildew": {
        "cause": "Fungal powdery mildew on leaves.",
        "cure": "Improve spacing, apply sulfur or biological fungicides."  # general
    },
    "Strawberry___Leaf_scorch": {
        "cause": "Bacterial or fungal leaf burn.",
        "cure": "Remove infected leaves; ensure proper spacing and treat with appropriate sprays."  # general
    },
    "Strawberry___healthy": {
        "cause": "No disease.",
        "cure": "Standard care."  # general
    },
    "Tomato___Bacterial_spot": {
        "cause": "Bacterial spots on leaves/fruit.",
        "cure": "Copper sprays; crop rotation."  # general
    },
    "Tomato___Early_blight": {
        "cause": "Fungal disease causing target-like lesions.",
        "cure": "Resistant varieties, crop rotation, fungicides."  # general
    },
    "Tomato___Late_blight": {
        "cause": "Water mold pathogen causing severe blight and rot.",
        "cure": "Fungicides (mancozeb, chlorothalonil) and sanitation."  # general
    },
    "Tomato___Leaf_Mold": {
        "cause": "Fungal infection in humid conditions.",
        "cure": "Improve air circulation; apply fungicides."  # general
    },
    "Tomato___Septoria_leaf_spot": {
        "cause": "Fungal spots with dark margins on leaves.",
        "cure": "Remove debris and apply fungicides; good water management."  # general
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "cause": "Spider mites (pest) causing leaf stippling.",
        "cure": "Insecticidal soaps, neem oil, biological controls."  # general
    },
    "Tomato___Target_Spot": {
        "cause": "Fungal leaf spot disease.",
        "cure": "Sanitation, crop rotation, fungicides."  # general
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "cause": "Viral disease spread by whiteflies.",
        "cure": "Control whiteflies; use resistant varieties."  # general
    },
    "Tomato___Tomato_mosaic_virus": {
        "cause": "Viral infection.",
        "cure": "Remove infected plants; sanitation and resistant varieties."  # general
    },
    "Tomato___healthy": {
        "cause": "No disease.",
        "cure": "Maintain plant health."  # general
    },
    "wheat_Healthy": {
        "cause": "Wheat is healthy.",
        "cure": "Standard crop care."  # general
    },
    "wheat_septoria": {
        "cause": "Septoria leaf blotch caused by fungal pathogen Zymoseptoria tritici.",
        "cure": "Use resistant varieties; crop rotation; fungicides labeled for septoria control."  # general :contentReference[oaicite:1]{index=1}
    },
    "wheat_stripe_rust": {
        "cause": "Stripe rust (yellow rust) fungus on wheat.",
        "cure": "Grow resistant cultivars; apply foliar fungicides in early infection."  # general :contentReference[oaicite:2]{index=2}
    }
}



# ✅ Load model ONCE (important)
model = tf.keras.models.load_model("crop_leaf_model.h5")

# ✅ Prediction API
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
            "cure": "Consult nearby agriculture expert."
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

# ✅ ADD: Health check (optional but useful)
@app.get("/")
def root():
    return {"status": "Python ML API running"}

