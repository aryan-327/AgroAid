import os
import json
import re

FRONTEND_SRC = r"c:\Users\aruna\OneDrive\Desktop\PROGRAMMING\Agro Aid\frontend\src"

EN_CLINICAL = {
    "fungicide": "Apply broad-spectrum organic fungicide (e.g., Copper or Sulfur based)",
    "dosage": "1.5 to 2.0 grams per liter of water",
    "method": "Foliar spray ensuring complete coverage of affected areas",
    "frequency": "Once every 7-10 days until symptoms subside",
    "safety": "Wear protective gear. Do not apply during peak sunlight or rain."
}
EN_REMEDY = {
    "cause": "Fungal spores or bacterial vectors thriving in high humidity",
    "immediate": "Prune and isolate severely infected leaves immediately",
    "environmental": "Improve air circulation; reduce overhead watering",
    "prevention": "Sanitize tools and practice proper crop spacing"
}

HI_CLINICAL = {
    "fungicide": "ब्रॉड-स्पेक्ट्रम जैविक कवकनाशी (जैसे, कॉपर या सल्फर आधारित) लागू करें",
    "dosage": "1.5 से 2.0 ग्राम प्रति लीटर पानी",
    "method": "प्रभावित क्षेत्रों की पूर्ण कवरेज सुनिश्चित करते हुए पर्ण छिड़काव करें",
    "frequency": "लक्षण कम होने तक हर 7-10 दिनों में एक बार",
    "safety": "सुरक्षात्मक गियर पहनें। तेज धूप या बारिश के दौरान न लगाएं।"
}
HI_REMEDY = {
    "cause": "उच्च आर्द्रता में पनपने वाले फंगल बीजाणु या बैक्टीरियल वैक्टर",
    "immediate": "गंभीर रूप से संक्रमित पत्तियों को तुरंत काटें और अलग करें",
    "environmental": "वायु संचार में सुधार करें; ऊपर से पानी देना कम करें",
    "prevention": "औजारों को साफ करें और उचित फसल अंतर का अभ्यास करें"
}

OD_CLINICAL = {
    "fungicide": "ବ୍ରଡ୍-ସ୍ପେକ୍ଟ୍ରମ୍ ଜୈବିକ କବକନାଶକ ପ୍ରୟୋଗ କରନ୍ତୁ",
    "dosage": "ପ୍ରତି ଲିଟର ପାଣିରେ ୧.୫ ରୁ ୨.୦ ଗ୍ରାମ୍",
    "method": "ପ୍ରଭାବିତ ଅଂଶରେ ସମ୍ପୂର୍ଣ୍ଣ ସ୍ପ୍ରେ କରନ୍ତୁ",
    "frequency": "ଲକ୍ଷଣ ନ କମିବା ପର୍ଯ୍ୟନ୍ତ ପ୍ରତି ୭-୧୦ ଦିନରେ ଥରେ",
    "safety": "ସୁରକ୍ଷା ପୋଷାକ ପିନ୍ଧନ୍ତୁ। ଅତ୍ୟଧିକ ଖରାରେ ପ୍ରୟୋଗ କରନ୍ତୁ ନାହିଁ।"
}
OD_REMEDY = {
    "cause": "ଅଧିକ ଆର୍ଦ୍ରତାରେ ବଢୁଥିବା ଫିମ୍ପି କିମ୍ବା ବ୍ୟାକ୍ଟେରିଆ",
    "immediate": "ଅଧିକ ସଂକ୍ରମିତ ପତ୍ରଗୁଡ଼ିକୁ ତୁରନ୍ତ କାଟି ଅଲଗା କରନ୍ତୁ",
    "environmental": "ବାୟୁ ଚଳାଚଳରେ ଉନ୍ନତି କରନ୍ତୁ; ଉପରୁ ପାଣି ଦେବା କମାନ୍ତୁ",
    "prevention": "ଯନ୍ତ୍ରପାତି ସଫା କରନ୍ତୁ ଏବଂ ଉପଯୁକ୍ତ ଗଛ ବ୍ୟବଧାନ ରଖନ୍ତୁ"
}

def update_dictionaries():
    # Load JS file to get 38 classes
    js_path = os.path.join(FRONTEND_SRC, "data", "diseaseInfo.js")
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    classes = re.findall(r'"([A-Za-z_,]+___[A-Za-z_(),-]+)": \{', js_content)

    def process_lang(lang, clinical_tpl, remedy_tpl):
        p = os.path.join(FRONTEND_SRC, "locales", f"{lang}.json")
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Ensure diseaseInfo exists
        if "diseaseInfo" not in data:
            data["diseaseInfo"] = {}
            
        for c in classes:
            is_healthy = "healthy" in c.lower()
            if c not in data["diseaseInfo"]:
                data["diseaseInfo"][c] = {}
                
            if not is_healthy:
                data["diseaseInfo"][c]["clinical"] = clinical_tpl
                data["diseaseInfo"][c]["remedy"] = remedy_tpl
            else:
                data["diseaseInfo"][c]["clinical"] = {}
                data["diseaseInfo"][c]["remedy"] = {}

        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    process_lang("en", EN_CLINICAL, EN_REMEDY)
    process_lang("hi", HI_CLINICAL, HI_REMEDY)
    process_lang("od", OD_CLINICAL, OD_REMEDY)
    print("Successfully populated clinical & remedy nodes.")

if __name__ == "__main__":
    update_dictionaries()
