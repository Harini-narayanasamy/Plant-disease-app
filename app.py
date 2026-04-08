import streamlit as st
import tensorflow as tf
import numpy as np

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="Plant Disease Recognition System",
    page_icon="🌿",
    layout="centered"
)

# ---------------------------------------------------
# Load Model (Cached for faster performance)
# ---------------------------------------------------
@st.cache_resource
def load_model():
    try:
        return tf.keras.models.load_model("trained_model.keras")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# ---------------------------------------------------
# Class Names (Must match training order exactly)
# ---------------------------------------------------
class_name = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# ---------------------------------------------------
# Disease Information (Description + Remedy)
# ---------------------------------------------------
disease_info = {
    'Apple___Apple_scab': {
        "description": "A fungal disease that causes olive-green to dark brown scabby lesions on leaves and fruits.",
        "remedy": "Remove infected leaves and fruits, improve air circulation, and apply a recommended fungicide."
    },
    'Apple___Black_rot': {
        "description": "A fungal disease causing black spots on leaves and rotting of fruits.",
        "remedy": "Prune infected branches, remove mummified fruits, and apply fungicide."
    },
    'Apple___Cedar_apple_rust': {
        "description": "A fungal disease causing yellow-orange spots on leaves and reducing plant vigor.",
        "remedy": "Remove nearby cedar hosts if possible and spray suitable fungicide during early growth."
    },
    'Apple___healthy': {
        "description": "The apple plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Continue regular watering, nutrition, and monitoring."
    },

    'Blueberry___healthy': {
        "description": "The blueberry plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Maintain proper irrigation, soil acidity, and routine monitoring."
    },

    'Cherry_(including_sour)___Powdery_mildew': {
        "description": "A fungal disease that appears as white powdery growth on leaves and shoots.",
        "remedy": "Remove infected leaves, improve ventilation, and apply sulfur or another recommended fungicide."
    },
    'Cherry_(including_sour)___healthy': {
        "description": "The cherry plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Continue proper pruning and routine care."
    },

    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': {
        "description": "A fungal leaf disease causing rectangular gray or tan lesions on leaves.",
        "remedy": "Use resistant varieties, practice crop rotation, and apply fungicide if severe."
    },
    'Corn_(maize)___Common_rust_': {
        "description": "A fungal disease causing reddish-brown pustules on both sides of corn leaves.",
        "remedy": "Use resistant hybrids and apply fungicide if infection is severe."
    },
    'Corn_(maize)___Northern_Leaf_Blight': {
        "description": "A fungal disease causing long, cigar-shaped gray-green lesions on leaves.",
        "remedy": "Use resistant varieties, rotate crops, and apply appropriate fungicide."
    },
    'Corn_(maize)___healthy': {
        "description": "The corn plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Maintain good field hygiene and balanced fertilization."
    },

    'Grape___Black_rot': {
        "description": "A fungal disease causing brown circular lesions on leaves and black shriveled fruits.",
        "remedy": "Remove infected leaves and fruits, prune properly, and apply fungicide."
    },
    'Grape___Esca_(Black_Measles)': {
        "description": "A complex fungal trunk disease causing leaf discoloration and berry spotting.",
        "remedy": "Prune infected wood, sanitize tools, and remove severely infected vines."
    },
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {
        "description": "A fungal disease causing brown irregular spots and blighting of grape leaves.",
        "remedy": "Remove infected foliage and apply suitable fungicide."
    },
    'Grape___healthy': {
        "description": "The grape plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Continue canopy management and regular observation."
    },

    'Orange___Haunglongbing_(Citrus_greening)': {
        "description": "A serious bacterial disease causing yellow shoots, mottled leaves, and poor-quality fruits.",
        "remedy": "Control psyllid insects, remove infected trees if necessary, and use certified disease-free plants."
    },

    'Peach___Bacterial_spot': {
        "description": "A bacterial disease causing dark angular spots on leaves and lesions on fruits.",
        "remedy": "Use resistant varieties, avoid overhead irrigation, and apply copper-based sprays."
    },
    'Peach___healthy': {
        "description": "The peach plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Maintain proper pruning and nutrition."
    },

    'Pepper,_bell___Bacterial_spot': {
        "description": "A bacterial disease causing small water-soaked spots that turn dark on leaves and fruits.",
        "remedy": "Remove infected plants, avoid leaf wetness, and apply copper-based bactericide."
    },
    'Pepper,_bell___healthy': {
        "description": "The bell pepper plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Continue good irrigation and crop care practices."
    },

    'Potato___Early_blight': {
        "description": "A fungal disease causing concentric ring-like brown spots on older leaves.",
        "remedy": "Remove infected leaves, avoid excess moisture, and apply fungicide."
    },
    'Potato___Late_blight': {
        "description": "A severe disease causing dark water-soaked lesions on leaves and tuber rot.",
        "remedy": "Remove infected plants immediately and apply recommended fungicide such as copper-based sprays."
    },
    'Potato___healthy': {
        "description": "The potato plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Maintain proper soil moisture and monitor regularly."
    },

    'Raspberry___healthy': {
        "description": "The raspberry plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Continue pruning and regular plant care."
    },

    'Soybean___healthy': {
        "description": "The soybean plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Maintain field sanitation and nutrient management."
    },

    'Squash___Powdery_mildew': {
        "description": "A fungal disease causing white powdery patches on leaves and stems.",
        "remedy": "Remove infected leaves, improve airflow, and apply sulfur or recommended fungicide."
    },

    'Strawberry___Leaf_scorch': {
        "description": "A fungal disease causing purple or red spots that enlarge and dry the leaf tissue.",
        "remedy": "Remove infected leaves, avoid overhead watering, and apply fungicide if needed."
    },
    'Strawberry___healthy': {
        "description": "The strawberry plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Maintain proper spacing and irrigation."
    },

    'Tomato___Bacterial_spot': {
        "description": "A bacterial disease causing dark spots on leaves, stems, and fruits.",
        "remedy": "Remove infected leaves, avoid overhead watering, and use copper-based bactericide."
    },
    'Tomato___Early_blight': {
        "description": "A fungal disease causing brown concentric-ring spots on older leaves.",
        "remedy": "Prune infected leaves, improve air circulation, and spray recommended fungicide."
    },
    'Tomato___Late_blight': {
        "description": "A destructive disease causing dark lesions, leaf collapse, and fruit rot.",
        "remedy": "Remove infected plants, avoid wet foliage, and apply copper-based or systemic fungicide."
    },
    'Tomato___Leaf_Mold': {
        "description": "A fungal disease causing yellow spots on upper leaf surfaces and mold underneath.",
        "remedy": "Reduce humidity, improve ventilation, and apply fungicide."
    },
    'Tomato___Septoria_leaf_spot': {
        "description": "A fungal disease causing many small circular spots with dark borders on leaves.",
        "remedy": "Remove infected leaves, avoid splashing water, and apply fungicide."
    },
    'Tomato___Spider_mites Two-spotted_spider_mite': {
        "description": "A pest infestation causing yellow speckling, leaf drying, and webbing on leaves.",
        "remedy": "Spray water under leaves, use neem oil or miticide, and remove heavily infested leaves."
    },
    'Tomato___Target_Spot': {
        "description": "A fungal disease causing circular brown lesions with concentric rings on leaves and fruits.",
        "remedy": "Remove infected plant parts and apply suitable fungicide."
    },
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
        "description": "A viral disease causing upward leaf curling, yellowing, and stunted growth.",
        "remedy": "Control whiteflies, remove infected plants, and use resistant varieties."
    },
    'Tomato___Tomato_mosaic_virus': {
        "description": "A viral disease causing mottled leaves, distortion, and reduced fruit yield.",
        "remedy": "Remove infected plants, disinfect tools, and avoid handling plants after tobacco exposure."
    },
    'Tomato___healthy': {
        "description": "The tomato plant appears healthy with no visible disease symptoms.",
        "remedy": "No treatment needed. Continue regular watering, staking, and monitoring."
    }
}

