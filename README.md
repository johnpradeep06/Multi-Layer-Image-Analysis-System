# Multi-Layer Forensic Image Analysis System

## Overview

This project is a sophisticated digital image forensic tool designed to detect deepfakes and manipulated images. It employs a multi-layered approach, combining traditional forensic techniques with modern AI-based detection, and culminates in a final decision made by a Large Language Model (LLM).

The system aggregates analysis from four distinct layers:
1.  **GenAI Detection**: Identifying traces of generative AI models.
2.  **Frequency Analysis**: Detecting anomalies in the frequency domain (e.g., GAN fingerprints).
3.  **Error Level Analysis (ELA)**: Highlighting compression inconsistencies indicative of editing.
4.  **Metadata Analysis**: Examining EXIF data for software signatures and camera information.

An LLM then acts as a "Forensic Expert," synthesizing these reports to provide a final verdict and a human-readable explanation.

## Features

-   **Multi-Model Analysis**: Robust detection by cross-referencing multiple forensic methods.
-   **GenAI Detection Layer**: Uses Sightengine API to detect AI-generated content.
-   **Frequency Analysis Layer**: Uses FFT (Fast Fourier Transform) to analyze image spectrums.
-   **ELA Layer**: Performs Error Level Analysis to detect pixel-level manipulations.
-   **Metadata Layer**: Extracts and analyzes EXIF tags for suspicious software traces (e.g., Photoshop).
-   **LLM Decision Engine**: OpenAI/OpenRouter integration to interpret technical data and generate a natural language report.

## Directory Structure

```
├── decision_engine.py      # Main entry point and LLM decision logic
├── layers/                 # Analytic modules
│   ├── analyse_image.py    # GenAI Detection (Sightengine)
│   ├── artifacts.py        # Frequency Analysis
│   ├── ela.py              # Error Level Analysis
│   └── metadata.py         # Metadata/EXIF Analysis
├── assests/                # Test images
├── requirements.txt        # Python dependencies
└── .env                    # Configuration credentials
```

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory.
2.  Add your API keys for OpenRouter (LLM) and Sightengine (GenAI detection):

```env
OPENROUTER_API_KEY=your_openrouter_api_key
SIGHTENGINE_API_USER=your_sightengine_api_user
SIGHTENGINE_API_SECRET=your_sightengine_api_secret
```

## Usage

To analyze an image, run the `decision_engine.py` script. You can modify the `test_image` variable in the `__main__` block to point to your target image.

```bash
python decision_engine.py
```

### Example Usage in Code

```python
from decision_engine import analyze_image

# Path to the image you want to analyze
image_path = "assests/test_image.jpg"

# Run analysis
result = analyze_image(image_path)

# Print the JSON result
print(result)
```

## Output Format

The system returns a JSON object containing the analysis results:

```json
{
  "status": "success",
  "request": {
      "id": "generated_id",
      "timestamp": 123456789,
      "operations": 4
  },
  "type": {
      "ai_generated": 0.95
  },
  "media": {
      "uri": "test_image.jpg"
  },
  "forensic_summary": "The image shows strong indicators of being AI-generated..."
}
```
