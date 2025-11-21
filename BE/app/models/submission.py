from datetime import datetime
from beanie import Document, PydanticObjectId, Indexed
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any

class GradeDetail(BaseModel):
    question_id: str
    score: float
    feedback: str

class Submission(Document):
    exam_id: PydanticObjectId = Indexed()
    student_id: str = Indexed() # Mã SV (VD: 23021668)
    student_name: str
    student_email: Optional[str] = None
    
    # File bài làm
    file_url: Optional[str] = None
    submission_type: str = "upload" # upload, typed
    
    # Trạng thái xử lý
    status: str = "pending" # pending, processing, processed, graded
    
    # Kết quả OCR (Answers Tab)
    ocr_data: Dict[str, Any] = {} # { "q1_text": "...", "q1_latex": "..." }
    
    # Kết quả Chấm điểm (Grading Tab)
    total_score: Optional[float] = None
    grades: List[GradeDetail] = []
    general_feedback: Optional[str] = None
    
    submitted_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "submissions"