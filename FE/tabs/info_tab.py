import streamlit as st

def render():
    """Vẽ nội dung của tab Info"""
    with st.form("info_form"):
        st.subheader("Info")
        st.caption("Configure the info for this exam")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Institute", "Zanista University")
            st.text_input("Department", "Mathematics")
            st.text_input("Course Title", "Biomechanics")
        with col2:
            st.selectbox("Course Level", ["Undergraduate", "Postgraduate"])
            st.text_input("Subject", "Bone Mechanics")
            st.date_input("Date")

        if st.form_submit_button("Save & Unlock Rubric"):
            # Ghi vào state để mở khóa tab tiếp theo
            st.session_state.info_complete = True 