# ---------------------------------------------------
# Prediction Function
# IMPORTANT: No /255.0 because your model expects raw pixel values
# ---------------------------------------------------
def model_prediction(test_image):
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)

    # Keep raw pixel values because your model was trained that way
    input_arr = np.expand_dims(input_arr, axis=0)

    prediction = model.predict(input_arr, verbose=0)
    result_index = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    return result_index, confidence

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.title("📋 Dashboard")
app_mode = st.sidebar.selectbox(
    "Select Page",
    ["Home", "About", "Plant Disease Recognition"]
)

# ---------------------------------------------------
# Home Page
# ---------------------------------------------------
if app_mode == "Home":
    st.header("🌿 Plant Disease Recognition System")

    image_path = "plant_homepage.jpg"
    try:
        st.image(image_path, use_container_width=True)
    except:
        st.warning("Homepage image not found. Please make sure 'plant_homepage.jpg' is in your project folder.")

    st.markdown("""
    ### Welcome to the Plant Disease Recognition System

    This web application helps detect plant diseases from leaf images using a trained **Deep Learning (CNN)** model.

    #### 📌 Project Objective
    The main goal of this project is to automatically identify plant leaf diseases by analyzing uploaded images.  
    This helps farmers and agricultural users take quick action and improve crop health.

    #### 🚀 Features
    - Upload a plant leaf image
    - Predict the disease using a trained TensorFlow/Keras model
    - Display the predicted disease name
    - Show prediction confidence
    - Show disease description
    - Show recommended remedy
    - Simple and user-friendly interface

    #### 🛠 Technologies Used
    - Python
    - TensorFlow / Keras
    - NumPy
    - Streamlit
    - CNN (Convolutional Neural Network)

    #### 📷 How to Use
    1. Open the **Plant Disease Recognition** page from the sidebar.
    2. Upload a clear image of a plant leaf.
    3. Click **Show Image** (optional).
    4. Click **Predict**.
    5. View the disease result, confidence, and remedy.

    #### 🌱 Note
    For better accuracy, upload a clear and properly visible leaf image with good lighting.
    """)

