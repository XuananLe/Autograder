from beanie import Document, Indexed
from typing import Optional


class Student(Document):
    student_code: str = Indexed(unique=True) # Đảm bảo mã SV không trùng
    full_name: str
    email: Optional[str] = None

    class Settings:
        name = "students"