import streamlit as st
import time

# --- ĐỊNH NGHĨA DIALOGS ---
# (Các hàm dialog chỉ được dùng bởi tab này, nên đặt chúng ở đây)
@st.dialog("Upload and Link Student Paper")
def upload_and_link_dialog():
    st.write("Upload PDF:")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        student_names = [s["name"] for s in st.session_state.student_roster]
        selected_name = st.selectbox("Find student", options=student_names, index=None)
        if st.button("Link File", type="primary"):
            for i, student in enumerate(st.session_state.student_roster):
                if student["name"] == selected_name:
                    st.session_state.student_roster[i]["file"] = uploaded_file.name
                    st.rerun()
                    break

@st.dialog("Add New Student to Roster")
def add_student_dialog():
    with st.form(key="new_student_form"):
        name = st.text_input("Full Name")
        student_id = st.text_input("Student ID")
        email = st.text_input("Email")
        if st.form_submit_button("Add Student"):
            new_student = {"id": student_id, "name": name, "email": email, "file": None}
            st.session_state.student_roster.append(new_student)
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
                if col_d4.button("View", key=f"view_{student['id']}"):
                    with st.dialog("Student Details"):
                        st.image("https.i.imgur.com/331iCIw.png")
                        st.subheader(student["name"])
                        st.write(f"**ID:** {student['id']}")
                        st.write(f"**Email:** {student['email']}")
                        if student["file"]:
                            st.write(f"**File Linked:** {student['file']}")
                        else:
                            st.write(f"**File Linked:** None")

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
    