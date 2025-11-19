import streamlit as st
import time

# --- ĐỊNH NGHĨA DIALOGS ---
@st.dialog("Upload Student Paper")
def upload_and_link_dialog():
    st.write("Step 1: Upload the PDF file")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    
    if uploaded_file:
        st.divider()
        st.write("Step 2: Enter Student Details for this paper")
        
        # Form để điền thông tin thủ công
        with st.form("manual_link_form"):
            name = st.text_input("Full Name")
            student_id = st.text_input("Student ID")
            email = st.text_input("Email")
            
            if st.form_submit_button("Save & Link File", type="primary"):
                if not name or not student_id:
                    st.error("Name and ID are required.")
                else:
                    # Tạo object sinh viên mới kèm file
                    new_student_with_file = {
                        "id": student_id,
                        "name": name,
                        "email": email,
                        "file": uploaded_file.name, # Gán file luôn
                        "processed_content": None
                    }
                    
                    # Thêm vào danh sách lớp
                    st.session_state.student_roster.append(new_student_with_file)
                    st.success(f"Added & Linked: {name}")
                    time.sleep(0.5)
                    st.rerun()

# --- 2. HÀM ADD STUDENT (Đã sửa: Thanh Search từ Database giả lập) ---
@st.dialog("Add Student from Database")
def add_student_dialog():
    st.write("Search for an existing student to add to the roster:")
    
    # --- GIẢ LẬP DATABASE TOÀN TRƯỜNG ---
    # Trong thực tế, cái này sẽ gọi API hoặc DB
    mock_database = [
        {"id": "23029999", "name": "Lê Văn Luyện", "email": "luyen@example.com"},
        {"id": "23028888", "name": "Trần Thị Bưởi", "email": "buoi@example.com"},
        {"id": "23027777", "name": "Ngô Bá Khá", "email": "kha@example.com"},
        {"id": "23026666", "name": "Đỗ Nam Trung", "email": "trung@example.com"},
    ]
    
    # Tạo list hiển thị cho Selectbox (Format: "Name - ID")
    search_options = {f"{s['name']} - {s['id']}": s for s in mock_database}
    
    # Thanh tìm kiếm (Selectbox hoạt động như search)
    selected_option = st.selectbox(
        "Search student", 
        options=list(search_options.keys()), 
        index=None, 
        placeholder="Type name or ID to search..."
    )
    
    if selected_option:
        # Lấy thông tin chi tiết từ selection
        student_data = search_options[selected_option]
        
        st.info(f"Selected: **{student_data['name']}** ({student_data['email']})")
        
        if st.button("Add to Roster", type="primary"):
            # Kiểm tra xem đã có trong lớp chưa để tránh trùng
            existing_ids = [s['id'] for s in st.session_state.student_roster if s['id'] != 'none']
            
            if student_data['id'] in existing_ids:
                st.warning("This student is already in the roster.")
            else:
                # Thêm vào roster (chưa có file)
                new_student = {
                    "id": student_data['id'],
                    "name": student_data['name'],
                    "email": student_data['email'],
                    "file": None, # Chưa có file
                    "processed_content": None
                }
                st.session_state.student_roster.append(new_student)
                st.success(f"Successfully added {student_data['name']}!")
                time.sleep(0.5)
                st.rerun()
