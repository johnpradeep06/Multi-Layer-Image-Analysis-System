from openai import OpenAI
import os
import base64
import json
from dotenv import load_dotenv

# Import Layer Functions
from layers.analyse_image import analyze_genai
from layers.artifacts import compute_frequency_score
from layers.ela import compute_ela_score
from layers.metadata import compute_metadata_score

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def analyze_image(image_path):
    print(f"Analyzing {image_path}...")
    
    # 1. Run all layers
    genai_result = analyze_genai(image_path)
    freq_result = compute_frequency_score(image_path)
    ela_result = compute_ela_score(image_path)
    meta_result = compute_metadata_score(image_path)
    
    # 2. Aggregate scores for context
    # Note: We pass the full detailed JSON to the LLM
    
    layer_outputs = {
        "genai_detection": genai_result,
        "frequency_analysis": freq_result,
        "ela_analysis": ela_result,
        "metadata_analysis": meta_result
    }
    
    # 3. Get LLM Decision
    final_decision = llm_decision_layer(image_path, layer_outputs)
    
    return final_decision

def llm_decision_layer(image_path, layer_outputs):

    base64_image = encode_image(image_path)
    
    # Extract summary scores for prompt readability (optional, but good for chain-of-thought)
    ai_score = layer_outputs['genai_detection']['score']
    freq_score = layer_outputs['frequency_analysis']['score']
    ela_score = layer_outputs['ela_analysis']['score']
    meta_score = layer_outputs['metadata_analysis']['score']

    prompt = f"""
You are a digital image forensic expert.

You have received analysis reports from 4 different forensic layers:

1. **GenAI Detection Model**:
   - Score: {ai_score} (0.0=Real, 1.0=Fake)
   - Full Report: {json.dumps(layer_outputs['genai_detection']['details'])}

2. **Frequency Analysis (Artifacts)**:
   - Score: {freq_score} (0.0=Low Risk, 1.0=High Risk)
   - Full Report: {json.dumps(layer_outputs['frequency_analysis']['details'])}

3. **Error Level Analysis (ELA)**:
   - Score: {ela_score} (0.0=Low Risk, 1.0=High Risk)
   - Full Report: {json.dumps(layer_outputs['ela_analysis']['details'])}

4. **Metadata Analysis**:
   - Score: {meta_score} (0.0=Low Risk, 1.0=High Risk)
   - Full Report: {json.dumps(layer_outputs['metadata_analysis']['details'])}

Task:
- Analyze the image visually (you are given the image).
- Correlate your visual findings with the layer reports above.
- Look for synthetic artifacts, inconsistencies, deepfake traces, unnatural lighting, etc.
- If the GenAI model says 99% fake, it's likely fake.
- If Metadata shows "Photoshop" but other scores are low, it might be just edited, not generated.

You MUST return ONLY valid JSON in this format:

{{
  "status": "success",
  "request": {{
      "id": "generated_id", 
      "timestamp": 123456789,
      "operations": 4
  }},
  "type": {{
      "ai_generated": float_between_0_and_1
  }},
  "media": {{
      "uri": "{os.path.basename(image_path)}"
  }},
  "forensic_summary": "short technical reasoning explaining the verdict"
}}

Do not return anything except JSON.
"""

    completion = client.chat.completions.create(
        model="openai/gpt-4o",
        temperature=0.2,
        max_tokens=600,
        messages=[
            {
                "role": "system",
                "content": "You are a strict forensic AI classifier. Output only JSON."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    # Example usage
    # Ensure you have a test image at this path or update it
    test_image = "assests/test10.png" 
    if os.path.exists(test_image):
        result = analyze_image(test_image)
        print(result)
    else:
        print(f"Test image not found at {test_image}")
