import streamlit as st
import time

def render():
    """Vẽ nội dung của tab Rubric (3 trạng thái)"""
    
    # 1. Khóa tab nếu Info chưa xong
    if not st.session_state.get("info_complete", False):
        st.warning("Vui lòng hoàn thành và lưu tab 'Info' trước.")
        return # Dừng vẽ tab này
    
    # 2. Hiển thị dựa trên trạng thái của Rubric
    
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
        st.info(f"File đã tải lên: **{st.session_state.uploaded_file_name}**")
        
        with st.form("rubric_options_form"):
            st.selectbox("Submission Type", ["Typed", "Handwritten"])
            st.number_input("Default Marks", value=20)
            st.checkbox("Allow Half Marks", value=True)

            with st.expander("» Advanced"):
                st.selectbox("OCR Method", ["Azure Vision", "Google Vision"], key="rub_ocr")
                st.selectbox("GPT Model", ["OpenAI: GPT-4o", "OpenAI: GPT-4"], key="rub_gpt")

            if st.form_submit_button("Begin Processing →", type="primary"):
                with st.spinner("Đang xử lý Rubric..."):
                    time.sleep(2) 
                st.session_state.rubric_status = "processed"
                st.rerun()

    # TRẠNG THÁI 3: PROCESSED
    elif st.session_state.rubric_status == "processed":
        
        # --- Header (Rubric, Overview) ---
        cols_header = st.columns([2, 3])
        with cols_header[0]:
            st.subheader("Rubric")
        with cols_header[1]:
            st.caption("Overview of the exam rubric")

        # --- Sub-tabs (Enhanced, Original) ---
        sub_tab_ai, sub_tab_orig = st.tabs(["📄 Enhanced with AI", "🧾 Original"])
        
        with sub_tab_ai:
            
            # --- Toolbar (Total, Search, Expand) ---
            # Tính tổng điểm từ state
            total_marks = sum(q['marks'] for q in st.session_state.processed_questions)
            
            cols_toolbar = st.columns([2, 3, 2])
            cols_toolbar[0].write(f"{len(st.session_state.processed_questions)} Questions | Total Marks: {total_marks}")
            cols_toolbar[1].text_input("Search...", placeholder="🔍 Search...", label_visibility="collapsed")
            cols_toolbar[2].write(":: Expand  /  [Collapse](https://#)") # Dùng link markdown cho nút giả

            # --- Danh sách câu hỏi (Question List) ---
            for i, q in enumerate(st.session_state.processed_questions):
                
                # 1. Tạo label động từ state
                dynamic_label = f"**> {q['title']}** ({q['marks']} Marks)"
                
                with st.expander(dynamic_label):
                    
                    # 2. Form để chỉnh sửa điểm
                    with st.form(key=f"form_q_{q['id']}"):
                        
                        st.markdown(f"**Question Content:** {q['description']}")
                        st.markdown("---")
                        
                        # --- Step-by-Step lồng nhau ---
                        st.markdown("**Step-by-Step** (Generated with AI)")
                        for step in q['steps']:
                            with st.expander(f"**> {step['title']}** ({step['marks']} Marks)"):
                                
                                # Tabs (Solution, Expectation...)
                                sol_tab, exp_tab, err_tab, mark_tab = st.tabs(["Solution", "Expectation", "Common Errors", "Marking"])
                                
                                with sol_tab:
                                    st.markdown(step['content']['solution'], unsafe_allow_html=True)
                                with exp_tab:
                                    st.markdown(step['content']['expectation'], unsafe_allow_html=True)
                                with err_tab:
                                    st.markdown(step['content']['common_errors'], unsafe_allow_html=True)
                                with mark_tab:
                                    st.markdown(step['content']['marking'], unsafe_allow_html=True)
                        
                        st.divider()
                        
                        # --- PHẦN CHỈNH SỬA ĐIỂM ---
                        st.subheader("Edit Question Marks")
                        new_marks = st.number_input(
                            "Total Marks for this Question", 
                            value=q['marks'], 
                            min_value=0, 
                            step=1
                        )
                        
                        if st.form_submit_button("Update Marks"):
                            # Cập nhật điểm trong session state
                            st.session_state.processed_questions[i]['marks'] = new_marks
                            st.success(f"{q['title']} updated to {new_marks} marks!")
                            st.rerun() # Tải lại để cập nhật label

        with sub_tab_orig:
            st.write("Nội dung Rubric gốc (Original) ở đây...")

        # --- Nút Reset (nằm bên ngoài sub-tab) ---
        if st.button("⟲ Reset rubric?"):
            st.session_state.rubric_status = "configuring"
            st.session_state.rubric_complete = False 
            st.rerun()
        
        # # --- Footer (Hiển thị sau khi Processed) ---
        # st.divider() 
        # col_f1, col_f2 = st.columns(2)
        # with col_f1:
        #     st.button("⤓ Rubric Downloads")
        # with col_f2:
        #     # Nút "Next" này sẽ MỞ KHÓA tab "Student answers"
        #     if st.button("Next: Student answers →", type="primary", use_container_width=True):
        #         st.session_state.rubric_complete = True
        #         st.toast("Đã mở khóa! Vui lòng nhấp vào tab 'Student answers'.")