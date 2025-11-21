# app/models/exam.py
from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

# --- Sub-models cho Rubric (Giữ nguyên) ---
class RubricStep(BaseModel):
    id: str
    title: str
    marks: float
    content: Dict[str, str] = {
        "solution": "", 
        "expectation": "", 
        "common_errors": "", 
        "marking": ""
    }

class Question(BaseModel):
    id: str
    title: str
    marks: float
    description: Optional[str] = ""
    steps: List[RubricStep] = []

# --- Model Chính (ĐÃ SỬA) ---
class Exam(Document):
    title: str = "New Exam"
    
    # Đổi course_name -> course_title để khớp với Schema
    course_title: Optional[str] = None 
    
    # Các trường bổ sung từ Tab Info
    institute: Optional[str] = None
    department: Optional[str] = None
    course_level: Optional[str] = None
    subject: Optional[str] = None
    
    # Lưu ý kiểu dữ liệu: Schema bạn để date là str, due_date là datetime
    date: Optional[str] = None 
    due_date: Optional[datetime] = None
    
    status: str = "draft"
    questions: List[Question] = []
    
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "exams"