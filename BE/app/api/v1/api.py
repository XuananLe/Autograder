from fastapi import APIRouter
from app.api.v1.endpoints import exams, submissions, students,upload

api_router = APIRouter()

api_router.include_router(exams.router, prefix="/exams", tags=["exams"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["submissions"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])