from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from app.models.submission import Submission
from app.schemas.submission import SubmissionResponse, StudentLink
from beanie import PydanticObjectId
import shutil # Dùng tạm để lưu file local

router = APIRouter()

# 1. [Answers Tab] Upload File & Link Student (Add Roster)
@router.post("/{exam_id}/students", response_model=SubmissionResponse)
async def add_student_submission(
    exam_id: PydanticObjectId, 
    student_data: StudentLink
):
    # Kiểm tra xem SV này đã có trong exam chưa
    existing = await Submission.find_one(
        Submission.exam_id == exam_id,
        Submission.student_id == student_data.student_id
    )
    
    if existing:
        raise HTTPException(400, "Student already in roster")

    new_sub = Submission(
        exam_id=exam_id,
        student_id=student_data.student_id,
        student_name=student_data.name,
        student_email=student_data.email,
        file_url=student_data.file_url
    )
    await new_sub.insert()
    return new_sub

# 2. [Answers Tab] Upload File PDF (Helper API)
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Lưu file vào folder 'static' hoặc đẩy lên S3
    file_location = f"static/{file.filename}"
    with open(file_location, "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "url": file_location}

# 3. [Answers Tab] Lấy danh sách lớp (Roster)
@router.get("/{exam_id}/roster", response_model=List[SubmissionResponse])
async def get_roster(exam_id: PydanticObjectId):
    submissions = await Submission.find(Submission.exam_id == exam_id).to_list()
    return submissions

# 4. [Answers Tab] Trigger Xử lý bài làm (OCR)
@router.post("/{exam_id}/process-answers")
async def process_answers(exam_id: PydanticObjectId):
    # 1. Lấy tất cả submission của exam
    subs = await Submission.find(Submission.exam_id == exam_id).to_list()
    
    # 2. Gửi task cho Celery/Background Worker (Mocking loop)
    for sub in subs:
        sub.status = "processed"
        # Giả lập data OCR
        sub.ocr_data = {
            "question_1_text": "Student Answer Text...",
            "question_1_latex": "x^2 + y^2 = z^2"
        }
        await sub.save()
        
    return {"message": "Processing started", "count": len(subs)}

# 5. [Grading Tab] Trigger Chấm điểm (Grading)
@router.post("/{exam_id}/grade")
async def grade_exam(exam_id: PydanticObjectId):
    subs = await Submission.find(Submission.exam_id == exam_id).to_list()
    
    # Giả lập chấm điểm
    for sub in subs:
        sub.status = "graded"
        sub.total_score = 8.5
        sub.general_feedback = "Good job!"
        await sub.save()
        
    return {"message": "Grading complete"}

# 6. [Student Dashboard] Lấy danh sách bài thi của 1 SV
@router.get("/student/{student_id}/exams")
async def get_student_exams(student_id: str):
    # Logic: Tìm các submission của SV này, sau đó join với bảng Exam để lấy Title/Due Date
    submissions = await Submission.find(Submission.student_id == student_id).to_list()
    
    results = []
    for sub in submissions:
        # Fetch exam info (Beanie support fetch link manually usually)
        from app.models.exam import Exam 
        exam = await Exam.get(sub.exam_id)
        if exam:
            results.append({
                "exam_title": exam.title,
                "course": exam.course_name,
                "due_date": exam.due_date,
                "status": sub.status, # Unfinished/Graded
                "score": sub.total_score,
                "submission_id": str(sub.id),
                "exam_id": str(exam.id)
            })
    return results