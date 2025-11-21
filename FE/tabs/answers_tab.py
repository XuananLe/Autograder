import streamlit as st
import time
from services import api

# --- ĐỊNH NGHĨA DIALOGS ---

@st.dialog("Upload Student Paper")
def upload_and_link_dialog():
    exam_id = st.session_state.get("current_exam_id")
    
    st.write("Bước 1: Tải lên file bài làm (PDF)")
    uploaded_file = st.file_uploader("Chọn file PDF", type=["pdf"], label_visibility="collapsed")
    
    if uploaded_file:
        st.divider()
        st.write("Bước 2: Nhập thông tin sinh viên cho bài này")
        
        with st.form("manual_link_form"):
            col1, col2 = st.columns(2)
            with col1:
                student_id = st.text_input("Mã Sinh Viên (ID)")
            with col2:
                name = st.text_input("Họ và Tên")
            
            email = st.text_input("Email (Tùy chọn)")
            
            if st.form_submit_button("Lưu & Liên kết File", type="primary"):
                if not name or not student_id:
                    st.error("Vui lòng nhập Tên và Mã SV.")
                else:
                    try:
                        # 1. Upload file lên Server lấy URL trước
                        with st.spinner("Đang tải file lên server..."):
                            upload_resp = api.upload_file(uploaded_file)
                        
                        if not upload_resp:
                            st.error("Lỗi: Không thể upload file lên server.")
                            return

                        file_url = upload_resp.get("url") # Lấy URL file từ server trả về

                        # 2. Gửi thông tin SV + URL file vào danh sách
                        payload = {
                            "student_id": student_id,
                            "name": name,
                            "email": email,
                            "file_url": file_url # <--- QUAN TRỌNG: Link file vào SV
                        }
                        
                        if api.add_student_to_roster(exam_id, payload):
                            st.toast(f"Đã thêm bài làm của: {name}", icon="✅")
                            st.session_state.force_reload = True # Báo hiệu reload data
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Không thể thêm sinh viên. Có thể ID đã tồn tại.")
                            
                    except Exception as e:
                        st.error(f"Đã xảy ra lỗi: {e}")

# --- 2. HÀM ADD STUDENT ---
@st.dialog("Add Student from Database")
def add_student_dialog():
    exam_id = st.session_state.get("current_exam_id")
    st.write("Tìm kiếm sinh viên trong CSDL trường:")
    
    # Mock DB để search (Client side)
    # Trong thực tế bạn dùng api.search_students(query)
    mock_database = [
        {"id": "23020001", "name": "Nguyen Van A", "email": "a@vnu.edu.vn"},
        {"id": "23020002", "name": "Tran Thi B", "email": "b@vnu.edu.vn"},
        {"id": "23020003", "name": "Le Van C", "email": "c@vnu.edu.vn"},
    ]
    search_options = {f"{s['name']} - {s['id']}": s for s in mock_database}
    
    selected_option = st.selectbox(
        "Tìm kiếm", 
        options=list(search_options.keys()), 
        index=None, 
        placeholder="Nhập tên hoặc mã SV..."
    )
    
    if selected_option:
        student_data = search_options[selected_option]
        st.info(f"Đã chọn: **{student_data['name']}**")
        
        if st.button("Thêm vào danh sách", type="primary"):
            payload = {
                "student_id": student_data['id'],
                "name": student_data['name'],
                "email": student_data['email'],
                "file_url": None # Chưa có bài làm
            }
            
            if api.add_student_to_roster(exam_id, payload):
                st.success(f"Đã thêm {student_data['name']}!")
                st.session_state.force_reload = True
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning("Sinh viên này có thể đã có trong danh sách.")

