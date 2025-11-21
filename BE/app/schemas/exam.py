# app/schemas/exam.py
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from beanie import PydanticObjectId

# --- Shared Sub-schemas ---
class RubricStepUpdate(BaseModel):
    id: str
    title: str
    marks: float
    content: Dict[str, str]

class QuestionUpdate(BaseModel):
    id: str
    title: str
    marks: float
    description: Optional[str] = None # Nên để default là None
    steps: List[RubricStepUpdate] = []

# --- Exam Schemas ---
class ExamCreate(BaseModel):
    title: str

class ExamInfoUpdate(BaseModel):
    institute: Optional[str] = None
    department: Optional[str] = None
    course_title: Optional[str] = None
    course_level: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None
    due_date: Optional[datetime] = None

class ExamRubricUpdate(BaseModel):
    questions: List[QuestionUpdate]

# --- Response Schema (ĐÃ KHỚP VỚI MODEL) ---
class ExamResponse(BaseModel):
    id: PydanticObjectId
    title: str
    
    course_title: Optional[str] = None
    institute: Optional[str] = None
    department: Optional[str] = None
    course_level: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None
    due_date: Optional[datetime] = None
    
    status: str
    questions: List[QuestionUpdate] = []
    created_at: datetime
    
    class Config:
        from_attributes = True