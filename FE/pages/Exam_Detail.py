# pages/4_Exam_Detail.py
import streamlit as st
from services import api
import time

st.set_page_config(page_title="Chi Tiết Bài Thi", layout="wide")

# 1. Lấy dữ liệu từ session (được truyền từ Dashboard)
exam_data = st.session_state.get("selected_exam_data")

if not exam_data:
    st.error("Chưa chọn bài thi nào.")
    if st.button("< Quay lại Dashboard"):
        st.switch_page("pages/Student_Dashboard.py")
    st.stop()

# Nút quay về
if st.button("< Quay lại Dashboard"):
    st.switch_page("pages/Student_Dashboard.py")

# Tiêu đề & Thông tin chung
st.title(exam_data.get('title'))
st.caption(f"Môn học: {exam_data.get('course_name')}")

col_main, col_sidebar = st.columns([2, 1])

# --- CỘT TRÁI: Đề bài ---
with col_main:
    st.header("Đề Bài")
    # Trong thực tế, bạn có thể lấy URL đề bài từ API nếu có. 
    # Hiện tại hiển thị ảnh mẫu.
    st.image("https://i.imgur.com/rNnF4Wf.png", caption="Đề thi", use_container_width=True)

# --- CỘT PHẢI: Trạng thái & Nộp bài ---
with col_sidebar:
    status = exam_data.get('status')
    score = exam_data.get('score')
    submission_id = exam_data.get('submission_id')
    existing_file = exam_data.get('file_url')
    feedback = exam_data.get('feedback')

    # Kiểm tra trạng thái để hiển thị Form Nộp Bài hay Kết Quả
    # Logic: Nếu chưa có file nộp (hoặc status là pending/unfinished) -> Hiện Form
    is_submitted = existing_file is not None
    
    if not is_submitted:
        # --- TRƯỜNG HỢP 1: CHƯA NỘP ---
        cols_status = st.columns(2)
        cols_status[0].info("Chưa nộp bài", icon="❕")
        cols_status[1].metric("Điểm", "--")

        st.divider()
        st.subheader("Nộp Bài")
        
        uploaded_file = st.file_uploader("Tải lên bài làm (PDF)", type=["pdf"])
        
        if uploaded_file:
            if st.button("Nộp Bài Thi", type="primary", use_container_width=True):
                try:
                    # B1: Upload file lên Server lấy URL
                    with st.spinner("Đang tải file lên server..."):
                        upload_res = api.upload_file(uploaded_file)
                    
                    if upload_res:
                        file_url = upload_res.get('url')
                        
                        # B2: Gọi API Submit (Update DB với link file mới)
                        if api.submit_exam_paper(submission_id, file_url):
                            st.success("Nộp bài thành công!")
                            st.balloons()
                            
                            # Cập nhật lại trạng thái local để UI tự đổi ngay lập tức
                            exam_data['status'] = 'finished'
                            exam_data['file_url'] = file_url
                            st.session_state.selected_exam_data = exam_data # Lưu ngược lại vào session
                            
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error("Lỗi: Không thể cập nhật trạng thái nộp bài.")
                    else:
                        st.error("Lỗi upload file.")
                        
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {e}")

    else:
        # --- TRƯỜNG HỢP 2: ĐÃ NỘP / ĐÃ CHẤM ---
        cols_status = st.columns(2)
        cols_status[0].success("Đã nộp", icon="✅")
        
        if score is not None:
            cols_status[1].metric("Điểm", f"{score}/10")
        else:
            cols_status[1].caption("Đang chờ chấm...")

        st.divider()
        st.subheader("Bài làm của bạn")
        
        if existing_file:
            st.write(f"File đã nộp: `{existing_file}`")
            # Link download (giả lập mở tab mới)
            st.link_button("📄 Xem bài làm", existing_file)
        
        st.divider()
        st.subheader("Nhận xét của Giáo viên / AI")
        if feedback:
            st.info(feedback)
        else:
            st.caption("Chưa có nhận xét.")
