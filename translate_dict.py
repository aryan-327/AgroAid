import os
import json
import re

FRONTEND_SRC = r"c:\Users\aruna\OneDrive\Desktop\PROGRAMMING\Agro Aid\frontend\src"

# Define static translations for plants
PLANTS_HI = {
    "Apple": "सेब", "Blueberry": "ब्लूबेरी", "Cherry": "चेरी", "Corn": "मक्का", 
    "Grape": "अंगूर", "Orange": "संतरा", "Peach": "आड़ू", "Pepper, bell": "शिमला मिर्च", 
    "Potato": "आलू", "Raspberry": "रास्पबेरी", "Soybean": "सोयाबीन", 
    "Squash": "लौकी/स्क्वैश", "Strawberry": "स्ट्रॉबेरी", "Tomato": "टमाटर"
}
PLANTS_OD = {
    "Apple": "ସେଓ", "Blueberry": "ବ୍ଲୁବେରୀ", "Cherry": "ଚେରୀ", "Corn": "ମକା", 
    "Grape": "ଅଙ୍ଗୁର", "Orange": "କମଳା", "Peach": "ପିଚ୍", "Pepper, bell": "କ୍ୟାପସିକମ୍", 
    "Potato": "ଆଳୁ", "Raspberry": "ରାସବେରୀ", "Soybean": "ସୋୟାବିନ୍", 
    "Squash": "ଲାଉ/ସ୍କ୍ୱାସ୍", "Strawberry": "ଷ୍ଟ୍ରବେରୀ", "Tomato": "ବିଲାତି ବାଇଗଣ"
}

# Define templates for healthy vs diseased
DISEASE_TEMPLATE_HI = {
    "summary": "{disease} एक विनाशकारी रोग है जो {plant} की फसल को प्रभावित करता है, जिससे अनियंत्रित होने पर उपज और गुणवत्ता में भारी नुकसान होता है।",
    "symptoms": "प्रारंभिक लक्षणों में निचली पत्तियों पर छोटे घाव या रंगहीनता शामिल हैं। जैसे-जैसे यह बढ़ता है, यह मुरझाने, गंभीर नेक्रोटिक धब्बे या फलों के सड़ने का कारण बन सकता है।",
    "treatment": "तुरंत उचित पंजीकृत उपचार लागू करें। प्रसार को सीमित करने के लिए भारी संक्रमित भागों को हटा दें और नष्ट कर दें।",
    "prevention": "फसल चक्रण का अभ्यास करें, वायु प्रवाह के लिए पौधों के बीच पर्याप्त दूरी सुनिश्चित करें, और औजारों को साफ रखें।"
}
HEALTHY_TEMPLATE_HI = {
    "summary": "आपका {plant} का पौधा स्वस्थ दिखता है और इस पर बीमारी के कोई लक्षण नहीं हैं।",
    "symptoms": "पत्तियां जीवंत, दृढ़ हैं और इनमें कोई असामान्य निशान, मुरझाहट या रंग बदलना नहीं दिख रहा है।",
    "treatment": "किसी उपचार की आवश्यकता नहीं है। नियमित रूप से पानी और उर्वरक देना जारी रखें।",
    "prevention": "लगातार पानी दें, हवा का अच्छा प्रवाह सुनिश्चित करें और कीटों की नियमित जांच करें।"
}

