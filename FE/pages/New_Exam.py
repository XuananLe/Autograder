import streamlit as st
from services import api 
from tabs import info_tab, rubric_tab, answers_tab, grading_tab

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Exam Editor")

# --- 2. KHỞI TẠO UI STATE ---
if 'edit_title_mode' not in st.session_state:
    st.session_state.edit_title_mode = False
if "show_toast" in st.session_state:
    st.toast(st.session_state.show_toast, icon="🎉")
    del st.session_state.show_toast

# State điều hướng (Navigation)
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# --- 3. LOGIC LOAD DỮ LIỆU TỪ API ---
if "current_exam_id" not in st.session_state:
    st.warning("Chưa chọn bài thi nào. Vui lòng quay lại Dashboard.")
    # Lưu ý: Đảm bảo tên file Dashboard của bạn đúng (ví dụ: Teacher_Dashboard.py)
    if st.button("Quay lại Dashboard"):
        st.switch_page("Home.py")
    st.stop()

current_exam_id = st.session_state.current_exam_id

# Hàm helper để load dữ liệu và map vào session_state
def load_exam_data(exam_id):
    exam = api.get_exam_detail(exam_id)
    roster = api.get_roster(exam_id)

    if exam:
        st.session_state.exam_name = exam.get("title", "Untitled Exam")
        st.session_state.exam_data = exam
        
        # Logic xác định trạng thái Rubric
        questions = exam.get("questions", [])
        st.session_state.processed_questions = questions
        
        if questions:
            st.session_state.rubric_status = "processed"
            st.session_state.rubric_complete = True
        else:
            if st.session_state.get("rubric_status") != "configuring":
                st.session_state.rubric_status = "uploading"
            st.session_state.rubric_complete = False
            
        # Logic xác định trạng thái Info
        if exam.get("course_title") or exam.get("course_name"):
            st.session_state.info_complete = True
        else:
            st.session_state.info_complete = False

    if roster is not None:
        st.session_state.student_roster = roster
        
        has_processed = any(s.get("status") == "processed" for s in roster)
        has_graded = any(s.get("status") == "graded" for s in roster)
        
        if has_graded:
            st.session_state.answers_status = "processed"
            st.session_state.answers_processing_complete = True
            st.session_state.grading_status = "processed"
        elif has_processed:
            st.session_state.answers_status = "processed"
            st.session_state.answers_processing_complete = True
            st.session_state.grading_status = "configuring"
        else:
            st.session_state.answers_status = "pending"
            st.session_state.answers_processing_complete = False
            st.session_state.grading_status = "configuring"

# --- TRIGGER LOAD DATA ---
if (st.session_state.get("loaded_exam_id") != current_exam_id) or st.session_state.get("force_reload"):
    with st.spinner("Đang tải dữ liệu..."):
        load_exam_data(current_exam_id)
        st.session_state.loaded_exam_id = current_exam_id
        st.session_state.force_reload = False 

# --- 4. HEADER & TITLE EDITING ---
col_header, col_edit_btn = st.columns([8, 1])

with col_header:
    if st.session_state.edit_title_mode:
        new_title = st.text_input(
            "Tên bài thi", 
            value=st.session_state.exam_name, 
            label_visibility="collapsed"
        )
    else:
        st.title(st.session_state.exam_name)

with col_edit_btn:
    st.write("") 
    st.write("") 
    if st.session_state.edit_title_mode:
        if st.button("💾", help="Lưu tên"):
            if api.update_exam_info(current_exam_id, {"title": new_title}):
                st.session_state.exam_name = new_title
                st.session_state.edit_title_mode = False
                st.toast("Đã cập nhật tên!", icon="✅")
                st.rerun()
            else:
                st.error("Lỗi khi cập nhật tên.")
    else:
        if st.button("✏️", help="Sửa tên"):
            st.session_state.edit_title_mode = True
            st.rerun()

# --- 5. THANH ĐIỀU HƯỚNG (WIZARD PROGRESS BAR) ---
# Dùng cái này thay cho st.tabs để tránh lỗi lặp giao diện và lỗi phiên bản
steps = ["1. Info", "2. Rubric", "3. Answers", "4. Grading"]
current_step_idx = st.session_state.current_step

st.progress((current_step_idx + 1) / 4)

cols = st.columns(4)
for i, step_name in enumerate(steps):
    btn_type = "primary" if i == current_step_idx else "secondary"
    
    is_disabled = False
    if i > 0 and not st.session_state.get("info_complete", False): is_disabled = True
    if i > 1 and not st.session_state.get("rubric_complete", False): is_disabled = True
    if i > 2 and not st.session_state.get("answers_processing_complete", False): is_disabled = True
    if i == current_step_idx: is_disabled = True # Đang ở bước này thì không cần bấm

    if cols[i].button(step_name, key=f"nav_step_{i}", type=btn_type, use_container_width=True, disabled=is_disabled):
        st.session_state.current_step = i
        st.rerun()

st.divider()

# --- 6. RENDER CONTENT (CHỈ RENDER 1 MÀN HÌNH DUY NHẤT) ---
if current_step_idx == 0:
    info_tab.render()
elif current_step_idx == 1:
    rubric_tab.render()
elif current_step_idx == 2:
    answers_tab.render()
elif current_step_idx == 3:
    grading_tab.render()

# --- 7. FOOTER NAVIGATION LOGIC ---
st.divider()
col1, col2 = st.columns([4, 1])

def nextStep(msg):
    if st.session_state.current_step < 3:
        st.session_state.current_step += 1
        st.session_state.show_toast = msg
        st.rerun()

# Hiển thị nút Next ở cuối trang
if current_step_idx == 0: # Info
    with col2:
        if st.button("Tiếp theo: Rubric →", type="primary", use_container_width=True, 
                     disabled=(not st.session_state.get("info_complete", False))):
            nextStep("Đã lưu Info! Chuyển sang Rubric.")

elif current_step_idx == 1: # Rubric
    with col1:
        if st.session_state.rubric_status == "processed":
            st.button("⤓ Tải Rubric", key="footer_dl_rubric")
    with col2:
        ready = st.session_state.get("rubric_status") == "processed"
        if st.button("Tiếp theo: Bài làm SV →", type="primary", use_container_width=True, disabled=not ready):
            st.session_state.rubric_complete = True
            nextStep("Đã xong Rubric! Chuyển sang Bài làm.")

elif current_step_idx == 2: # Answers
    with col1:
        if st.button("⟲ Reset"):
            st.session_state.answers_status = "pending"
            st.session_state.answers_processing_complete = False
            st.rerun()
    with col2:
        ready = st.session_state.get("answers_processing_complete", False)
        if st.button("Tiếp theo: Chấm điểm →", type="primary", use_container_width=True, disabled=not ready):
            nextStep("Đã xử lý xong! Chuyển sang Chấm điểm.")

elif current_step_idx == 3: # Grading
    with col1:
        st.button("⤓ Tải Báo cáo")
    with col2:
        is_graded = st.session_state.get("grading_status") == "processed"
        if st.button("Hoàn tất ✓", type="primary", use_container_width=True, disabled=not is_graded):
            st.switch_page("Home.py")