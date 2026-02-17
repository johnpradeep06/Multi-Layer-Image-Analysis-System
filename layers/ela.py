from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import io

def compute_ela_score(image_path, quality=90):
    """
    Returns ELA-based risk score (0–100)
    """

    original = Image.open(image_path).convert("RGB")

    # Save compressed version in memory
    buffer = io.BytesIO()
    original.save(buffer, 'JPEG', quality=quality)
    buffer.seek(0)
    compressed = Image.open(buffer)

    # Difference
    ela_image = ImageChops.difference(original, compressed)

    # Convert to numpy
    ela_array = np.array(ela_image)

    mean_brightness = np.mean(ela_array)

    # Normalize to risk
    # You may tune this scaling

    # Normalize to risk (0-100) -> (0.0 - 1.0)
    if mean_brightness < 5:
        risk = 0.15
    elif mean_brightness < 15:
        risk = 0.40
    elif mean_brightness < 30:
        risk = 0.65
    else:
        risk = 0.85

    return {
        "tool_name": "ela_analysis",
        "status": "success",
        "score": float(risk),
        "details": {
            "mean_brightness": float(mean_brightness)
        }
    }

if __name__ == "__main__":
    ela_score = compute_ela_score("../assests/test8.jpeg")
    print(ela_score)
