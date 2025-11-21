import streamlit as st
import time
from services import api

def render():
    """
    Vẽ (render) toàn bộ nội dung cho tab Rubric.
    """
    
    # 1. Lấy Context hiện tại
    exam_id = st.session_state.get("current_exam_id")
    if not exam_id:
        st.error("Exam ID not found.")
        return

    # 2. GUARD: Kiểm tra xem đã xong Tab Info chưa
    if not st.session_state.get("info_complete", False):
        st.warning("Please complete and save the 'Info' tab first.")
        return
    
    # ---------------------------------------------------------
    # TRẠNG THÁI 1: UPLOADING (Chưa có file)
    # ---------------------------------------------------------
    if st.session_state.rubric_status == "uploading":
        st.subheader("Upload Rubric")
        st.caption("Upload the exam question paper or rubric (PDF).")
        
        uploaded_file = st.file_uploader("Upload Rubric (.pdf)", type=["pdf"])
        
        if uploaded_file:
            with st.spinner("Uploading file to server..."):
                upload_resp = api.upload_file(uploaded_file)
                
                if upload_resp:
                    st.session_state.rubric_status = "configuring"
                    st.session_state.uploaded_file_name = upload_resp.get('filename', uploaded_file.name)
                    
                    # --- FIX: Đồng bộ Step ---
                    st.session_state.current_step = 1 
                    
                    st.rerun()
                else:
                    st.error("Failed to upload file. Please try again.")

    # ---------------------------------------------------------
    # TRẠNG THÁI 2: CONFIGURING (Đã có file, chờ xử lý)
    # ---------------------------------------------------------
    elif st.session_state.rubric_status == "configuring":
        st.subheader("Configure Rubric Options")
        
        file_name = st.session_state.get('uploaded_file_name', 'Uploaded File')
        st.info(f"File ready: **{file_name}**", icon="📄")
        
        with st.form("rubric_options_form"):
            st.write("**AI Processing Configuration**")
            col1, col2 = st.columns(2)
            with col1:
                submission_type = st.selectbox("Submission Type", ["Typed", "Handwritten"])
                ocr_method = st.selectbox("OCR Engine", ["Azure AI Vision", "Google Cloud Vision"], key="rub_ocr")
            with col2:
                gpt_model = st.selectbox("LLM Model", ["OpenAI: GPT-4o", "OpenAI: GPT-4-Turbo"], key="rub_gpt")
                detail_level = st.selectbox("Detail Level", ["Standard", "Detailed Steps"])

            st.caption("The AI will extract questions, marks, and grading criteria automatically.")
            
            if st.form_submit_button("Begin Processing →", type="primary"):
                
                payload = {
                    "submission_type": submission_type,
                    "ocr_method": ocr_method,
                    "gpt_model": gpt_model,
                    "detail_level": detail_level
                }

                with st.spinner("Sending request to AI Server..."):
                    success = api.process_rubric(exam_id, payload)
                    
                    if success:
                        st.session_state.rubric_status = "processed"
                        st.session_state.force_reload = True
                        
                        # --- FIX: ĐỒNG BỘ STEP ---
                        # Ép footer chuyển sang bước 1 (Rubric Footer)
                        # Để nút "Next: Student Answers" hiện ra và bấm được
                        st.session_state.current_step = 1 
                        
                        st.success("Processing complete! Loading results...")
                        time.sleep(1) 
                        st.rerun()
                    else:
                        st.error("Server Error: Could not process rubric.")

    # ---------------------------------------------------------
    # TRẠNG THÁI 3: PROCESSED (Hiển thị & Chỉnh sửa)
    # ---------------------------------------------------------
    elif st.session_state.rubric_status == "processed":
        
        questions = st.session_state.get("processed_questions", [])
        
        cols_header = st.columns([2, 3])
        with cols_header[0]:
            st.subheader("Rubric Content")
        with cols_header[1]:
            st.caption("Review and edit the AI-generated grading criteria.")

        total_marks = sum(q.get('marks', 0) for q in questions)
        st.markdown(f"**Total Questions:** {len(questions)} &nbsp; | &nbsp; **Total Marks:** {total_marks}", unsafe_allow_html=True)
        st.divider()

        if len(questions) == 0:
            st.warning("No questions found. The AI might have failed to extract data.")
            if st.button("Try Again"):
                st.session_state.rubric_status = "configuring"
                st.rerun()
            return

        for i, q in enumerate(questions):
            label = f"**{q.get('title', f'Question {i+1}')}** ({q.get('marks', 0)} Marks)"
            
            with st.expander(label, expanded=False):
                st.markdown("**Question Description**")
                st.write(q.get('description', 'No description available.'))
                st.markdown("---")
                
                st.markdown("**Grading Steps (Criteria)**")
                steps = q.get('steps', [])
                
                for step in steps:
                    step_title = f"{step.get('title', 'Untitled Step')} ({step.get('marks', 0)} Marks)"
                    
                    with st.expander(step_title):
                        t_sol, t_exp, t_err, t_mark = st.tabs(["Solution", "Expectation", "Common Errors", "Marking"])
                        
                        def render_field(tab, key_name, display_name):
                            with tab:
                                widget_key = f"txt_{q['id']}_{step['id']}_{key_name}"
                                current_val = step['content'].get(key_name, "")
                                new_val = st.text_area(
                                    f"Edit {display_name}", 
                                    value=current_val, 
                                    height=150,
                                    key=widget_key
                                )
                                if new_val != current_val:
                                    step['content'][key_name] = new_val

                        render_field(t_sol, "solution", "Solution")
                        render_field(t_exp, "expectation", "Expectation")
                        render_field(t_err, "common_errors", "Common Errors")
                        render_field(t_mark, "marking", "Marking Rules")

                st.divider()

                with st.form(key=f"mark_form_{q['id']}"):
                    col_mark_1, col_mark_2 = st.columns([3, 1])
                    with col_mark_1:
                        st.write("**Edit Total Marks for this Question**")
                    with col_mark_2:
                        new_marks = st.number_input("Marks", value=float(q.get('marks', 0)), step=0.5, label_visibility="collapsed")
                    
                    if st.form_submit_button("Update Marks"):
                        st.session_state.processed_questions[i]['marks'] = new_marks
                        
                        if api.update_rubric(exam_id, st.session_state.processed_questions):
                            st.toast(f"Updated {q['title']} marks!", icon="✅")
                            st.session_state.force_reload = True
                            
                            # --- FIX: Đồng bộ Step ---
                            st.session_state.current_step = 1
                            
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Failed to update marks.")

        col_action_1, col_action_2 = st.columns([4, 1])
        
        with col_action_1:
             if st.button("⟲ Reset / Upload New File"):
                st.session_state.rubric_status = "configuring"
                st.session_state.rubric_complete = False
                st.rerun()

        with col_action_2:
            if st.button("💾 Save All Changes", type="primary", use_container_width=True):
                with st.spinner("Saving changes to database..."):
                    if api.update_rubric(exam_id, st.session_state.processed_questions):
                        st.success("Rubric saved successfully!")
                        st.session_state.force_reload = True
                        
                        # --- FIX: Đồng bộ Step ---
                        st.session_state.current_step = 1
                        st.rerun()
                    else:
                        st.error("Failed to save changes.")