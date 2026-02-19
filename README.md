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
-   **Full Stack Application**:
    -   **Backend**: FastAPI server for handling uploads and analysis.
    -   **Frontend**: React (Vite) application with a modern forensic dashboard.
    -   **Gallery**: automatic categorization of images into "Real" and "Under Review".

## Directory Structure

```
├── backend/                # FastAPI Application
│   ├── main.py             # API Endpoints
│   ├── models.py           # Database Models
│   └── database.py         # DB Connection
├── frontend/               # React Application (Vite)
├── decision_engine.py      # Core Analysis Logic
├── layers/                 # Analytic Modules
├── assests/                # Test Images
├── requirements.txt        # Python Dependencies
└── .env                    # Configuration
```

## Installation & Setup

### 1. Clone the repository
```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Backend Setup (Termina 1)

Create a virtual environment and install dependencies:

```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate
# Activate venv (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Configuration**:
1.  Create a `.env` file in the root directory.
2.  Add your API keys:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
SIGHTENGINE_API_USER=your_sightengine_api_user
SIGHTENGINE_API_SECRET=your_sightengine_api_secret
```

**Run the Backend**:
```bash
python -m uvicorn backend.main:app --reload
```
The API will start at `http://localhost:8000`.

### 3. Frontend Setup (Terminal 2)

Navigate to the frontend directory and install Node.js dependencies:

```bash
cd frontend
npm install
```

**Run the Frontend**:
```bash
npm run dev
```
The application will be available at `http://localhost:5173`.

## Usage

1.  Open the frontend URL (`http://localhost:5173`).
2.  **Upload an Image**: Drag & drop or select an image.
3.  **View Analysis**: Watch the forensic analysis steps (Pixels, Metadata, CFA, GenAI).
4.  **See Verdict**:
    -   **Real**: Image is added to the Public Gallery.
    -   **Under Review**: Image had some editing traces (e.g. Photoshop metadata) and is added to the Review Gallery.
    -   **Blocked**: Image is high-confidence AI genrated.

## API Documentation

-   Swagger UI: `http://localhost:8000/docs`
-   ReDoc: `http://localhost:8000/redoc`
