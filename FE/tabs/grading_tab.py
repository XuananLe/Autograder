# app_tabs/grading_tab.py
import streamlit as st
import time
import pandas as pd

# --- HÀM RENDER CHÍNH ---
def render():
    """Vẽ nội dung của tab Grading"""
    
    # 1. Khóa tab nếu chưa xử lý xong bài làm
    # (Dùng .get để tránh lỗi nếu key chưa khởi tạo)
    if not st.session_state.get("answers_processing_complete", False):
        st.warning("Vui lòng hoàn thành và nhấn 'Finish' ở bước 'Student answers' trước.")
        return

    # -----------------------------------------------------------------
    # --- TRẠNG THÁI 1: CONFIGURING ---
    # -----------------------------------------------------------------
    if st.session_state.grading_status == "configuring":
        st.subheader("Grading Options")
        with st.form("grading_options_form"):
            st.selectbox("Marking Generosity", ["4: Generous", "3: Standard", "2: Strict"])
            
            # Grade Boundaries
            st.write("Grade Boundaries")
            grade_data = pd.DataFrame([
                {"Grade": "A", "Min. Mark (%)": 80},
                {"Grade": "B", "Min. Mark (%)": 70},
                {"Grade": "C", "Min. Mark (%)": 60},
                {"Grade": "F", "Min. Mark (%)": 0},
            ])
            st.data_editor(grade_data, num_rows="dynamic")

            if st.form_submit_button("Start Grading →", type="primary"):
                st.session_state.grading_status = "processing"
                st.rerun()

    # -----------------------------------------------------------------
    # --- TRẠNG THÁI 2: PROCESSING ---
    # -----------------------------------------------------------------
    elif st.session_state.grading_status == "processing":
        with st.spinner("AI is grading submissions..."):
            time.sleep(2) # Mock delay
        st.session_state.grading_status = "processed"
        st.success("Grading Complete!")
        st.rerun()

    # -----------------------------------------------------------------
    # --- TRẠNG THÁI 3: PROCESSED ---
    # -----------------------------------------------------------------
    elif st.session_state.grading_status == "processed":
        
        tab_class, tab_student = st.tabs(["Class Performance", "Student Performance"])

        # --- Tab 1: Class Performance ---
        with tab_class:
            st.subheader("Class Results")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Class Average", "7.5/10", "75%")
            with col2:
                st.info("Biểu đồ phân bố điểm sẽ hiện ở đây (cần thư viện matplotlib/altair)")

            # Question Feedback
            st.subheader("Question Analysis")
            questions = st.session_state.get("processed_questions", [])
            
            for q in questions:
                with st.expander(f"**{q.get('title', 'Question')}** - {q.get('marks', 0)} Marks"):
                    st.write(q.get('description', ''))
                    st.caption("AI Feedback: Students mostly understood this concept.")

        # --- Tab 2: Student Performance ---
        with tab_student:
            st.subheader("Individual Results")
            
            # === KHẮC PHỤC LỖI KEY ERROR Ở ĐÂY ===
            roster = st.session_state.get("student_roster", [])
            
            # Tạo danh sách tên để hiển thị trong Selectbox
            # Logic: Ưu tiên 'student_name', nếu không có thì lấy 'name', mặc định 'Unknown'
            student_options = {}
            for s in roster:
                s_id = s.get('student_id', s.get('id', 'unknown'))
                s_name = s.get('student_name', s.get('name', 'Unknown'))
                
                if s_id != 'none':
                    label = f"{s_name} ({s_id})"
                    student_options[label] = s

            if not student_options:
                st.info("No students found.")
            else:
                selected_label = st.selectbox("Select Student", list(student_options.keys()))
                selected_student = student_options[selected_label]
                
                st.divider()
                col_pdf, col_grade = st.columns(2)
                
                with col_pdf:
                    st.write("**Exam Paper**")
                    file_url = selected_student.get('file_url', selected_student.get('file'))
                    if file_url:
                        st.info(f"Viewing file: {file_url}")
                        st.image("https://i.imgur.com/gKk9Nf2.png", caption="Mock Preview")
                    else:
                        st.warning("No file uploaded.")

                with col_grade:
                    st.write("**Grading Details**")
                    # Lặp qua các câu hỏi để hiện điểm giả lập
                    for q in st.session_state.get("processed_questions", []):
                        with st.expander(f"{q.get('title', 'Q')} ({q.get('marks')} pts)"):
                            st.write("**Score:** 8.0 (Mock)")
                            st.write("**Feedback:** Good understanding.")