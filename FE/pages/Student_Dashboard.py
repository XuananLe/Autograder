# pages/3_Student_Dashboard.py
import streamlit as st

st.set_page_config(
    page_title="Student Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed" # Ẩn thanh sidebar mặc định
)

# --- Dữ liệu Giả (Mock Data) ---
# Khởi tạo state nếu nó chưa tồn tại (chỉ chạy 1 lần)
if 'exams' not in st.session_state:
    st.session_state.exams = [
        {
            "id": "ex001", 
            "title": "Thị giác máy", 
            "course": "INT3401E 2", 
            "due": "11:59pm 22/10/2025", 
            "status": "Unfinished", 
            "points": None,
            "feedback": "Not submitted yet.",
            "submission_file": None,
            "exam_file": "https://i.imgur.com/rNnF4Wf.png" # Ảnh mock đề thi
        },
        {
            "id": "ex002", 
            "title": "Thị giác máy", 
            "course": "INT3401E 2", 
            "due": "11:59pm 22/10/2025", 
            "status": "finished", 
            "points": None,
            "feedback": "Waiting for grading.",
            "submission_file": "My_Finished_Exam.pdf",
            "exam_file": "https://i.imgur.com/rNnF4Wf.png"
        },
        {
            "id": "ex003", 
            "title": "Thị giác máy", 
            "course": "INT3401E 2", 
            "due": "11:59pm 22/10/2025", 
            "status": "graded", 
            "points": 10, 
            "feedback": "you did very well. Hope you keep trying!", 
            "submission_file": "NguyenThiPhuong_23021668-3.docx",
            "exam_file": "https://i.imgur.com/rNnF4Wf.png"
        },
        {
            "id": "ex004", 
            "title": "Thị giác máy", 
            "course": "INT3401E 2", 
            "due": "11:59pm 22/10/2025", 
            "status": "graded", 
            "points": 8.5,
            "feedback": "Good work, but check calculation on Q2.",
            "submission_file": "My_Exam_8.5.pdf",
            "exam_file": "https://i.imgur.com/rNnF4Wf.png"
        }
    ]

st.title("Your exams")

# --- Header của Bảng ---
cols_h = st.columns([3, 2, 2, 1])
cols_h[0].write("**Title**")
cols_h[1].write("**Due**")
cols_h[2].write("**Status**")
cols_h[3].write("**Points**")
st.divider()

# --- Lặp qua và hiển thị danh sách Exam ---
for exam in st.session_state.exams:
    
    # Dùng st.container(border=True) để tạo "thẻ"
    with st.container(border=True):
        cols = st.columns([3, 2, 2, 1])
        
        # Cột 1: Tiêu đề (có thể click)
        # CẬP NHẬT: Thêm query_params để giữ trạng thái "student"
        # cols[0].page_link(
        #     "pages/4_Exam_Detail.py", 
        #     label=f"**{exam['title']}**\n\n{exam['course']}", 
        #     icon="📄",
        # )
        button_label = f"**{exam['title']}**\n\n{exam['course']}"
        
        # 2. Dùng st.button với key duy nhất
        if cols[0].button(button_label, key=f"go_to_{exam['id']}", use_container_width=True):
            # 3. Lưu ID vào state
            st.session_state.current_exam_id = exam["id"] 
            # 4. Chuyển trang
            st.switch_page("pages/Exam_Detail.py")
        
        # Cột 2: Due
        cols[1].write(exam["due"])
        
        # Cột 3: Status (dùng màu)
        if exam["status"] == "Unfinished":
            cols[2].error(exam["status"], icon="❗")
        elif exam["status"] == "graded":
            cols[2].success(exam["status"], icon="✅")
        else:
            cols[2].info(exam["status"], icon="🔵") # "finished"
        
        # Cột 4: Points
        cols[3].metric(
            "Points", # Thêm 1 nhãn (ví dụ: "Points")
            exam["points"] if exam["points"] is not None else "--",
            label_visibility="collapsed" # Ẩn nhãn đi
        )