# --- HÀM RENDER CHÍNH ---
def render():
    """Vẽ nội dung của tab Student Answers"""
    if not st.session_state.get("rubric_complete", False):
        st.warning("Vui lòng hoàn thành và xử lý 'Rubric' trước.")
        return

    if st.session_state.answers_status == "pending":
        # Nút bấm
        col_btn_1, col_btn_2, _ = st.columns([1, 1, 3])
        if col_btn_1.button("Upload PDF ➕", type="primary", use_container_width=True):
            upload_and_link_dialog()
        if col_btn_2.button("Add Student ➕", use_container_width=True):
            add_student_dialog()
        st.divider()

        # Bảng Roster
        st.subheader("Student Roster")
        
        col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns([3, 2, 3, 1, 1])
        col_h1.write("**Name**")
        col_h2.write("**Student ID**")
        col_h3.write("**Email**")
        col_h4.write("**View**")
        col_h5.write("**Status**")    
        for student in st.session_state.student_roster:
                col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns([3, 2, 3, 1, 1])
                
                col_d1.write(student["name"])
                col_d2.write(student["id"])
                col_d3.write(student["email"])
                
                # Nút "View" (Giữ nguyên)
                if student.get("file"): 
                    if col_d4.button("View", key=f"view_{student['id']}"):
                        @st.dialog("Student Details", width="large")
                        def show_details(s):
                            with st.container(height=600):
                        # Chia làm 2 cột: Cột trái (Info), Cột phải (Bài làm)
                                col_info, col_paper = st.columns([1, 2]) 
                                
                                with col_info:
                                    st.subheader(s["name"])
                                    st.write(f"**ID:** {s['id']}")
                                    st.write(f"**Email:** {s['email']}")
                                    st.write(f"**File Linked:** {s.get('file', 'None')}")
                                
                                with col_paper:
                                    st.subheader("Exam Paper Preview")
                                    if s.get('file'):
                                        # Hiển thị ảnh giả lập bài làm (hoặc PDF viewer)
                                        st.image("https://i.imgur.com/gKk9Nf2.png", caption=f"File: {s['file']}")
                                    else:
                                        st.info("No paper linked yet.")
                        show_details(student)
                else:
                    # Nếu chưa có bài làm, để trống hoặc hiện dấu gạch ngang
                    col_d4.write("-")

                # Trạng thái (Status) (Giữ nguyên)
                if student["file"] is not None:
                    col_d5.success("Matched", icon="✅")
                else:
                    col_d5.warning("None", icon="⚠️")
            
            # --- Form Tùy chọn (Options) (Giữ nguyên) ---
        st.divider()
        st.subheader("Processing Options")
            
        with st.form("answers_options_form"):
            st.selectbox("Submission Type", ["Handwritten", "Typed"]) 
            with st.expander("» Advanced"):
                st.selectbox("OCR Method", ["Azure Vision", "OpenAI: GPT-4o"], key="ans_ocr")
                st.selectbox("GPT Model", ["OpenAI: GPT-4o", "OpenAI: GPT-4"], key="ans_gpt")
                st.selectbox("Vision Model", ["OpenAI: GPT-4o", "Google Gemini"], key="ans_vis")

            if st.form_submit_button("Begin Processing →", type="primary"):
                st.session_state.answers_status = "processing"
                with st.spinner("Đang xử lý bài làm của sinh viên... (Fake 3 giây)"):
                    time.sleep(3) 
                    
                st.session_state.answers_status = "processed"
                st.session_state.answers_processing_complete = True
                st.success("Xử lý hoàn tất!")
                st.rerun()

    elif st.session_state.answers_status == "processed":
        
        st.subheader("Processed Student Answers")
        
        # Thanh tìm kiếm (Giả lập)
        st.text_input("Search Student...", placeholder="🔍 Search by name, email, or ID", label_visibility="collapsed")
        
        # Lặp qua các sinh viên và hiển thị bài làm
        for student in st.session_state.student_roster:
            
            processed_data = student.get("processed_content")
            if not processed_data:
                continue
                
            # Dùng st.expander cho mỗi sinh viên
            with st.expander(f"**{student['name']}** - {student['id']} - ({student.get('file', 'No File')})"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Original PDF (View)")
                    st.write(f"Hiển thị file PDF `{student.get('file', '')}` ở đây...")
                    # st.image(...) hoặc st.pdf_viewer(...)
                
                with col2:
                    st.subheader("Student Answer (AI Extracted)")
                    
                    # Dữ liệu mock từ state
                    q_text = student["processed_content"]["question_1_text"]
                    q_latex = student["processed_content"]["question_1_latex"]
                    
                    # Tabs (Text và LaTeX)
                    tab_text, tab_latex = st.tabs(["T (Text)", "T (LaTeX)"])
                    
                    with tab_text:
                        # Hiển thị LaTeX đã render
                        st.markdown(q_text)
                        
                    with tab_latex:
                        # Hiển thị code LaTeX (có thể chỉnh sửa)
                        st.text_area("Edit LaTeX", value=q_latex, height=200)
    