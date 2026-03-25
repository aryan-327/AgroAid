# AgroAid - AI Crop Disease Predictor

🌾 **An intelligent agricultural solution for identifying crop diseases using deep learning**

## 📋 Overview

AgroAid is a full-stack web application that uses a pre-trained ResNet50 deep learning model to identify 38 different plant diseases from leaf images. The system supports three languages (English, Hindi, Odia) and provides disease information, treatment recommendations, and agricultural tips.

**Features:**
- 📸 Image upload and camera capture
- 🤖 AI-powered disease classification (ResNet50)
- 📊 Confidence scoring for predictions
- 💊 Treatment recommendations and solutions
- 🌍 Multi-language support (English, Hindi, Odia)
- 📱 Responsive design (mobile & desktop)
- 🎨 Premium UI with Framer Motion animations

---

## 🏗️ Project Structure

```
Agro Aid/
├── app.py                          # Flask backend (Python)
├── predict.py                      # Standalone prediction script
├── plant_disease_model.keras       # Pre-trained TensorFlow model (28.5 MB)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── frontend/                       # React + Vite frontend
│   ├── src/
│   │   ├── components/            # React components (7 files)
│   │   ├── data/                  # Disease database JSON
│   │   ├── locales/               # Translations (en, hi, od)
│   │   ├── services/              # API integration
│   │   ├── App.jsx
│   │   └── index.css              # Design system & styles
│   ├── public/
│   ├── vite.config.js             # Vite config with API proxy
│   ├── package.json               # Node dependencies
│   ├── .env.example               # Frontend env template
│   └── README.md                  # Frontend documentation
│
└── .stitch/designs/               # Design templates (reference only)
```

---

## 🌾 Supported Plant Diseases

**38 Plant-Disease Combinations:**

| Plant | Diseases | Count |
|-------|----------|-------|
| Apple 🍎 | Scab, Black Rot, Cedar Apple Rust, Healthy | 4 |
| Blueberry | Healthy | 1 |
| Cherry 🍒 | Healthy, Powdery Mildew | 2 |
| Corn 🌽 | Cercospora Leaf Spot, Common Rust, Healthy, Northern Leaf Blight | 4 |
| Grape 🍇 | Black Rot, Esca, Healthy, Leaf Blight | 4 |
| Orange 🍊 | Haunglongbing (Citrus Greening) | 1 |
| Peach 🍑 | Bacterial Spot, Healthy | 2 |
| **Pepper** 🌶️ | Bacterial Spot, Healthy | **2** |
| **Potato** 🥔 | Early Blight, Healthy, Late Blight | **3** |
| Raspberry | Healthy | 1 |
| Soybean | Healthy | 1 |
| Squash | Powdery Mildew | 1 |
| Strawberry 🍓 | Healthy, Leaf Scorch | 2 |
| **Tomato** 🍅 | Bacterial Spot, Early Blight, Healthy, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Tomato Mosaic Virus, Tomato Yellow Leaf Curl Virus | **10** |

**Total: 38 classifications**

---

## ⚙️ Tech Stack

### Backend
- **Framework**: Flask 3.0.0
- **CORS**: Flask-CORS 4.0.0
- **ML Model**: TensorFlow 2.15.0 / Keras
- **Image Processing**: Pillow 10.0.0
- **Data Processing**: NumPy 1.26.0
- **Runtime**: Python 3.9+

### Frontend
- **Framework**: React 19.2.4
- **Build Tool**: Vite 8.0.0
- **Styling**: TailwindCSS 4.2.1
- **Animations**: Framer Motion 12.38.0
- **Internationalization**: i18next 25.8.18
- **HTTP Client**: Axios 1.13.6
- **Linting**: ESLint 9.39.4

### Model
- **Architecture**: ResNet50 (Pre-trained)
- **Training Data**: PlantVillage Dataset
- **Input**: 224×224 RGB images
- **Output**: 38-class probability distribution

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher (for frontend)
- pip (Python package manager)
- npm or yarn (Node package manager)

### Step 1: Backend Setup

```bash
# Navigate to root directory (Agro Aid folder)
cd "Agro Aid"

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Create environment file (optional)
cp .env.example .env.local

# Return to root
cd ..
```

---

## 🏃 Running the Application

### Option A: Terminal Tabs (Recommended for Development)

**Terminal 1 - Backend:**
```bash
# From root directory, activate venv if needed
python app.py
```
Backend will start on: `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
# From root/frontend directory
npm run dev
```
Frontend will start on: `http://localhost:5173`

Open browser to: **http://localhost:5173**

### Option B: Single Terminal (Using `&`)

```bash
# Start backend in background
python app.py &

# Start frontend
cd frontend && npm run dev
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-03-18T10:30:00.000Z"
}
```

#### 2. Predict Disease
```
POST /api/predict

Content-Type: multipart/form-data
Form Data:
  - file: <image file (JPEG, PNG, WebP)>

Response (Success):
{
  "class": "Tomato___Early_Blight",
  "confidence": 0.9847,
  "plant": "Tomato",
  "disease_name": "Early Blight",
  "scientific_name": "",
  "message": "Prediction successful"
}

Response (Error):
{
  "error": "Invalid image",
  "message": "Could not process the uploaded image..."
}
```

**Max File Size:** 10 MB
**Supported Formats:** JPEG, PNG, WebP

#### 3. Get All Classes
```
GET /api/classes

Response:
{
  "classes": ["Apple___Apple_scab", "Apple___Black_rot", ...],
  "total": 38,
  "message": "Classes retrieved successfully"
}
```

