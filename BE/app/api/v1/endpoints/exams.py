from fastapi import APIRouter, HTTPException
from typing import List, Optional
from beanie import PydanticObjectId
from pydantic import BaseModel

# Import các Models từ Beanie
from app.models.exam import Exam, Question, RubricStep
# Import Schemas
from app.schemas.exam import ExamCreate, ExamResponse, ExamInfoUpdate, ExamRubricUpdate

router = APIRouter()

# --- 1. CRUD CƠ BẢN ---

@router.post("/", response_model=ExamResponse)
async def create_exam(exam_in: ExamCreate):
    """Tạo Exam mới (Draft)"""
    new_exam = Exam(title=exam_in.title)
    await new_exam.insert()
    return new_exam

@router.get("/", response_model=List[ExamResponse])
async def get_exams():
    """Lấy danh sách tất cả Exam"""
    return await Exam.find_all().sort("-created_at").to_list()

@router.get("/{exam_id}", response_model=ExamResponse)
async def get_exam_detail(exam_id: PydanticObjectId):
    """Lấy chi tiết 1 Exam"""
    exam = await Exam.get(exam_id)
    if not exam:
        raise HTTPException(404, "Exam not found")
    return exam

@router.put("/{exam_id}/info", response_model=ExamResponse)
async def update_exam_info(exam_id: PydanticObjectId, info: ExamInfoUpdate):
    """Cập nhật Tab Info"""
    exam = await Exam.get(exam_id)
    if not exam:
        raise HTTPException(404, "Exam not found")
    
    update_data = info.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(exam, key, value)
        
    await exam.save()
    return exam

@router.put("/{exam_id}/rubric", response_model=ExamResponse)
async def update_rubric(exam_id: PydanticObjectId, rubric_data: ExamRubricUpdate):
    """Lưu thủ công Rubric (khi user sửa trên UI)"""
    exam = await Exam.get(exam_id)
    if not exam:
        raise HTTPException(404, "Exam not found")
    
    # Convert Schema -> Model
    new_questions = []
    for q in rubric_data.questions:
        # Chuyển đổi từng QuestionUpdate thành Question Model
        steps_model = []
        for s in q.steps:
            steps_model.append(RubricStep(**s.model_dump()))
            
        q_model = Question(
            id=q.id,
            title=q.title,
            marks=q.marks,
            description=q.description,
            steps=steps_model
        )
        new_questions.append(q_model)
        
    exam.questions = new_questions
    await exam.save()
    return exam

# --- 2. LOGIC XỬ LÝ AI (QUAN TRỌNG: Đây là chỗ bạn đang thiếu/lỗi) ---

# Schema riêng cho request xử lý (Body nhận từ Frontend)
class RubricProcessRequest(BaseModel):
    submission_type: Optional[str] = None
    ocr_method: Optional[str] = None
    gpt_model: Optional[str] = None
    detail_level: Optional[str] = None

@router.post("/{exam_id}/rubric/process")
async def process_exam_rubric(exam_id: PydanticObjectId, payload: RubricProcessRequest):
    """
    Endpoint giả lập quá trình AI trích xuất Rubric.
    Thay vì Frontend mock, SERVER sẽ tự tạo dữ liệu và lưu vào Database.
    """
    exam = await Exam.get(exam_id)
    if not exam:
        raise HTTPException(404, "Exam not found")

    print(f"🤖 Processing Exam {exam_id} with options: {payload}")

    # --- SERVER-SIDE GENERATION LOGIC ---
    # Tại đây bạn sẽ gọi OpenAI / Azure Document Intelligence.
    # Hiện tại mình sẽ tạo dữ liệu mẫu "Cứng" ở Server để đảm bảo không bao giờ lỗi.
    
    generated_questions = [
        Question(
            id="q1",
            title="Question 1: FitzHugh-Nagumo Model",
            marks=20.0,
            description="Analyze the differential equations provided in the document.",
            steps=[
                RubricStep(
                    id="s1-1",
                    title="Identify Equations",
                    marks=10.0,
                    content={
                        "solution": "dv/dt = f(v) - w + I_a",
                        "expectation": "Student must write the correct diff equation.",
                        "common_errors": "Missing I_a term.",
                        "marking": "10 marks for full equation."
                    }
                ),
                RubricStep(
                    id="s1-2",
                    title="Piecewise Function f(v)",
                    marks=10.0,
                    content={
                        "solution": "f(v) has 3 parts...",
                        "expectation": "Define all 3 ranges correctly.",
                        "common_errors": "Wrong boundaries.",
                        "marking": "3.3 marks per correct range."
                    }
                )
            ]
        ),
        Question(
            id="q2",
            title="Question 2: Parameter Analysis",
            marks=15.0,
            description="Explain the significance of parameter b in the model.",
            steps=[
                RubricStep(
                    id="s2-1",
                    title="Biological Meaning",
                    marks=15.0,
                    content={
                        "solution": "Parameter b represents...",
                        "expectation": "Link math to biology.",
                        "common_errors": "Vague explanation.",
                        "marking": "Full marks for detailed explanation."
                    }
                )
            ]
        )
    ]

    # Lưu thẳng vào Database
    exam.questions = generated_questions
    
    # (Tùy chọn) Cập nhật trạng thái exam nếu cần
    # exam.status = "draft" 
    
    await exam.save()
    
    return {
        "message": "Successfully processed rubric",
        "generated_count": len(generated_questions)
    }