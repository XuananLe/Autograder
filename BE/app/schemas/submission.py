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