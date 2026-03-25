import tensorflow as tf
import numpy as np
from PIL import Image
import os
import sys
from tensorflow.keras.applications.resnet50 import preprocess_input

# -------------------------
# 1️⃣ Load the model
model_path = "plant_disease_model.keras"

try:
    if not os.path.isfile(model_path):
        print(f"❌ Error: Model file not found at '{model_path}'")
        print(f"📍 Current working directory: {os.getcwd()}")
        sys.exit(1)

    model = tf.keras.models.load_model(model_path, compile=False)
    print(f"✅ Model loaded successfully from '{model_path}'")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)

# -------------------------
# 2️⃣ Define class names (replace with your 38 PlantVillage classes)
class_names = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                'Blueberry___healthy', 'Cherry___healthy', 'Cherry___Powdery_mildew', 'Corn___Cercospora_leaf_spot Gray_leaf_spot',
                  'Corn___Common_rust', 'Corn___healthy', 'Corn___Northern_Leaf_Blight', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 
                  'Grape___healthy', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Orange___Haunglongbing_(Citrus_greening)',
                    'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
                      'Potato___healthy', 'Potato___Late_blight', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
                        'Strawberry___healthy', 'Strawberry___Leaf_scorch', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 
                        'Tomato___healthy', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 
                        'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 
               'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus']

# -------------------------
# 3️⃣ Function to load & preprocess an image
IMG_SIZE = 224  # must match model input



def preprocess_image(image_path):
    """
    Load, resize, and preprocess an image for ResNet50 model.

    Args:
        image_path (str): Path to the image file

    Returns:
        np.ndarray: Preprocessed image array with shape (1, 224, 224, 3)

    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image cannot be processed
    """
    try:
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        img = Image.open(image_path).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img)

        # ResNet50 preprocessing
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        return img_array
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        raise
    except Exception as e:
        print(f"❌ Image Processing Error: {e}")
        raise ValueError(f"Could not process image: {e}")

# -------------------------
# 4️⃣ Ask user for image path
image_path = input("Enter path to leaf image: ")

try:
    if not os.path.isfile(image_path):
        print("❌ File not found:", image_path)
        sys.exit(1)

    print(f"🔄 Processing image: {image_path}")
    img = preprocess_image(image_path)

    # -------------------------
    # 5️⃣ Predict
    print("🤖 Running inference...")
    preds = model.predict(img)
    pred_idx = np.argmax(preds)
    confidence = preds[0][pred_idx] * 100

    # -------------------------
    # 6️⃣ Print results
    predicted_class = class_names[pred_idx]
    print(f"\n{'='*50}")
    print(f"✅ Prediction Complete")
    print(f"{'='*50}")
    print(f"🌿 Plant Disease: {predicted_class}")
    print(f"📊 Confidence: {confidence:.2f}%\n")

except ValueError as e:
    print(f"❌ Validation Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    sys.exit(1)
