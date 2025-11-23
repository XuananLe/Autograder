# pages/3_Student_Dashboard.py
import streamlit as st
from services import api

st.set_page_config(page_title="Student Dashboard", layout="wide")

st.title("Cổng Thi Trực Tuyến")

# --- Ô NHẬP MÃ SINH VIÊN ---
col_input, _ = st.columns([1, 3])
if "student_id_input" not in st.session_state:
    st.session_state.student_id_input = "test" # Giá trị mặc định để test nhanh

student_id = col_input.text_input("Nhập Mã Sinh Viên của bạn:", value=st.session_state.student_id_input)
st.session_state.student_id_input = student_id # Lưu lại state

if not student_id:
    st.warning("Vui lòng nhập Mã Sinh Viên để xem bài thi.")
    st.stop()

# --- GỌI API LẤY DỮ LIỆU THEO ID ---
with st.spinner(f"Đang tìm bài thi của SV: {student_id}..."):
    my_exams = api.get_student_exams(student_id)

# --- HIỂN THỊ KẾT QUẢ ---
st.caption(f"Tìm thấy {len(my_exams)} bài thi.")
cols_h = st.columns([3, 2, 2, 1])
cols_h[0].markdown("**Tên Bài Thi**")
cols_h[1].markdown("**Hạn Nộp**")
cols_h[2].markdown("**Trạng Thái**")
cols_h[3].markdown("**Điểm**")
st.divider()

if not my_exams:
    st.info(f"Không tìm thấy bài thi nào cho ID: **{student_id}**")
    st.write("Gợi ý: Hãy kiểm tra lại xem Giáo viên đã 'Add Student' với đúng ID này chưa.")
else:
    for exam in my_exams:
        with st.container(border=True):
            cols = st.columns([3, 2, 2, 1])
            
            title = exam.get('title', 'Untitled')
            course = exam.get('course_name', 'Unknown')
            submission_id = exam.get('submission_id')
            
            # Nút bấm vào thi
            btn_label = f"**{title}**\n\n{course}"
            if cols[0].button(btn_label, key=f"btn_{submission_id}", use_container_width=True):
                st.session_state.selected_exam_data = exam 
                st.switch_page("pages/Exam_Detail.py")
            
            due = exam.get('due_date')
            cols[1].write(due[:10] if due else "--")
            
            status = exam.get('status', 'Unfinished')
            if status in ["Unfinished", "pending"]:
                cols[2].error("Chưa nộp", icon="❗")
            elif status == "graded":
                cols[2].success("Đã chấm", icon="✅")
            else:
                cols[2].info("Đã nộp", icon="🔵")
            
            score = exam.get('score')
            cols[3].metric("Điểm", score if score is not None else "--", label_visibility="collapsed")

