# app_tabs/rubric_tab.py
import streamlit as st
import time

def render():
    """
    Vẽ (render) toàn bộ nội dung cho tab Rubric.
    """
    
    # --- 1. KHÓA TAB ---
    if not st.session_state.get("info_complete", False):
        st.warning("Vui lòng hoàn thành và lưu tab 'Info' trước.")
        return
    
    # --- 2. LOGIC 3 TRẠNG THÁI ---
    
    # TRẠNG THÁI 1: UPLOADING
    if st.session_state.rubric_status == "uploading":
        st.subheader("Upload Rubric")
        uploaded_file = st.file_uploader("Upload Rubric (.pdf)", type=["pdf"])
        if uploaded_file:
            st.session_state.rubric_status = "configuring"
            st.session_state.uploaded_file_name = uploaded_file.name
            st.rerun()

    # TRẠNG THÁI 2: CONFIGURING
    elif st.session_state.rubric_status == "configuring":
        st.subheader("Configure Rubric Options")
        st.info(f"File đã tải lên: **{st.session_state.get('uploaded_file_name', '...')}**")
        
        with st.form("rubric_options_form"):
            st.selectbox("Submission Type", ["Typed", "Handwritten"])
            with st.expander("» Advanced"):
                st.selectbox("OCR Method", ["Azure Vision", "Google Vision"], key="rub_ocr")
                st.selectbox("GPT Model", ["OpenAI: GPT-4o", "OpenAI: GPT-4"], key="rub_gpt")

            if st.form_submit_button("Begin Processing →", type="primary"):
                with st.spinner("Đang xử lý Rubric..."):
                    time.sleep(2)
                st.session_state.rubric_status = "processed"
                st.rerun()

    # TRẠNG THÁI 3: PROCESSED (MÀN HÌNH CHÍNH)
    elif st.session_state.rubric_status == "processed":
        
        # --- Header ---
        cols_header = st.columns([2, 3])
        with cols_header[0]:
            st.subheader("Rubric")
        with cols_header[1]:
            st.caption("Overview of the exam rubric")

        # --- Sub-tabs ---
        sub_tab_ai, sub_tab_orig = st.tabs(["📄 Enhanced with AI", "🧾 Original"])
        
        with sub_tab_ai:
            
            # --- Toolbar ---
            total_marks = sum(q['marks'] for q in st.session_state.processed_questions)
            cols_toolbar = st.columns([2, 3, 2])
            cols_toolbar[0].write(f"{len(st.session_state.processed_questions)} Questions | Total Marks: {total_marks}")
            cols_toolbar[1].text_input("Search...", placeholder="🔍 Search...", label_visibility="collapsed")
            cols_toolbar[2].write(":: Expand  /  Collapse")

            # --- Danh sách câu hỏi (Question List) ---
            for i, q in enumerate(st.session_state.processed_questions):
                
                dynamic_label = f"**> {q['title']}** ({q['marks']} Marks)"
                
                with st.expander(dynamic_label):
                    
                    # === PHẦN 1: NỘI DUNG (Nằm NGOÀI Form) ===
                    
                    # Question Content
                    st.markdown(f"**Question Content:**")
                    st.write(q['description'])
                    
                    st.markdown("---")
                    
                    # Step-by-Step (Editable)
                    st.markdown("**Step-by-Step** (Generated with AI)")
                    
                    for step in q['steps']:
                        with st.expander(f"**> {step['title']}** ({step['marks']} Marks)"):
                            
                            # Tabs
                            step_tabs = st.tabs(["Solution", "Expectation", "Common Errors", "Marking"])
                            
                            # Hàm helper vẽ nội dung
                            def render_editable_content(tab, content_key, step_id, label):
                                with tab:
                                    edit_key = f"edit_mode_{step_id}_{content_key}"
                                    if edit_key not in st.session_state:
                                        st.session_state[edit_key] = False

                                    col_content, col_btn = st.columns([9, 1])
                                    
                                    # Nút Edit/View (Bây giờ đã an toàn vì ở ngoài form)
                                    with col_btn:
                                        if st.session_state[edit_key]:
                                            if st.button("👁️", key=f"btn_view_{edit_key}", help="Switch to View Mode"):
                                                st.session_state[edit_key] = False
                                                st.rerun()
                                        else:
                                            if st.button("✏️", key=f"btn_edit_{edit_key}", help="Edit Content"):
                                                st.session_state[edit_key] = True
                                                st.rerun()

                                    # Nội dung
                                    with col_content:
                                        current_content = step['content'][content_key]
                                        if st.session_state[edit_key]:
                                            new_content = st.text_area(
                                                f"Edit {label}", 
                                                value=current_content,
                                                height=200,
                                                key=f"input_{edit_key}"
                                            )
                                            if new_content != current_content:
                                                step['content'][content_key] = new_content
                                        else:
                                            st.markdown(current_content, unsafe_allow_html=True)

                            # Gọi hàm helper
                            render_editable_content(step_tabs[0], 'solution', step['id'], "Solution")
                            render_editable_content(step_tabs[1], 'expectation', step['id'], "Expectation")
                            render_editable_content(step_tabs[2], 'common_errors', step['id'], "Common Errors")
                            render_editable_content(step_tabs[3], 'marking', step['id'], "Marking")
                    
                    st.divider()
                    
                    # === PHẦN 2: SỬA ĐIỂM (Nằm TRONG Form riêng) ===
                    # Chỉ bao quanh phần sửa điểm bằng form để tránh xung đột button
                    with st.form(key=f"form_q_{q['id']}"):
                        st.subheader("Edit Question Marks")
                        new_marks = st.number_input(
                            "Total Marks for this Question", 
                            value=q['marks'], 
                            min_value=0, 
                            step=1
                        )
                        
                        if st.form_submit_button("Update Marks"):
                            st.session_state.processed_questions[i]['marks'] = new_marks
                            st.success(f"{q['title']} updated to {new_marks} marks!")
                            st.rerun()

        with sub_tab_orig:
            st.write("Nội dung Rubric gốc (Original) ở đây...")

        # --- Nút Reset ---
        if st.button("⟲ Reset rubric?"):
            st.session_state.rubric_status = "configuring"
            st.session_state.rubric_complete = False 
            st.rerun()