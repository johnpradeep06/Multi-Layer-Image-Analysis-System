from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class AnalysisResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Forensic Data
    ai_generated_score: float
    final_result: str  # "AI Generated", "AI Edited", "Real"
    forensic_summary: str
    
    # Details from JSON
    request_id: Optional[str] = None
    
