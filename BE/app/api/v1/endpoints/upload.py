# app/api/v1/endpoints/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid

router = APIRouter()

@router.post("/", response_model=dict)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload file lên thư mục 'static' và trả về đường dẫn URL.
    """
    try:
        # 1. Kiểm tra định dạng (Optional)
        if not file.filename.endswith((".pdf", ".png", ".jpg", ".jpeg")):
             raise HTTPException(status_code=400, detail="Only PDF and Image files are allowed.")

        # 2. Tạo tên file độc nhất (UUID)
        # Ví dụ: bai_lam.pdf -> c9a2-4b12-....pdf
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"static/{unique_filename}"

        # 3. Lưu file xuống ổ cứng
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 4. Trả về đường dẫn
        # Lưu ý: Trả về đường dẫn tương đối hoặc tuyệt đối tùy nhu cầu
        return {
            "filename": file.filename, # Tên gốc
            "saved_name": unique_filename, # Tên đã lưu
            "url": f"static/{unique_filename}" # Đường dẫn để FE lưu vào DB
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")