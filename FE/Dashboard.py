# 1_Dashboard.py
import streamlit as st

st.set_page_config(
    page_title="GoodPoint Dashboard",
    layout="centered"
)

st.title("GoodPoint")
st.caption("Create a new exam or select a previous one")

# Nút "New Exam" sẽ tự động điều hướng đến file "pages/2_New_Exam.py"
# Chúng ta dùng st.page_link (Streamlit 1.33+)
st.page_link("pages/New_Exam.py", label="+ New Exam", use_container_width=True, icon="📄")

st.divider()

# --- Hiển thị các Exam (Dùng st.expander) ---
st.subheader("Ongoing Exams")
with st.container(border=True):
    cols = st.columns([3, 2, 1])
    cols[0].write("**Yr 7 Maths**")
    cols[1].write("19 May 2025")
    cols[2].button("Upload", key="upload_maths") # Nút này chỉ là giả

st.subheader("Graded Exams")
with st.container(border=True):
    cols = st.columns([3, 2, 1])
    cols[0].write("**Old Exam**")
    cols[1].write("18 May 2025")
    cols[2].success("Graded") # Dùng st.success cho đẹp