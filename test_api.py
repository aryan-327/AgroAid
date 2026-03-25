import requests
import sys
import os

def test_api():
    url = "http://localhost:5000/api/predict"
    
    # Create a dummy image
    image_path = "test_image.jpg"
    try:
        from PIL import Image
        img = Image.new('RGB', (224, 224), color = 'red')
        img.save(image_path)
    except Exception as e:
        print("Could not create test image:", e)
        return

    try:
        with open(image_path, "rb") as f:
            files = {"file": ("test_image.jpg", f, "image/jpeg")}
            print(f"Sending POST to {url}...")
            response = requests.post(url, files=files)
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    test_api()
