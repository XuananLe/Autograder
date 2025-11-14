# app_tabs/grading_tab.py
import streamlit as st
import time
import pandas as pd # Cần pandas để tạo bảng Grade Boundaries

# --- HÀM DIALOG (cho nút "Edit Grade Boundaries") ---
@st.dialog("Edit Grade Boundaries")
def edit_boundaries_dialog():
    st.write("Configure the grade boundaries:")
    
    # Dùng st.data_editor để tạo bảng có thể sửa
    grade_data = pd.DataFrame([
        {"Grade": "A+", "Min. Mark (%)": 95},
        {"Grade": "A", "Min. Mark (%)": 80},
        {"Grade": "B", "Min. Mark (%)": 70},
        {"Grade": "C", "Min. Mark (%)": 60},
        {"Grade": "F", "Min. Mark (%)": 0},
    ])
    st.data_editor(grade_data, num_rows="dynamic") # num_rows="dynamic" cho phép thêm/xóa hàng

    if st.button("Save Boundaries"):
        # (Lưu logic ở đây)
        st.rerun()


# --- HÀM RENDER CHÍNH ---
def render():
    """Vẽ nội dung của tab Grading"""
    
    # 1. Khóa tab nếu Student Answers chưa xong
    if not st.session_state.get("answers_processing_complete", False):
        st.warning("Vui lòng hoàn thành và nhấn 'Finish' ở tab 'Student answers' trước.")
        return

    # -----------------------------------------------------------------
    # --- TRẠNG THÁI 1: CONFIGURING (Image 4) ---
    # -----------------------------------------------------------------
    if st.session_state.grading_status == "configuring":
        st.subheader("Grading Options")
        st.caption("Configure the grading process")

        with st.form("grading_options_form"):
            
            st.selectbox(
                "Marking Generosity", 
                ["4: Generous, allowing general alignment with rubric"]
            )

            # Bảng Grade Boundaries (dùng st.data_editor)
            st.write("Grade Boundaries")
            grade_data = pd.DataFrame([
                {"Grade": "A+", "Min. Mark (%)": 95},
                {"Grade": "A", "Min. Mark (%)": 80},
                {"Grade": "B", "Min. Mark (%)": 70},
                {"Grade": "C", "Min. Mark (%)": 60},
                {"Grade": "D", "Min. Mark (%)": 50},
                {"Grade": "F", "Min. Mark (%)": 0},
            ])
            st.data_editor(grade_data, num_rows="dynamic")

            with st.expander("» Advanced"):
                st.selectbox("GPT Model", ["OpenAI: GPT-4o", "OpenAI: GPT-4"])
                st.number_input("Feedback token length", value=140)

            # Nút "Start Grading" (button "answer" mà bạn nói)
            if st.form_submit_button("Start Grading →", type="primary"):
                st.session_state.grading_status = "processing"
                st.rerun()

    # -----------------------------------------------------------------
    # --- TRẠNG THÁI 2: PROCESSING (Đang chạy) ---
    # -----------------------------------------------------------------
    elif st.session_state.grading_status == "processing":
        with st.spinner("Đang chấm điểm... (Fake 3 giây)"):
            time.sleep(3)
        st.session_state.grading_status = "processed"
        st.success("Grading Complete!")
        st.rerun()

    # -----------------------------------------------------------------
    # --- TRẠNG THÁI 3: PROCESSED (Image 1, 2, 3) ---
    # -----------------------------------------------------------------
    elif st.session_state.grading_status == "processed":
        
        # --- Hai tab con mới ---
        tab_class, tab_student = st.tabs(["Class Performance", "Student Performance"])

        # --- Tab con 1: Class Performance (Image 2, 3) ---
        with tab_class:
            st.subheader("Class Results (Generated with AI)")
            
            with st.container(border=True):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Class Average", "81.6%", "Grade A")
                    st.caption("16.3/20 Marks")
                with col2:
                    if st.button("Edit Grade Boundaries"):
                        edit_boundaries_dialog() # Gọi dialog
                
                # Biểu đồ (dùng ảnh giả)
                st.image("https://i.imgur.com/kH8N3hV.png") 

            # Class Feedback
            with st.expander("Class Feedback (Generated with AI)", expanded=True):
                st.write("Based on the provided feedback... (Fake text)...")

            # Question Feedback
            st.subheader("Question feedback")
            st.checkbox("Show only mistakes")
            st.checkbox("Show only feedback needing review")
            
            
            search_query = st.text_input("🔍 Search Questions", placeholder="Search...", label_visibility="collapsed")
            # Lọc danh sách câu hỏi
            questions_to_show = st.session_state.processed_questions
            if search_query:
                questions_to_show = [
                    q for q in questions_to_show 
                    if search_query.lower() in q['title'].lower()
                ]
            # Danh sách câu hỏi (Giống Rubric)
            for q in questions_to_show:
                grading_info = q.get("grading_data", {})
                expander_label = f"**> {q['title']}** (Average: {grading_info.get('average_str', 'N/A')})"
                
                with st.expander(expander_label, expanded=(q['id'] == 'q1')):
                    col_solution_key, col_feedback_data = st.columns(2)
                    with col_solution_key:
                            st.write(f"**(Hiển thị PDF/Ảnh Solution Key cho {q['title']} ở đây)**")
                            # Mock PDF viewer toolbar
                            st.image("https://i.imgur.com/UfK8Ytl.png") 
                            # Mock PDF content
                            st.image("https://i.imgur.com/gKk9Nf2.png") 
                        
                        # --- CỘT 2: Thông tin Feedback (Bên phải) ---
                    with col_feedback_data:
                            # 1. Question Content (Collapsible)
                        with st.expander("Question Content", expanded=True):
                            st.write(q['description'])
                            st.latex(r'''\frac{dv}{dt} = f(v) - w + I_a''') # Fake LaTeX

                            # 2. Statistics (Collapsible)
                        with st.expander("Statistics (Generated with AI)", expanded=True):
                            stats = grading_info.get("statistics", {})
                            for key, value in stats.items():
                                st.metric(label=key, value=value)
                            
                            # 3. Feedback (Collapsible)
                        with st.expander("Feedback (Generated with AI)", expanded=True):
                            st.text_area(
                                "Feedback text", 
                                value=grading_info.get("feedback", "No feedback available."), 
                                height=300,
                                key=f"feedback_{q['id']}" # Key này rất quan trọng
                            )

        # --- Tab con 2: Student Performance (Image 1) ---
        with tab_student:
            st.subheader("Individual Student Performance")
            
            # Chọn sinh viên
            student_names = [s["name"] for s in st.session_state.student_roster if s['id'] != 'none']
            selected_student = st.selectbox("Select Student", student_names)
            
            st.write(f"Showing results for **{selected_student}**")
            
            # Layout 2 cột (PDF viewer và Nội dung)
            col_pdf, col_content = st.columns(2)
            
            with col_pdf:
                st.write(f"(Hiển thị PDF viewer cho {selected_student} ở đây...)")
                st.image("https://i.imgur.com/UfK8Ytl.png")
                st.image("https://i.imgur.com/gKk9Nf2.png")
            
            with col_content:
                # Lặp qua các câu hỏi để hiển thị Feedback
                for q in st.session_state.processed_questions:
                    grading_info = q.get("grading_data", {})
                    expander_label = f"**> {q['title']}** (Average: {grading_info.get('average_str', 'N/A')})"
                    
                    with st.expander(expander_label, expanded=(q['id'] == 'q1')):
                        
                        # Question Content (Collapsible)
                        with st.expander("Question Content", expanded=True):
                            st.write(q['description'])
                            st.latex(r'''\frac{dv}{dt} = f(v) - w + I_a''')

                        # Statistics (Collapsible)
                        with st.expander("Statistics (Generated with AI)", expanded=True):
                            stats = grading_info.get("statistics", {})
                            for key, value in stats.items():
                                st.metric(label=key, value=value)
                        
                        # Feedback (Collapsible)
                        with st.expander("Feedback (Generated with AI)", expanded=True):
                            st.text_area(
                                "Feedback text", 
                                value=grading_info.get("feedback", "No feedback available."), 
                                height=300,
                                key=f"feedback_student_{q['id']}"
                            )