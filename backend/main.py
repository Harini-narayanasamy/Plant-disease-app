import os
import io
import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image

try:
    from disease_info import disease_info
except ImportError:
    from backend.disease_info import disease_info

app = FastAPI(title="Plant Disease API")

# Setup CORS to allow React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allows all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Model Loading
# ---------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "trained_model.keras")
model = None

try:
    print(f"Loading model from {MODEL_PATH}")
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# ---------------------------------------------------
# Class Names
# ---------------------------------------------------
class_name = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

def format_class_name(raw_name):
    return raw_name.replace("___", " - ").replace("_", " ")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend is running"}

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded correctly on server.")
    
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize((128, 128))
        
        # Convert to numpy array and preprocess
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.expand_dims(input_arr, axis=0)
        
        # Predict
        start_time = time.time()
        prediction = model.predict(input_arr, verbose=0)
        eval_time = (time.time() - start_time) * 1000 # in ms
        
        result_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction)) * 100
        
        predicted_class = class_name[result_index]
        formatted_name = format_class_name(predicted_class)
        
        is_healthy = "healthy" in predicted_class.lower()

        disease_details = disease_info.get(predicted_class, {
            "description": "No detailed information available.",
            "remedy": "Consult an agricultural expert."
        })

        return {
            "success": True,
            "raw_class": predicted_class,
            "disease_name": formatted_name,
            "confidence": confidence,
            "is_healthy": is_healthy,
            "description": disease_details["description"],
            "remedy": disease_details["remedy"],
            "inference_time_ms": eval_time
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

# To run: uvicorn main:app --reload --host 0.0.0.0 --port 8000
