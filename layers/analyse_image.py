import os
from dotenv import load_dotenv
import requests
import json
load_dotenv()

def analyze_genai(image_path):
    params = {
        'models': 'genai',
        'api_user': os.getenv("SIGHTENGINE_API_USER"),
        'api_secret': os.getenv("SIGHTENGINE_API_SECRET")
    }
    
    try:
        with open(image_path, 'rb') as img_file:
            files = {'media': img_file}
            r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
            
        output = json.loads(r.text)
        
        # Standardize Output
        # Extract ai_generated confidence if available, else default to 0
        ai_score = output.get('type', {}).get('ai_generated', 0)
        
        return {
            "tool_name": "sightengine_genai",
            "status": "success",
            "score": float(ai_score), # 0.0 to 1.0
            "details": output
        }
    except Exception as e:
        return {
            "tool_name": "sightengine_genai",
            "status": "error",
            "score": 0.0,
            "details": {"error": str(e)}
        }

if __name__ == "__main__":
    # Test
    print(analyze_genai(os.path.abspath("../assests/aswin.png")))
