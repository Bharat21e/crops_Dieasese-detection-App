import sys
import json
from PIL import Image
import numpy as np
import tensorflow as tf

# Define the class names
class_names = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
     "Blueberry___healthy", "Cherry___Powdery_mildew", "Cherry___healthy",
    "Corn___Cercospora_leaf_spot Gray_leaf_spot", "Corn___Common_rust", "Corn___Northern_Leaf_Blight", "Corn___healthy",
    "Grape___Black_rot", "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy", "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy", "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy",
    "Soybean___healthy", "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy",
    "Healthy","Brown_Rust","Yellow_Rust"
]

# Disease data dictionary
disease_data = {
    "Apple___Apple_scab": {
        "cause": "Fungus Venturia inaequalis. Favorable conditions are cool, wet weather.",
        "cure": "Use fungicides and resistant apple varieties. Prune and destroy infected leaves."
    },
    "Apple___Black_rot": {
        "cause": "Caused by the fungus Botryosphaeria obtusa.",
        "cure": "Prune and remove infected areas. Apply fungicides during the growing season."
    },
    "Apple___Cedar_apple_rust": {
        "cause": "Fungus Gymnosporangium juniperi-virginianae. Requires junipers as an alternate host.",
        "cure": "Remove nearby juniper hosts. Use resistant varieties and fungicides."
    },
    "Apple___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
   
    "Blueberry___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Cherry___Powdery_mildew": {
        "cause": "Fungus Podosphaera clandestina.",
        "cure": "Apply sulfur-based or fungicide treatments. Ensure good air circulation."
    },
    "Cherry___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Corn___Cercospora_leaf_spot Gray_leaf_spot": {
        "cause": "Fungus Cercospora zeae-maydis.",
        "cure": "Use resistant hybrids and fungicide sprays."
    },
    "Corn___Common_rust": {
        "cause": "Fungus Puccinia sorghi.",
        "cure": "Apply fungicides and plant resistant varieties."
    },
    "Corn___Northern_Leaf_Blight": {
        "cause": "Fungus Exserohilum turcicum.",
        "cure": "Use resistant varieties and fungicides."
    },
    "Corn___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Grape___Black_rot": {
        "cause": "Fungus Guignardia bidwellii.",
        "cure": "Prune infected areas and apply fungicides."
    },
    "Grape___Esca_(Black_Measles)": {
        "cause": "Fungal complex including Phaeomoniella chlamydospora.",
        "cure": "Remove infected wood. Avoid injuries to vines."
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "cause": "Fungus Pseudocercospora vitis.",
        "cure": "Apply fungicides and manage vineyard hygiene."
    },
    "Grape___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "cause": "Bacterium Candidatus Liberibacter spp. Spread by psyllid insects.",
        "cure": "Control psyllid population and remove infected trees."
    },
    "Peach___Bacterial_spot": {
        "cause": "Bacterium Xanthomonas campestris pv. pruni.",
        "cure": "Use resistant varieties and copper-based bactericides."
    },
    "Peach___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacterium Xanthomonas campestris pv. vesicatoria.",
        "cure": "Use copper-based bactericides and resistant varieties."
    },
    "Pepper,_bell___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Potato___Early_blight": {
        "cause": "Fungus Alternaria solani.",
        "cure": "Apply fungicides and practice crop rotation."
    },
    "Potato___Late_blight": {
        "cause": "Pathogen Phytophthora infestans.",
        "cure": "Use resistant varieties and fungicides."
    },
    "Potato___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Raspberry___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Soybean___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Squash___Powdery_mildew": {
        "cause": "Fungal pathogens including Erysiphe cichoracearum.",
        "cure": "Apply sulfur-based fungicides and maintain good air circulation."
    },
    "Strawberry___Leaf_scorch": {
        "cause": "Fungus Diplocarpon earlianum.",
        "cure": "Remove infected leaves and apply fungicides."
    },
    "Strawberry___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Tomato___Bacterial_spot": {
        "cause": "Bacterium Xanthomonas spp.",
        "cure": "Apply copper-based bactericides and practice crop rotation."
    },
    "Tomato___Early_blight": {
        "cause": "Fungus Alternaria solani.",
        "cure": "Apply fungicides and remove infected leaves."
    },
    "Tomato___Late_blight": {
        "cause": "Pathogen Phytophthora infestans.",
        "cure": "Use resistant varieties and fungicides."
    },
    "Tomato___Leaf_Mold": {
        "cause": "Fungus Passalora fulva.",
        "cure": "Apply fungicides and ensure good ventilation."
    },
    "Tomato___Septoria_leaf_spot": {
        "cause": "Fungus Septoria lycopersici.",
        "cure": "Remove infected leaves and apply fungicides."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "cause": "Spider mites Tetranychus urticae.",
        "cure": "Use miticides or insecticidal soaps."
    },
    "Tomato___Target_Spot": {
        "cause": "Fungus Corynespora cassiicola.",
        "cure": "Apply fungicides and ensure good air circulation."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "cause": "Virus spread by whiteflies.",
        "cure": "Control whitefly population and use resistant varieties."
    },
    "Tomato___Tomato_mosaic_virus": {
        "cause": "Virus transmitted through contact and contaminated tools.",
        "cure": "Remove infected plants and sterilize tools."
    },
    "Tomato___healthy": {
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Healthy":{
        "cause": "No disease present.",
        "cure": "Maintain good cultural practices for optimal health."
    },
    "Brown_Rust":{
        "cause": "brown Rust present.",
        "cure": "no update availabel."
    },
     "Yellow_Rust":{  
        "cause": "yellow Rust present.",
        "cure": "no update availabel."
    }
    
    
}

# Load the model
try:
    model = tf.keras.models.load_model('wheatleaf_disease/crop_leaf_model.h5')
except Exception as e:
    print(json.dumps({"error": f"Failed to load model: {str(e)}"}))
    sys.exit(1)

# Prediction function
def predict_leaf_disease(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        image = image.resize((150, 150))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array)[0]
        predicted_index = int(np.argmax(predictions))
        predicted_class = class_names[predicted_index]

        healthy = float(predictions[predicted_index]) * 100
        affected = 100.0 - healthy

        disease_info = disease_data.get(predicted_class, {
            "cause": "Disease information not available.",
            "cure": "check information  near crops docters."
        })

        return json.dumps({
            "prediction": predicted_class,
            "healthy": round(healthy, 2),
            "affected": round(affected, 2),
            "cause": disease_info["cause"],
            "cure": disease_info["cure"]
        })

    except Exception as e:
        return json.dumps({"error": str(e)})

# CLI main function
def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Image path required"}))
        return

    image_path = sys.argv[1]
    try:
        result = predict_leaf_disease(image_path)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == '__main__':
    main()