#### 4. API Status
```
GET /api/status

Response:
{
  "api": "AgroAid Plant Disease Prediction",
  "version": "1.0.0",
  "model": "ResNet50 - PlantVillage Dataset",
  "classes": 38,
  "model_loaded": true,
  "endpoints": { ... }
}
```

---

## 🧪 Testing

### Test the Backend Directly

```bash
# Health check
curl http://localhost:5000/api/health

# List all classes
curl http://localhost:5000/api/classes

# Predict (with image)
curl -X POST http://localhost:5000/api/predict \
  -F "file=@/path/to/leaf_image.jpg"
```

### Standalone Prediction Script

```bash
# Run the predict.py script directly
python predict.py

# When prompted, enter the path to an image file
# Example: images/tomato_leaf.jpg
```

### Frontend Testing

1. Open http://localhost:5173 in browser
2. Upload a leaf image or capture with camera
3. View prediction results
4. Switch languages (English, Hindi, Odia)
5. Read disease solutions and tips

---

## 🌐 Environment Configuration

### Backend (.env at root)
```env
# Optional configuration
FLASK_DEBUG=True
```

### Frontend (.env.local at frontend/)
```env
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=AgroAid
VITE_DEBUG=false
```

---

## 📁 Key Files Explained

### Backend
- **app.py** - Main Flask application
  - `/api/health` - Health check
  - `/api/predict` - Disease prediction endpoint
  - `/api/classes` - List classes
  - `/api/status` - API info
  - Model loading and error handling
  - CORS configuration

- **predict.py** - Standalone CLI script for local predictions
  - Load model from disk
  - Preprocess image (ResNet50)
  - Run inference
  - Display results

- **plant_disease_model.keras** - Pre-trained TensorFlow model
  - ResNet50 architecture
  - 38-class output
  - Ready to use (no training required)

- **requirements.txt** - Python dependencies
  - Flask, TensorFlow, Pillow, NumPy
  - Flask-CORS for cross-origin requests

### Frontend
- **package.json** - Node dependencies and scripts
  - `npm run dev` - Start development server
  - `npm run build` - Production build
  - `npm run lint` - ESLint checking

- **vite.config.js** - Vite configuration
  - React plugin setup
  - API proxy (localhost:5000)
  - TailwindCSS plugin

- **src/services/api.js** - Axios API client
  - Configures base URL from environment
  - `predictDisease()` - Submit image for prediction
  - `checkHealth()` - Check API health
  - 30-second timeout

- **src/App.jsx** - Main React component
  - Orchestrates all sub-components
  - Manages image upload & predictions
  - Error handling with demo fallback
  - Custom cursor for desktop

- **src/data/disease_solutions.json** - Disease database
  - 38 plant-disease entries
  - Disease names, scientific names
  - Treatment solutions
  - Agricultural tips
  - Severity levels

- **src/locales/** - Translation files
  - en.json (English)
  - hi.json (Hindi)
  - od.json (Odia)

---

## 🐛 Troubleshooting

### Backend won't start
```
Error: Model file not found
→ Ensure plant_disease_model.keras is in root directory
```

### Frontend can't connect to backend
```
Error: Failed to fetch /api/predict
→ Check if backend is running on localhost:5000
→ Check browser DevTools Network tab
→ Verify Vite proxy in vite.config.js
```

### Image upload fails
```
Error: Could not process image
→ Ensure image is valid (JPEG, PNG, WebP)
→ Check file size < 10 MB
→ Try a different image format
```

### Model inference is slow
```
→ First prediction is slower (model warming up)
→ Subsequent predictions are faster
→ On M1/M2 Mac or GPU, inference is much faster
```

### Language not switching
```
→ Check browser console for i18n errors
→ Verify locales JSON files exist
→ Hard refresh browser (Ctrl+Shift+R)
```

---

## 📈 Performance Notes

- **Backend Response Time:** 2-5 seconds (first request), 0.5-2 seconds (subsequent)
- **Frontend Load:** < 2 seconds (Vite HMR enabled)
- **Model Size:** 28.5 MB (pre-trained, optimized)
- **Model Input:** 224×224 pixels (auto-resized)

---

## 🔒 Security Notes

- No authentication required (internal/demo app)
- CORS enabled for localhost only
- File upload limited to 10 MB
- Input validation on all endpoints
- No sensitive data stored

---

## 📝 Development Workflow

1. **Backend Development:** Edit `app.py` → Flask auto-reloads
2. **Frontend Development:** Edit React files → Vite HMR auto-updates
3. **Model Updates:** Replace `plant_disease_model.keras` → Restart backend
4. **Add Language:** Create `src/locales/[lang].json` → Update i18n config
5. **Add Disease:** Update `disease_solutions.json` and model classes

---

## 🚢 Deployment

### Build Frontend
```bash
cd frontend
npm run build
# Creates dist/ folder with optimized build
```

### Production Server
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production WSGI server
pip install gunicorn
gunicorn app:app --workers 4 --bind 0.0.0.0:5000
```

---

## 📄 License

All rights reserved. Project: AgroAid

---

## 👥 Team & Support

Built with ❤️ for sustainable agriculture.

For issues or questions:
1. Check troubleshooting section above
2. Review error messages in browser DevTools
3. Check Flask terminal output
4. Ensure all dependencies are installed

---

## 🎯 Future Enhancements

- [ ] User authentication & history
- [ ] Multiple language support expansion
- [ ] Real-time batch predictions
- [ ] Export predictions as PDF/CSV
- [ ] Mobile app (React Native)
- [ ] On-device ML (TensorFlow Lite)
- [ ] Weather integration for recommendations
- [ ] Farmer community features

---

**Last Updated:** March 18, 2024
**Version:** 1.0.0
**Status:** ✅ Ready for deployment
