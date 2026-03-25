"""
AgroAid Flask Backend
Plant Disease Prediction API
"""

import os
import sys
import json
import base64
import logging
from io import BytesIO
from datetime import datetime

import tensorflow as tf
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.applications.resnet50 import preprocess_input

# ───────────────────────────────────────────────────────────────
# Configuration
# ───────────────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:5173", "http://localhost:3173"]}})

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Model path
MODEL_PATH = "plant_disease_model.keras"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Plant-Disease Class Names (38 classes from PlantVillage)
CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry___healthy', 'Cherry___Powdery_mildew',
    'Corn___Cercospora_leaf_spot Gray_leaf_spot', 'Corn___Common_rust', 'Corn___healthy', 'Corn___Northern_Leaf_Blight',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___healthy', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
    'Potato___Early_blight', 'Potato___healthy', 'Potato___Late_blight',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___healthy', 'Strawberry___Leaf_scorch',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___healthy', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus'
]

# Global model variable
model = None

# ───────────────────────────────────────────────────────────────
# Model Loading
# ───────────────────────────────────────────────────────────────

def load_model():
    """Load the Keras model from disk."""
    global model
    try:
        if not os.path.isfile(MODEL_PATH):
            logger.error(f"Model file not found at {MODEL_PATH}")
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        logger.info(f"✅ Model loaded successfully from {MODEL_PATH}")
        return True
    except Exception as e:
        logger.error(f"❌ Error loading model: {str(e)}")
        return False

# ───────────────────────────────────────────────────────────────
# Image Preprocessing
# ───────────────────────────────────────────────────────────────

def preprocess_image(image_bytes):
    """
    Preprocess image for ResNet50 model.

    Args:
        image_bytes (bytes): Raw image bytes

    Returns:
        tuple: (preprocessed array, original image PIL object) or (None, None) on error
    """
    try:
        image = Image.open(BytesIO(image_bytes)).convert('RGB')
        image = image.resize((224, 224))
        image_array = np.array(image)
        image_array = preprocess_input(image_array)
        image_array = np.expand_dims(image_array, axis=0)
        return image_array, image
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        return None, None

def generate_gradcam_plus_plus(img_array, model, class_idx):
    try:
        # Find the last convolutional layer
        target_layer = None
        inner_model = model
        
        # Check if model is nested or has a base model
        for layer in reversed(model.layers):
            output = layer.output
            if isinstance(output, list):
                output = output[0]
            if hasattr(output, 'shape') and len(output.shape) == 4:
                target_layer = layer
                break
                
        if target_layer is None:
            for layer in model.layers:
                if isinstance(layer, tf.keras.Model):
                    inner_model = layer
                    for l in reversed(inner_model.layers):
                        output = l.output
                        if isinstance(output, list):
                            output = output[0]
                        if hasattr(output, 'shape') and len(output.shape) == 4:
                            target_layer = l
                            break
                    break
                    
        if target_layer is None:
            logger.error("Could not find a convolutional layer for Grad-CAM++")
            return None

        tl_output = target_layer.output
        if isinstance(tl_output, list):
            tl_output = tl_output[0]

        grad_model = tf.keras.models.Model(
            inner_model.inputs,
            [tl_output, inner_model.output]
        )

        img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)

        with tf.GradientTape() as tape:
            tape.watch(img_tensor)
            conv_outputs, predictions = grad_model(img_tensor)
            loss = predictions[:, class_idx]

        # First derivative
        grads = tape.gradient(loss, conv_outputs)
        if grads is None:
            return None
            
        first_derivative = grads
        second_derivative = tf.square(first_derivative)
        third_derivative = first_derivative * second_derivative
        
        global_sum = tf.reduce_sum(conv_outputs, axis=(0, 1, 2))
        
        alpha_num = second_derivative
        alpha_denom = 2.0 * second_derivative + global_sum * third_derivative
        alpha_denom = tf.where(alpha_denom != 0.0, alpha_denom, tf.ones_like(alpha_denom))
        
        alphas = alpha_num / alpha_denom
        weights = tf.maximum(first_derivative, 0.0) # ReLU
        
        alpha_normalization_constant = tf.reduce_sum(alphas, axis=(1,2))
        alphas /= tf.reshape(alpha_normalization_constant + 1e-7, (1, 1, 1, -1))
        
        deep_linearization_weights = tf.reduce_sum(alphas * weights, axis=(1, 2))
        cam = tf.reduce_sum(deep_linearization_weights * conv_outputs, axis=-1)
        cam = tf.maximum(cam, 0.0) # ReLU
        
        cam_max = tf.reduce_max(cam)
        if cam_max != 0:
            cam = cam / cam_max
            
        return cam.numpy()[0]
    except Exception as e:
        import traceback
        logger.error(f"Grad-CAM++ Generation Error Details:\n{traceback.format_exc()}")
        return None

