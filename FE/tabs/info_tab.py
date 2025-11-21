import streamlit as st
from services import api
def render():
    """Vẽ nội dung của tab Info"""
    exam_id = st.session_state.get("current_exam_id")
    current_data = st.session_state.get("exam_data", {})
    with st.form("info_form"):
        st.subheader("Info")
        st.caption("Configure the info for this exam")
        
        col1, col2 = st.columns(2)
        with col1:
            inst = st.text_input("Institute", value=current_data.get('institute', ''))
            dept = st.text_input("Department", value=current_data.get('department', ''))
            course_title = st.text_input("Course Title", value=current_data.get('course_title', ''))
        with col2:
            course_level = st.text_input("Course Level", value=current_data.get('course_level', ''))
            sub = st.text_input("Subject", value=current_data.get('subject', ''))
            date = st.text_input("Date", value=current_data.get('date', ''))
        date_due = st.text_input("Due", value=current_data.get('date_due', ''))
        if st.form_submit_button("Save & Unlock Rubric"):
            # Ghi vào state để mở khóa tab tiếp theo
            payload = {
                "institute": inst,
                "department": dept,
                "course_title": course_title,
                "course_level": course_level,
                "sub":sub,
                "date":date,
                "date_due":date_due
            }
            success = api.update_exam_info(exam_id, payload)
            
            if success:
                st.session_state.info_complete = True
                st.success("Saved successfully!")
                st.session_state.force_reload = True # Đánh dấu để reload lại data mới
            else:
                st.error("Failed to save.")