# ---------------------------------------------------
# About Page
# ---------------------------------------------------
elif app_mode == "About":
    st.header("ℹ️ About This Project")

    st.markdown("""
    ### Plant Disease Recognition System

    This project uses a **Convolutional Neural Network (CNN)** based Deep Learning model to detect plant leaf diseases from uploaded images.

    #### 🔄 Project Workflow
    1. User uploads a plant leaf image
    2. Image is resized to **128 x 128**
    3. The trained CNN model processes the image
    4. The predicted disease class is identified
    5. Confidence score is calculated
    6. Disease description and remedy are displayed

    #### 🌾 Applications
    - Early disease detection in crops
    - Helps farmers take quick preventive action
    - Reduces crop loss
    - Supports smart agriculture solutions
    - Useful for academic and research projects

    #### 📚 Dataset
    This project is commonly built using the **PlantVillage dataset** containing multiple plant disease classes.

    #### 👨‍💻 Developed Using
    - Streamlit for Web Interface
    - TensorFlow/Keras for Model
    - NumPy for Image Processing
    """)

# ---------------------------------------------------
# Plant Disease Recognition Page
# ---------------------------------------------------
elif app_mode == "Plant Disease Recognition":
    st.header("🧪 Plant Leaf Disease Recognition")

    test_image = st.file_uploader(
        "Choose a plant leaf image:",
        type=["jpg", "jpeg", "png"]
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Show Image"):
            if test_image is not None:
                st.image(test_image, caption="Uploaded Leaf Image", use_container_width=True)
            else:
                st.warning("Please upload an image first.")

    with col2:
        if st.button("Predict"):
            if test_image is None:
                st.error("Please upload an image before prediction.")
            elif model is None:
                st.error("Model could not be loaded. Please check 'trained_model.keras' file.")
            else:
                with st.spinner("Analyzing the leaf image..."):
                    test_index, confidence = model_prediction(test_image)

                if test_index >= len(class_name):
                    st.error("Prediction index out of range. Please check your model class order.")
                else:
                    predicted_class = class_name[test_index]
                    formatted_name = predicted_class.replace("___", " - ").replace("_", " ")

                    st.balloons()

                    st.subheader("✅ Prediction Result")
                    st.success(f"**Predicted Disease:** {formatted_name}")
                    st.info(f"**Confidence:** {confidence:.2f}%")

                    if predicted_class in disease_info:
                        st.subheader("🦠 Disease Details")
                        st.write(f"**Description:** {disease_info[predicted_class]['description']}")
                        st.write(f"**Recommended Action:** {disease_info[predicted_class]['remedy']}")
                    else:
                        st.warning("Detailed information is not available for this disease.")

                    # Optional Debug Info (You can remove later)
                    with st.expander("🔍 Debug Info (Optional)"):
                        st.write("Predicted Index:", test_index)
                        st.write("Raw Class Name:", predicted_class)