def apply_jet_colormap_and_encode(cam, original_image):
    try:
        from PIL import ImageFilter
        import io
        import base64
        
        # Resize to match original image
        cam_img = Image.fromarray(np.uint8(255 * cam)).resize(original_image.size, Image.Resampling.LANCZOS)
        
        # Apply Gaussian blur (σ=1.5) before colormap conversion to reduce artifacts
        cam_img = cam_img.filter(ImageFilter.GaussianBlur(1.5))
        
        v = np.array(cam_img) / 255.0
        four_v = 4 * v
        
        # Jet colormap formula
        r = np.clip(np.minimum(four_v - 1.5, -four_v + 4.5), 0, 1)
        g = np.clip(np.minimum(four_v - 0.5, -four_v + 3.5), 0, 1)
        b = np.clip(np.minimum(four_v + 0.5, -four_v + 2.5), 0, 1)
        
        # Transparent (0%) blending to 0.55 opacity for heatmap regions
        a = np.clip(v * 2, 0, 1) * 0.55
        
        colored = np.stack([r, g, b, a], axis=-1) * 255
        colored = colored.astype(np.uint8)
        
        heatmap_overlay = Image.fromarray(colored, 'RGBA')
        result = Image.alpha_composite(original_image.convert('RGBA'), heatmap_overlay)
        
        buffer = io.BytesIO()
        result.convert('RGB').save(buffer, format='JPEG', quality=85)
        b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        logger.error(f"Heatmap visualization error: {str(e)}")
        return None

# ───────────────────────────────────────────────────────────────
# API Routes
# ───────────────────────────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        return jsonify({
            'status': 'healthy',
            'model_loaded': model is not None,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict plant disease from uploaded image.

    Returns:
        JSON with:
        - class: predicted disease class name
        - confidence: confidence score (0-1)
        - scientific_name: disease scientific name (if available)
        - message: status message
    """
    try:
        # Check model is loaded
        if model is None:
            logger.warning("Model not loaded, attempting to load...")
            if not load_model():
                return jsonify({
                    'error': 'Model not available',
                    'message': 'ML model could not be loaded'
                }), 503

        # Check for file in request
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided',
                'message': 'Please upload an image file'
            }), 400

        file = request.files['file']

        # Validate file
        if file.filename == '':
            return jsonify({
                'error': 'Empty filename',
                'message': 'Please select a valid image file'
            }), 400

        if file.content_length and file.content_length > MAX_FILE_SIZE:
            return jsonify({
                'error': 'File too large',
                'message': f'Maximum file size is {MAX_FILE_SIZE / (1024*1024):.0f}MB'
            }), 400

        # Read and preprocess image
        image_bytes = file.read()
        img_array, original_image = preprocess_image(image_bytes)

        if img_array is None:
            return jsonify({
                'error': 'Invalid image',
                'message': 'Could not process the uploaded image. Please ensure it is a valid image file.'
            }), 400

        # Run prediction
        logger.info(f"Processing image: {file.filename}")
        predictions = model.predict(img_array, verbose=0)
        confidence = float(np.max(predictions))
        class_idx = int(np.argmax(predictions))
        class_name = CLASS_NAMES[class_idx]

        logger.info(f"Prediction: {class_name} (confidence: {confidence:.4f})")

        # Parse class name
        parts = class_name.split('___')
        plant = parts[0].replace('_', ' ') if len(parts) > 0 else 'Unknown'
        disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Healthy'
        
        # Generate Grad-CAM++ Heatmap
        heatmap_b64 = None
        if not 'healthy' in disease.lower():
            logger.info("Generating Grad-CAM++ heatmap...")
            cam = generate_gradcam_plus_plus(img_array, model, class_idx)
            if cam is not None:
                heatmap_b64 = apply_jet_colormap_and_encode(cam, original_image)

        return jsonify({
            'class': class_name,
            'confidence': round(confidence, 4),
            'plant': plant,
            'disease_name': disease,
            'scientific_name': '',
            'heatmap_base64': heatmap_b64,
            'message': 'Prediction successful'
        }), 200

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': 'Prediction failed',
            'message': f'An error occurred during prediction: {str(e)}'
        }), 500

@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Get list of all supported disease classes."""
    try:
        return jsonify({
            'classes': CLASS_NAMES,
            'total': len(CLASS_NAMES),
            'message': 'Classes retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Get API status and model information."""
    try:
        return jsonify({
            'api': 'AgroAid Plant Disease Prediction',
            'version': '1.0.0',
            'model': 'ResNet50 - PlantVillage Dataset',
            'classes': len(CLASS_NAMES),
            'model_loaded': model is not None,
            'endpoints': {
                '/api/health': 'Health check',
                '/api/predict': 'Disease prediction (POST)',
                '/api/classes': 'List all disease classes',
                '/api/status': 'API status'
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        'message': 'AgroAid Backend API',
        'endpoints': {
            'GET /api/health': 'Health check',
            'POST /api/predict': 'Predict plant disease from image',
            'GET /api/classes': 'List supported disease classes',
            'GET /api/status': 'API status and info'
        }
    }), 200

# ───────────────────────────────────────────────────────────────
# Error Handlers
# ───────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': 'The requested endpoint does not exist'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Server error', 'message': 'An internal server error occurred'}), 500

# ───────────────────────────────────────────────────────────────
# Application Startup
# ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("🌱 AgroAid Backend Starting...")
    print(f"📍 Working Directory: {os.getcwd()}")
    print(f"🤖 Model Path: {MODEL_PATH}")

    # Load model on startup
    if load_model():
        print(f"✅ {len(CLASS_NAMES)} plant disease classes loaded")
    else:
        print("⚠️  Warning: Model could not be loaded at startup")
        print("   The API will attempt to load the model on first request")

    print("\n🚀 Starting Flask server on http://localhost:5000")
    print("📡 CORS enabled for: localhost:3000, localhost:5173, localhost:3173\n")

    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )