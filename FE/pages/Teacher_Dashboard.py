# 1_Dashboard.py
import streamlit as st
from services import api

st.set_page_config(
    page_title="GoodPoint Dashboard",
    layout="centered"
)

# --- HEADER & NEW EXAM BUTTON ---
st.title("GoodPoint")
st.caption("Create a new exam or select a previous one")

# Nút này chỉ dùng để TẠO MỚI
if st.button("📄 + New Exam", use_container_width=True):
    # Gọi API tạo draft exam
    new_exam = api.create_exam("Untitled Exam")
    if new_exam:
        st.session_state.current_exam_id = new_exam['id'] # Lưu ID
        # Reset các trạng thái cũ để tránh hiển thị data của exam trước
        st.session_state.force_reload = True 
        st.switch_page("pages/New_Exam.py")

st.divider()

# --- FETCH DATA TỪ API ---
# Lấy toàn bộ danh sách exam
all_exams = api.get_exams()

# Phân loại Exam dựa trên 'status'
# (Giả sử status: 'draft', 'published', 'grading' -> Ongoing | 'graded', 'finalized' -> Graded)
ongoing_exams = []
graded_exams = []

if all_exams:
    for exam in all_exams:
        status = exam.get('status', 'draft')
        if status in ['graded', 'finalized']:
            graded_exams.append(exam)
        else:
            ongoing_exams.append(exam)

# --- SECTION 1: ONGOING EXAMS ---
st.subheader("Ongoing Exams")
with st.container(border=True):
    if not ongoing_exams:
        st.info("No ongoing exams found.")
    else:
        for exam in ongoing_exams:
            cols = st.columns([3, 2, 1])
            
            # Cột 1: Tên Exam
            cols[0].write(f"**{exam.get('title', 'Untitled')}**")
            
            # Cột 2: Ngày tạo (Format lại chút cho đẹp nếu có)
            date_str = exam.get('created_at', '')
            if date_str:
                date_str = date_str[:10] # Lấy YYYY-MM-DD
            cols[1].write(date_str)
            
            # Cột 3: Nút Edit
            # Dùng key unique để tránh lỗi duplicate widget ID
            if cols[2].button("Edit", key=f"btn_edit_{exam['id']}"):
                st.session_state.current_exam_id = exam['id']
                st.session_state.force_reload = True # Bắt buộc load lại data mới
                st.switch_page("pages/New_Exam.py")

# --- SECTION 2: GRADED EXAMS ---
st.subheader("Graded Exams")
with st.container(border=True):
    if not graded_exams:
        st.info("No graded exams yet.")
    else:
        for exam in graded_exams:
            cols = st.columns([3, 2, 1])
            
            # Cột 1: Tên Exam
            cols[0].write(f"**{exam.get('title', 'Untitled')}**")
            
            # Cột 2: Ngày tạo
            date_str = exam.get('created_at', '')[:10]
            cols[1].write(date_str)
            
            # Cột 3: Trạng thái (Badge màu xanh) hoặc nút View
            # Nếu muốn xem lại kết quả, có thể đổi thành nút button("Results")
            cols[2].success("Graded") 
            
            # (Optional) Nếu bạn muốn bấm vào để xem lại cấu hình:
            # if cols[2].button("View", key=f"btn_view_{exam['id']}"):
            #     st.session_state.current_exam_id = exam['id']
            #     st.session_state.force_reload = True
            #     st.switch_page("pages/2_New_Exam.py")