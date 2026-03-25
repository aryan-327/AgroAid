import json

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

database = {}

def format_disease(disease):
    return disease.replace('_', ' ').replace('   ', ' ')

def get_pathogen(disease):
    d = disease.lower()
    if 'bacterial' in d: return "Bacterium: Xanthomonas species"
    if 'fungal' in d or 'blight' in d or 'scab' in d or 'rust' in d or 'rot' in d or 'mold' in d or 'mildew' in d or 'esca' in d or 'spot' in d:
        if 'early_blight' in d: return "Fungus: Alternaria solani"
        if 'late_blight' in d: return "Oomycete: Phytophthora infestans"
        if 'powdery_mildew' in d: return "Fungus: Podosphaera spp."
        if 'rust' in d: return "Fungus: Puccinia spp."
        if 'apple_scab' in d: return "Fungus: Venturia inaequalis"
        if 'black_rot' in d: return "Fungus: Botryosphaeria obtusa"
        if 'septoria' in d: return "Fungus: Septoria lycopersici"
        if 'scorch' in d: return "Fungus: Diplocarpon earlianum"
        return "Fungus: Pathogenic fungal strain"
    if 'virus' in d or 'curl' in d or 'mosaic' in d:
        return "Virus: Tobamovirus or Begomovirus"
    if 'mites' in d:
        return "Arachnid: Tetranychus urticae"
    if 'greening' in d:
        return "Bacterium: Candidatus Liberibacter asiaticus"
    return "Unknown pathogen"

for c in classes:
    parts = c.split('___')
    plant_raw = parts[0]
    disease_raw = parts[1] if len(parts) > 1 else 'healthy'
    
    plant = plant_raw.replace('_', ' ').replace(',', '')
    disease = disease_raw.replace('_', ' ')
    
    is_healthy = 'healthy' in disease.lower()
    
    if is_healthy:
        database[c] = {
            "isHealthy": True,
            "pathogen": "None",
            "spread": "N/A",
            "conditions": { "tempMin": 18, "tempMax": 28, "humidityMin": 40, "humidityMax": 70, "notes": "Optimal growing conditions." },
            "summary": f"Your {plant} appears healthy and shows no signs of disease.",
            "symptoms": "Leaves are vibrant, firm, and show no unusual markings, wilting, or discoloration.",
            "treatment": "No treatment required. Continue regular watering and fertilization.",
            "prevention": "Maintain consistent watering, ensure good air circulation, and inspect regularly for pests."
        }
    else:
        pathogen = get_pathogen(disease_raw)
        
        spread = ""
        if "Bacterium" in pathogen: spread = "Water splash, contaminated tools, infected seeds"
        elif "Fungus" in pathogen or "Oomycete" in pathogen: spread = "Wind-dispersed spores, lingering crop debris, soil contact"
        elif "Virus" in pathogen: spread = "Aphids, whiteflies, contaminated tools"
        elif "Arachnid" in pathogen: spread = "Wind, human clothing, neighboring plants"
        else: spread = "Infected plant material, soil contact"
        
        t_min = 20
        t_max = 30
        h_min = 60
        h_max = 90
        if "Fungus" in pathogen:
            t_min = 22; t_max = 28; h_min = 80; h_max = 100
        elif "Virus" in pathogen:
            t_min = 25; t_max = 35; h_min = 40; h_max = 70
        elif "Arachnid" in pathogen:
            t_min = 27; t_max = 35; h_min = 20; h_max = 50
        
        db_entry = {
            "isHealthy": False,
            "pathogen": pathogen,
            "spread": spread,
            "conditions": { "tempMin": t_min, "tempMax": t_max, "humidityMin": h_min, "humidityMax": h_max, "notes": "Thrives in these parameters." },
            "summary": f"{format_disease(disease_raw)} is a destructive disease affecting {plant} crops, causing significant yield and quality loss if unchecked.",
            "symptoms": "Initial symptoms include small lesions or discoloration on lower leaves. As it progresses, it may cause wilting, severe necrotic spots, or fruit rot.",
            "treatment": "Apply appropriate registered treatments immediately. Remove and destroy heavily infected parts to limit the spread.",
            "prevention": "Practice crop rotation, ensure adequate plant spacing for airflow, and sanitize tools between uses."
        }
        database[c] = db_entry

# Write explicitly as a JS export
with open(r"c:\Users\aruna\OneDrive\Desktop\PROGRAMMING\Agro Aid\frontend\src\data\diseaseInfo.js", "w", encoding="utf-8") as f:
    f.write("export const diseaseInfo = ")
    json.dump(database, f, indent=2, ensure_ascii=False)
    f.write(";\n")
