from fastapi import APIRouter, HTTPException
from typing import List
from beanie.operators import RegEx # Dùng để tìm kiếm gần đúng (Like %...%)

from app.models.student import Student
from pydantic import BaseModel

router = APIRouter()

# Schema trả về gọn nhẹ cho search
class StudentSearchResponse(BaseModel):
    student_code: str
    full_name: str
    email: str | None = None

@router.get("/search", response_model=List[StudentSearchResponse])
async def search_students(q: str):
    """
    Tìm kiếm sinh viên theo Tên hoặc Mã SV.
    Dùng Regex để tìm không phân biệt hoa thường ('i').
    """
    if not q:
        return []
    
    # Tìm trong DB: Hoặc trùng Tên, Hoặc trùng Mã
    students = await Student.find(
        RegEx(Student.full_name, q, "i") | RegEx(Student.student_code, q, "i")
    ).limit(20).to_list()
    
    return students

# API tạo sinh viên mới (nếu chưa có) để test
@router.post("/", response_model=StudentSearchResponse)
async def create_student(student: Student):
    # Kiểm tra trùng
    exists = await Student.find_one(Student.student_code == student.student_code)
    if exists:
        raise HTTPException(400, "Student ID already exists")
    await student.insert()
    return student