DISEASE_TEMPLATE_OD = {
    "summary": "{disease} ଏକ କ୍ଷତିକାରକ ରୋଗ ଯାହା {plant} ଫସଲକୁ ପ୍ରଭାବିତ କରେ, ଯାହାକି ଅଣଦେଖା କଲେ ଅମଳ ଏବଂ ଗୁଣବତ୍ତାରେ ବ୍ୟାପକ କ୍ଷତି ଘଟାଏ।",
    "symptoms": "ପ୍ରାଥମିକ ଲକ୍ଷଣଗୁଡ଼ିକ ମଧ୍ୟରେ ତଳ ପତ୍ରରେ ଛୋଟ ଦାଗ କିମ୍ବା ରଙ୍ଗ ପରିବର୍ତ୍ତନ ଅନ୍ତର୍ଭୁକ୍ତ। ଏହା ବଢ଼ିବା ସହିତ, ଶୁଖିଯିବା, ଗୁରୁତର ଦାଗ କିମ୍ବା ଫଳ ପଚିଯିବା ଦେଖାଯାଇପାରେ।",
    "treatment": "ତୁରନ୍ତ ଉପଯୁକ୍ତ ପଞ୍ଜୀକୃତ ଉପଚାର ପ୍ରୟୋଗ କରନ୍ତୁ। ବ୍ୟାପିବା ରୋକିବା ପାଇଁ ଅଧିକ ସଂକ୍ରମିତ ଅଂଶଗୁଡ଼ିକୁ କାଢ଼ି ନଷ୍ଟ କରନ୍ତୁ।",
    "prevention": "ଫସଲ ପର୍ଯ୍ୟାୟ ଅଭ୍ୟାସ କରନ୍ତୁ, ବାୟୁ ଚଳାଚଳ ପାଇଁ ଉଦ୍ଭିଦ ମଧ୍ୟରେ ପର୍ଯ୍ୟାପ୍ତ ବ୍ୟବଧାନ ରଖନ୍ତୁ ଏବଂ ଯନ୍ତ୍ରପାତି ସଫା ରଖନ୍ତୁ।"
}
HEALTHY_TEMPLATE_OD = {
    "summary": "ଆପଣଙ୍କର {plant} ଉଦ୍ଭିଦ ସୁସ୍ଥ ଦେଖାଯାଉଛି ଏବଂ ଏଥିରେ ରୋଗର କୌଣସି ଲକ୍ଷଣ ନାହିଁ।",
    "symptoms": "ପତ୍ରଗୁଡ଼ିକ ସତେଜ ଏବଂ ଦୃଢ଼ ଅଛି, ଏବଂ କୌଣସି ଅସ୍ୱାଭାବିକ ଚିହ୍ନ, ଶୁଖିବା କିମ୍ବା ରଙ୍ଗ ପରିବର୍ତ୍ତନ ଦେଖାଯାଉନାହିଁ।",
    "treatment": "କୌଣସି ଚିକିତ୍ସା ଆବଶ୍ୟକ ନାହିଁ। ନିୟମିତ ପାଣି ଏବଂ ସାର ଦେବା ଜାରି ରଖନ୍ତୁ।",
    "prevention": "ନିୟମିତ ଭାବେ ପାଣି ଦିଅନ୍ତୁ, ଭଲ ବାୟୁ ଚଳାଚଳ ସୁନିଶ୍ଚିତ କରନ୍ତୁ ଏବଂ କୀଟପତଙ୍ଗ ପାଇଁ ନିୟମିତ ଯାଞ୍ଚ କରନ୍ତୁ।"
}

def translate_dict():
    # Load JS file
    js_path = os.path.join(FRONTEND_SRC, "data", "diseaseInfo.js")
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # Extract all keys (Apple___healthy etc)
    classes = re.findall(r'"([A-Za-z_,]+___[A-Za-z_(),-]+)": \{', js_content)
    
    hi_diseaseInfo = {}
    od_diseaseInfo = {}
    hi_diseases = {}
    od_diseases = {}

    for c in classes:
        parts = c.split("___")
        plant_en = parts[0].replace("_", " ") if len(parts)>0 else "Unknown"
        disease_en = parts[1].replace("_", " ") if len(parts)>1 else "Healthy"
        
        is_healthy = "healthy" in disease_en.lower()
        
        # 1. Fill Disease names inside dicts (we'll just use English for the scientific-ish names or transliteration)
        # Since I can't live translate, I'll pass the English name into the temple as-is for the Disease,
        # but translate the Plant
        plant_hi = PLANTS_HI.get(plant_en, plant_en)
        plant_od = PLANTS_OD.get(plant_en, plant_en)
        
        if is_healthy:
            d_hi = HEALTHY_TEMPLATE_HI
            d_od = HEALTHY_TEMPLATE_OD
            dis_hi = "स्वस्थ"
            dis_od = "ସୁସ୍ଥ"
        else:
            d_hi = DISEASE_TEMPLATE_HI
            d_od = DISEASE_TEMPLATE_OD
            dis_hi = disease_en
            dis_od = disease_en

        hi_diseases[disease_en] = dis_hi
        od_diseases[disease_en] = dis_od

        hi_diseaseInfo[c] = {
            "summary": d_hi["summary"].format(plant=plant_hi, disease=disease_en),
            "symptoms": d_hi["symptoms"],
            "treatment": d_hi["treatment"],
            "prevention": d_hi["prevention"],
            "pathogen": "Data pending" if not is_healthy else "कोई नहीं",
            "spread": "हवा से फैलने वाले बीजाणु, फसल का मलबा" if not is_healthy else "लागू नहीं"
        }
        od_diseaseInfo[c] = {
            "summary": d_od["summary"].format(plant=plant_od, disease=disease_en),
            "symptoms": d_od["symptoms"],
            "treatment": d_od["treatment"],
            "prevention": d_od["prevention"],
            "pathogen": "Data pending" if not is_healthy else "କିଛି ନାହିଁ",
            "spread": "ପବନରେ ବ୍ୟାପୁଥିବା ବୀଜାଣୁ, ଫସଲର ଅବଶିଷ୍ଟାଂଶ" if not is_healthy else "ଲାଗୁ ନୁହେଁ"
        }

    # Now load hi.json and od.json, append and save
    def update_json(lang, plants, diseases, diseaseInfo):
        p = os.path.join(FRONTEND_SRC, "locales", f"{lang}.json")
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        data["plants"] = plants
        data["diseases"] = diseases
        data["diseaseInfo"] = diseaseInfo
        
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    update_json("hi", PLANTS_HI, hi_diseases, hi_diseaseInfo)
    update_json("od", PLANTS_OD, od_diseases, od_diseaseInfo)
    print("Done generating JSON translations")

if __name__ == "__main__":
    translate_dict()
