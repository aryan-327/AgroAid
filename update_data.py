import json
import os

filepath = r"c:\Users\aruna\OneDrive\Desktop\PROGRAMMING\Agro Aid\frontend\src\data\disease_solutions.json"

classes = [
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

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

for c in classes:
    parts = c.split('___')
    plant_raw = parts[0]
    disease_raw = parts[1] if len(parts) > 1 else 'healthy'
    
    plant = plant_raw.replace('_', ' ').replace(',', '')
    disease = disease_raw.replace('_', ' ')
    
    is_healthy = 'healthy' in disease.lower()
    
    if c not in data:
        # Check if the slightly modified key exists (e.g., Pepper__bell)
        if plant_raw.replace(",_", "__") + "___" + disease_raw in data:
            data[c] = data[plant_raw.replace(",_", "__") + "___" + disease_raw]
            continue
            
        data[c] = {
            "plant": plant,
            "disease": disease,
            "severity": "None" if is_healthy else "Medium",
            "scientific": "",
            "description": "No disease detected." if is_healthy else "Disease identified. Further context required.",
            "clinical": {
                "en": { "fungicide": "No treatment required" if is_healthy else "Consult local agricultural extension", "dosage": "—", "method": "—", "frequency": "—", "safety": "—" },
                "hi": { "fungicide": "कोई उपचार नहीं" if is_healthy else "कृषि विशेषज्ञ से सलाह लें", "dosage": "—", "method": "—", "frequency": "—", "safety": "—" },
                "od": { "fungicide": "ଚିକିତ୍ସା ନାହିଁ" if is_healthy else "କୃଷି ବିଶେଷଜ୍ଞଙ୍କ ସହ ପରାମର୍ଶ କରନ୍ତୁ", "dosage": "—", "method": "—", "frequency": "—", "safety": "—" }
            },
            "remedy": {
                "en": { "cause": "Unknown", "immediate": "Monitor crop", "environmental": "—", "prevention": "—" },
                "hi": { "cause": "अज्ञात", "immediate": "फसल की निगरानी करें", "environmental": "—", "prevention": "—" },
                "od": { "cause": "ଅଜଣା", "immediate": "ଫସଲର ନିରୀକ୍ଷଣ କରନ୍ତୁ", "environmental": "—", "prevention": "—" }
            },
            "tips": []
        }

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
