import shutil
import os
import sys
import json
from typing import List
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

# Add parent directory to path to import decision_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decision_engine import analyze_image
from backend.database import create_db_and_tables, get_session
from backend.models import AnalysisResult

app = FastAPI()

# Input/Output Directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads for static access
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/analyze")
async def analyze_uploaded_image(
    file: UploadFile = File(...), session: Session = Depends(get_session)
):
    try:
        # 1. Save File
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Run Analysis
        # analyze_image returns a JSON string
        result_json_str = analyze_image(file_path)
        
        try:
            # Clean possible markdown formatting from LLM
            clean_json_str = result_json_str.strip()
            if clean_json_str.startswith("```json"):
                clean_json_str = clean_json_str[7:]
            if clean_json_str.startswith("```"):
                clean_json_str = clean_json_str[3:]
            if clean_json_str.endswith("```"):
                clean_json_str = clean_json_str[:-3]
            
            result_data = json.loads(clean_json_str)
        except json.JSONDecodeError:
             return {"status": "error", "message": "Failed to decode AI response", "raw": result_json_str}

        # 3. Extract Fields
        # The structure from decision_engine:
        # {
        #   "request": { "id": ... },
        #   "type": { "ai_generated": float },
        #   "Final Result": "...",
        #   "forensic_summary": "..."
        # }
        
        ai_score = result_data.get("type", {}).get("ai_generated", 0.0)
        final_result = result_data.get("Final Result", "Unknown")
        summary = result_data.get("forensic_summary", "")
        req_id = result_data.get("request", {}).get("id", "")

        # 4. Save to DB
        analysis_entry = AnalysisResult(
            filename=file.filename,
            ai_generated_score=ai_score,
            final_result=final_result,
            forensic_summary=summary,
            request_id=req_id
        )
        session.add(analysis_entry)
        session.commit()
        session.refresh(analysis_entry)

        return {
            "status": "success",
            "data": result_data,
            "db_entry": analysis_entry
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/gallery/real", response_model=List[AnalysisResult])
def get_real_gallery(session: Session = Depends(get_session)):
    statement = select(AnalysisResult).where(AnalysisResult.final_result == "Real")
    results = session.exec(statement).all()
    return results


@app.get("/gallery/review", response_model=List[AnalysisResult])
def get_review_gallery(session: Session = Depends(get_session)):
    statement = select(AnalysisResult).where(AnalysisResult.final_result == "AI Edited")
    results = session.exec(statement).all()
    return results
