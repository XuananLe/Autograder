# pages/4_Exam_Detail.py
import streamlit as st

st.set_page_config(
    page_title="Exam Details",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- KHÔNG CẦN BẢO VỆ (GUARD) ---

# 1. Đọc "exam_id" từ session_state (Cách này ổn định)
selected_exam_id = st.session_state.get("current_exam_id")

# 2. Tìm dữ liệu exam (Giữ nguyên)
exam_data = None
if 'exams' in st.session_state and selected_exam_id:
    for exam in st.session_state.exams:
        if exam["id"] == selected_exam_id:
            exam_data = exam
            break

# 3. Xử lý lỗi
if not exam_data:
    st.error("Could not find the selected exam.")
    if st.button("< Back to Dashboard"):
        st.switch_page("pages/Student_Dashboard.py")
    st.stop()

# 4. Hiển thị trang chi tiết
# Nút quay về (Dùng st.button + st.switch_page)
if st.button("< Back to AI Grader"):
    st.switch_page("pages/Student_Dashboard.py")
    
st.title(exam_data['title'])

col_main, col_sidebar = st.columns([2, 1])

# --- CỘT TRÁI (Đề bài) ---
with col_main:
    st.header("Exam Paper")
    st.image(exam_data["exam_file"], use_container_width=True)

# --- CỘT PHẢI (Thông tin) ---
with col_sidebar:
    
    # --- *** BẮT ĐẦU SỬA ĐỔI LOGIC *** ---
    
    # TRƯỜNG HỢP 1: UNFINISHED (Ảnh 2 - Cho phép nộp bài)
    if exam_data["status"] == "Unfinished":
        # Hiển thị các hộp trạng thái (nhưng làm mờ)
        cols_status = st.columns(2)
        with cols_status[0]:
            st.info("Not Submitted", icon="❕") # Màu xanh dương
        with cols_status[1]:
            st.metric("Points", "--")

        st.divider()
        st.subheader("Submitting: upload a file")
        st.warning("You have not submitted this exam yet.")
        
        uploaded_file = st.file_uploader("Upload your file here")
        
        if uploaded_file is not None:
            if st.button("Submit Exam", type="primary"):
                # Cập nhật state
                exam_data["status"] = "finished" 
                exam_data["submission_file"] = uploaded_file.name
                exam_data["feedback"] = "Submitted! Waiting for grading."
                st.success("Exam Submitted!")
                st.rerun()

    # TRƯỜNG HỢP 2: FINISHED hoặc GRADED (Ảnh 3 - Hiển thị chi tiết)
    else:
        # Hiển thị các hộp trạng thái (với dữ liệu)
        cols_status = st.columns(2)
        with cols_status[0]:
            # Dùng st.error để có hộp màu đỏ/nâu
            st.error("Submitted", icon="✅") 
        with cols_status[1]:
            if exam_data['points'] is not None:
                # Dùng st.success để có hộp màu xanh lá
                st.success(f"Points: {exam_data['points']}", icon="⭐")

        st.divider()
        
        st.subheader("Submitting: upload a file") # Tiêu đề tĩnh
        
        st.write("**Submission**")
        st.caption("Submitted!")
        st.caption("Oct 16 at 11:59pm (Mock Date)")
        st.caption("Submission Details") # Chỉ là text
        
        if exam_data.get("submission_file"):
            fake_file_content = f"Mock data for {exam_data['submission_file']}"
            st.download_button(
                label=f"Download {exam_data['submission_file']}",
                data=fake_file_content,
                file_name=exam_data["submission_file"]
            )
        
        st.divider()

        # Hiển thị Feedback
        st.subheader("Feedback:")
        if exam_data.get("feedback"):
            # Hiển thị feedback dưới dạng văn bản thuần
            st.write(exam_data["feedback"])
        else:
            st.info("No feedback yet.")
            
    # --- *** LOGIC KẾT THÚC TẠI ĐÂY *** ---