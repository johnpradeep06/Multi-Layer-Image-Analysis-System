# ML Pipeline Application - Setup Guide

This guide will help you run the newly created backend and frontend for your Forensic Image Analysis system.

## 1. Backend Setup

The backend is built with FastAPI and handles image analysis and database storage.

### Prerequisites
Make sure you are in the root directory: `c:\Users\cyril\PSG`

### Installation
Install the required Python packages (if you haven't already):
```bash
pip install fastapi uvicorn sqlmodel python-multipart pillow numpy opencv-python openai python-dotenv
```

### Running the Server
Run the backend using `uvicorn` from the root directory to ensure all imports work correctly:

```bash
python -m uvicorn backend.main:app --reload
```

- The API will be available at: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Uploaded images will be saved to: `PSG/uploads/`
- Database file: `PSG/database.db` (created automatically on first run)

## 2. Frontend Setup

The frontend is a Vite + React application styled with TailwindCSS.

### Installation
Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

### Running the Application
Start the development server:

```bash
npm run dev
```

- Open your browser to: `http://localhost:5173`

## 3. How to Use

1. **Upload an Image**:
   - Go to the local frontend URL.
   - Drag & drop an image or click to select.
   - Click "Start Analysis".

2. **Analysis Flow**:
   - The system will show a forensic analysis animation.
   - The backend runs `decision_engine.py` (GenAI, Frequency, ELA, Metadata).
   - An LLM verdict is generated.

3. **Results**:
   - **Real Images**: Marked "UPLOAD SUCCESSFUL" and added to the **Public Gallery**.
   - **AI Edited**: Marked "UNDER REVIEW" and added to the **Review Gallery**.
   - **AI Generated**: Marked "UPLOAD BLOCKED".

4. **Gallery**:
   - Scroll down to see the gallery.
   - Switch tabs between "VERIFIED REAL" and "UNDER REVIEW".