# --- HÀM RENDER CHÍNH ---
def render():
    """Vẽ nội dung của tab Student Answers"""
    exam_id = st.session_state.get("current_exam_id")
    if not exam_id: return

    # 1. Check điều kiện tiên quyết
    if not st.session_state.get("rubric_complete", False):
        st.warning("Vui lòng hoàn thành bước 'Rubric' trước.")
        return

    # 2. Lấy dữ liệu Roster từ Session (Được load từ API bởi New_Exam.py)
    roster = st.session_state.get("student_roster", [])

    # -------------------------------------------------------
    # TRẠNG THÁI 1: PENDING (Chưa xử lý AI)
    # -------------------------------------------------------
    if st.session_state.answers_status == "pending":
        # Toolbar
        c1, c2, c3 = st.columns([1.5, 1.5, 4])
        if c1.button("➕ Upload Bài Làm", type="primary", use_container_width=True):
            upload_and_link_dialog()
        if c2.button("➕ Thêm SV từ DB", use_container_width=True):
            add_student_dialog()
        
        st.divider()

        # Danh sách sinh viên (Roster Table)
        st.write(f"**Danh sách lớp ({len(roster)} sinh viên)**")
        
        # Header bảng
        cols = st.columns([3, 2, 3, 2, 2])
        cols[0].markdown("**Họ Tên**")
        cols[1].markdown("**Mã SV**")
        cols[2].markdown("**Email**")
        cols[3].markdown("**File Bài Làm**")
        cols[4].markdown("**Trạng Thái**")
        
        if not roster:
            st.info("Chưa có sinh viên nào. Hãy upload bài làm hoặc thêm từ DB.")
        
        for s in roster:
            # Map data an toàn
            s_name = s.get("student_name", s.get("name", "Unknown"))
            s_id = s.get("student_id", s.get("id", ""))
            s_email = s.get("student_email", s.get("email", ""))
            s_file = s.get("file_url", s.get("file")) # Lấy URL file
            
            c = st.columns([3, 2, 3, 2, 2])
            c[0].write(s_name)
            c[1].write(s_id)
            c[2].write(s_email)
            
            # Cột File: Hiển thị link hoặc nút xem
            if s_file:
                c[3].write(f"📄 [Xem File]({s_file})") # Giả sử file_url là link xem được
            else:
                c[3].write("-")
                
            # Cột Trạng thái
            if s_file:
                c[4].success("Đã nộp", icon="✅")
            else:
                c[4].warning("Chưa nộp", icon="⚠️")
                
        st.divider()
        
        # --- FORM XỬ LÝ (Processing Options) ---
        # Form này chỉ hiện khi ở trạng thái Pending
        st.subheader("Tùy chọn xử lý AI")
        
        with st.form("answers_process_form"):
            c1, c2 = st.columns(2)
            c1.selectbox("Loại bài làm", ["Viết tay (Handwritten)", "Đánh máy (Typed)"])
            c2.selectbox("Mức độ chi tiết", ["Tiêu chuẩn", "Chi tiết từng bước"])
            
            with st.expander("Cấu hình nâng cao"):
                st.selectbox("OCR Engine", ["Azure AI Vision", "Google Vision"], key="ans_ocr")
                st.selectbox("LLM Model", ["OpenAI: GPT-4o", "OpenAI: GPT-4"], key="ans_gpt")

            # Nút Submit Form
            submitted = st.form_submit_button("🚀 Bắt đầu Chấm điểm (Begin Processing)", type="primary")
            
            if submitted:
                # Gọi API xử lý
                if api.process_answers(exam_id):
                    st.session_state.answers_status = "processing"
                    with st.spinner("Đang gửi lệnh xử lý lên server..."):
                        time.sleep(1.5)
                    
                    # Sau khi xử lý xong (giả lập)
                    st.session_state.answers_status = "processed"
                    st.session_state.answers_processing_complete = True
                    st.session_state.force_reload = True # Reload data mới (có kết quả OCR)
                    st.success("Đã gửi lệnh xử lý thành công!")
                    st.rerun()
                else:
                    st.error("Lỗi: Không thể gửi lệnh xử lý.")

    # -------------------------------------------------------
    # TRẠNG THÁI 2: PROCESSED (Đã có kết quả)
    # -------------------------------------------------------
    elif st.session_state.answers_status == "processed":
        st.success("✅ Đã xử lý xong bài làm của sinh viên.")
        
        search = st.text_input("Tìm kiếm bài làm...", placeholder="Nhập tên hoặc mã SV...")
        
        # Filter danh sách hiển thị
        display_list = roster
        if search:
            s_lower = search.lower()
            display_list = [s for s in roster if s_lower in s.get("student_name", "").lower()]
            
        for s in display_list:
            s_name = s.get("student_name", "Unknown")
            # Hiển thị kết quả OCR (giả lập hiển thị expander)
            with st.expander(f"Bài làm: {s_name}"):
                c1, c2 = st.columns(2)
                c1.info("Bản gốc (PDF)")
                # c1.image(...) 
                c2.success("AI Trích xuất (OCR)")
                c2.write("Nội dung bài làm sẽ hiện ở đây...")