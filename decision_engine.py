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

# --------------------------------------------------
# Setup
# --------------------------------------------------

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# --------------------------------------------------
# Utility: Encode Image
# --------------------------------------------------

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# --------------------------------------------------
# Main Analysis Pipeline
# --------------------------------------------------

def analyze_image(image_path):
    print(f"\nAnalyzing {image_path}...\n")

    # Run all forensic layers
    genai_result = analyze_genai(image_path)
    freq_result = compute_frequency_score(image_path)
    ela_result = compute_ela_score(image_path)
    meta_result = compute_metadata_score(image_path)

    layer_outputs = {
        "genai_detection": genai_result,
        "frequency_analysis": freq_result,
        "ela_analysis": ela_result,
        "metadata_analysis": meta_result
    }

    # Get final LLM decision
    return llm_decision_layer(image_path, layer_outputs)

# --------------------------------------------------
# LLM Decision Layer (Optimized)
# --------------------------------------------------

def llm_decision_layer(image_path, layer_outputs):

    base64_image = encode_image(image_path)

    # Extract only summary scores (keep it efficient)
    ai_score = layer_outputs['genai_detection']['score']
    freq_score = layer_outputs['frequency_analysis']['score']
    ela_score = layer_outputs['ela_analysis']['score']
    meta_score = layer_outputs['metadata_analysis']['score']

    prompt = f"""
You are a digital image forensic expert.

You have received 4 forensic risk scores (0.0 = Real/Low Risk, 1.0 = Fake/High Risk):

GenAI Detection Score: {ai_score}
Frequency Artifact Score: {freq_score}
ELA Score: {ela_score}
Metadata Risk Score: {meta_score}

Instructions:
- Analyze the image visually.
- Correlate with the risk scores.
- Look for synthetic artifacts, deepfake traces, unnatural lighting, or inconsistencies.
- If GenAI score is very high (>0.9), image is likely AI generated.
- If metadata moderate and artifacts have high scores and GenAI score is low, it may be AI edited, not generated.
- If the Metadata score is 0.05 straightly conlcude it is Real.
- Apart from this if something is off in the image you can conclude based on your own analysis to


Return ONLY valid JSON in this format:

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
  "forensic_summary": "Write a concise forensic justification in 2-3 sentences. Highlight only the strongest visual indicator of manipulation (e.g., lighting inconsistency, unnatural texture, blending artifacts). Avoid mentioning scores, probabilities, or internal analysis metrics.",
  "Final Result": "AI Generated / AI Edited / Real"
}}

Do not return anything except JSON.
"""

    completion = client.chat.completions.create(
        model="qwen/qwen3-vl-235b-a22b-thinking",
        temperature=0.2,
        max_tokens=392,
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

# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":

    test_image = "assests/test5.png"

    if os.path.exists(test_image):

        result = analyze_image(test_image)

        # Try to parse and pretty print JSON
        try:
            parsed_result = json.loads(result)

            print("===== FINAL FORENSIC VERDICT =====\n")
            print("AI Generated Score :", parsed_result["type"]["ai_generated"])
            print("Final Result       :", parsed_result["Final Result"])
            print("Reasoning          :", parsed_result["forensic_summary"])
            print("\nFull JSON Output:\n")
            print(json.dumps(parsed_result, indent=4))

        except json.JSONDecodeError:
            print("LLM did not return valid JSON:")
            print(result)

    else:
        print(f"Test image not found at {test_image}")