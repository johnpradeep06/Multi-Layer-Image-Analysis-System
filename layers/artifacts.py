import numpy as np
from PIL import Image
import cv2

def compute_frequency_score(image_path):
    """
    Returns frequency-based risk score (0–100)
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (256, 256))

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log(np.abs(fshift) + 1)

    mean_spectrum = np.mean(magnitude_spectrum)
    std_spectrum = np.std(magnitude_spectrum)

    # Heuristic GAN fingerprint detection
    anomaly_score = std_spectrum

    # Normalize to risk

    
    # Normalize to risk (0-100) -> (0.0 - 1.0)
    # The original logic had risk = 90 (0.9), 75 (0.75), 20 (0.2)
    
    if anomaly_score > 1.1 :
        risk = 0.90
    elif 0.9 <= anomaly_score <= 1.1:
        risk = 0.75
    elif anomaly_score < 0.9:
        risk = 0.20
    
    return {
        "tool_name": "frequency_analysis",
        "status": "success",
        "score": float(risk),
        "details": {
            "anomaly_score": float(anomaly_score),
            "mean_spectrum": float(mean_spectrum),
            "std_spectrum": float(std_spectrum)
        }
    }

if __name__ == "__main__":
    freq_score  =  compute_frequency_score("../../test8.jpeg")
    print(freq_score)
