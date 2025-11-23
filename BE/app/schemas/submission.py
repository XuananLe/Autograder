from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from beanie import PydanticObjectId

class StudentLink(BaseModel):
    student_id: str
    name: str
    email: str
    file_url: Optional[str] = None

class SubmissionResponse(BaseModel):
    id: PydanticObjectId
    exam_id: PydanticObjectId
    student_id: str
    student_name: str
    file_url: Optional[str]
    status: str
    total_score: Optional[float]
    
class StudentExamResponse(BaseModel):
    exam_id: str
    submission_id: str
    title: str
    course_name: str
    due_date: Optional[datetime]
    status: str # Unfinished, finished, graded
    score: Optional[float] = None
    feedback: Optional[str] = None
    file_url: Optional[str] = None