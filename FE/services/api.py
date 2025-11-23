# services/api.py
import requests
import streamlit as st

API_URL = "http://localhost:8000/api/v1"

def get_exams():
    """Lấy danh sách tất cả kỳ thi"""
    try:
        resp = requests.get(f"{API_URL}/exams/")
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def create_exam(title: str):
    """Tạo kỳ thi mới"""
    resp = requests.post(f"{API_URL}/exams/", json={"title": title})
    return resp.json() if resp.status_code == 200 else None

def get_exam_detail(exam_id: str):
    """Lấy chi tiết 1 kỳ thi"""
    resp = requests.get(f"{API_URL}/exams/{exam_id}")
    return resp.json() if resp.status_code == 200 else None

def update_exam_info(exam_id: str, data: dict):
    """Cập nhật thông tin (Tab Info)"""
    resp = requests.put(f"{API_URL}/exams/{exam_id}/info", json=data)
    return resp.status_code == 200

def update_rubric(exam_id: str, questions: list):
    """Lưu Rubric"""
    # Backend đang mong đợi dict: { "questions": [...] }
    payload = {"questions": questions}
    resp = requests.put(f"{API_URL}/exams/{exam_id}/rubric", json=payload)
    return resp.status_code == 200

def get_roster(exam_id: str):
    """Lấy danh sách sinh viên nộp bài"""
    resp = requests.get(f"{API_URL}/submissions/{exam_id}/roster")
    return resp.json() if resp.status_code == 200 else []

def add_student_to_roster(exam_id: str, student_data: dict):
    """Thêm sinh viên vào danh sách"""
    resp = requests.post(f"{API_URL}/submissions/{exam_id}/students", json=student_data)
    return resp.status_code == 200

def process_answers(exam_id: str):
    """Kích hoạt OCR"""
    resp = requests.post(f"{API_URL}/submissions/{exam_id}/process-answers")
    return resp.status_code == 200

def grade_exam(exam_id: str):
    """Kích hoạt chấm điểm"""
    resp = requests.post(f"{API_URL}/submissions/{exam_id}/grade")
    return resp.status_code == 200
def search_students(query: str):
    """Tìm kiếm sinh viên từ Database toàn trường"""
    try:
        # params={'q': query} sẽ tạo url: .../students/search?q=abc
        resp = requests.get(f"{API_URL}/students/search", params={"q": query})
        return resp.json() if resp.status_code == 200 else []
    except:
        return []
def upload_file(uploaded_file_obj):
    """
    Upload file object của Streamlit lên Server.
    """
    try:
        # 'file' là tên tham số mà FastAPI endpoint yêu cầu (file: UploadFile)
        files = {"file": (uploaded_file_obj.name, uploaded_file_obj, uploaded_file_obj.type)}
        
        resp = requests.post(f"{API_URL}/upload/", files=files)
        
        if resp.status_code == 200:
            return resp.json() # Trả về {"url": "static/..."}
        else:
            st.error(f"Upload failed: {resp.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to server: {e}")
        return None
def process_rubric(exam_id: str, options: dict):
    """
    Gửi lệnh yêu cầu Server xử lý Rubric (OCR + AI Extraction)
    """
    try:
        resp = requests.post(f"{API_URL}/exams/{exam_id}/rubric/process", json=options)
        return resp.status_code == 200
    except Exception as e:
        st.error(f"API Error: {e}")
        return False
    
def get_student_exams(student_id: str):
    """
    Lấy danh sách bài thi theo ID sinh viên.
    """
    try:
        # Gọi endpoint lọc theo ID
        resp = requests.get(f"{API_URL}/submissions/student/{student_id}")
        return resp.json() if resp.status_code == 200 else []
    except Exception as e:
        print(f"Error fetching exams: {e}")
        return []

# ... (các hàm submit giữ nguyên)
def submit_exam_paper(submission_id: str, file_url: str):
    try:
        resp = requests.post(
            f"{API_URL}/submissions/{submission_id}/submit", 
            json={"file_url": file_url}
        )
        return resp.status_code == 200
    except Exception as e:
        print(f"Error submitting: {e}")
        return False