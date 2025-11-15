# Home.py
import streamlit as st

st.set_page_config(
    page_title="Autograder Home",
    layout="centered"
)


st.title("Chào mừng đến với Autograder")
st.write("Vui lòng chọn giao diện của bạn:")

col1, col2 = st.columns(2)

with col1:
    # Dùng st.button, không dùng st.link_button
    if st.button("🧑‍🏫 Teacher View", use_container_width=True):
        st.switch_page("pages/Teacher_Dashboard.py") # <-- Chuyển trang
    
with col2:
    if st.button("🎓 Student View", use_container_width=True):
        st.switch_page("pages/Student_Dashboard.py") # <-- Chuyển trang