# pages/2_New_Exam.py
import streamlit as st
import time
from tabs import info_tab, rubric_tab, answers_tab, grading_tab

if 'exam_name' not in st.session_state:
    st.session_state.exam_name = "Exam 1" # Tên mặc định
if 'edit_title_mode' not in st.session_state:
    st.session_state.edit_title_mode = False
if "show_toast" in st.session_state:
    st.toast(st.session_state.show_toast, icon="🎉")
    del st.session_state.show_toast
st.set_page_config(layout="wide")
    
# --- QUẢN LÝ TRẠNG THÁI (State Management) ---
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'info_complete' not in st.session_state:
    st.session_state.info_complete = False
    
    
if 'rubric_complete' not in st.session_state:
    st.session_state.rubric_complete = False
if 'rubric_status' not in st.session_state:
    st.session_state.rubric_status = "uploading"
    
    
if 'answers_status' not in st.session_state:
    st.session_state.answers_status = "pending"
if 'answers_processing_complete' not in st.session_state:
    st.session_state.answers_processing_complete = False
if 'grading_complete' not in st.session_state:
    st.session_state.grading_complete = False
    
if 'grading_status' not in st.session_state:
    st.session_state.grading_status = "configuring"
    
               
if 'student_roster' not in st.session_state:
    st.session_state.student_roster = [
        {
            "id": "23021668", 
            "name": "Nguyễn Thị Phương", 
            "email": "nguyenthiphuong2k5nb@gmail.com", 
            "file": "nguyenthiphuong.pdf", # Giả lập là đã gán file
            "processed_content": {
                "question_1_text": "Student Answer (Text) for Q1:\nFor $b > 1/2$ and $b < I_a < 5b - 1$.",
                "question_1_latex": "Student Answer (LaTeX) for Q1:\n\\text{For } b > \\frac{1}{2} \\text{ and } b < I_a < 5b - 1."
            }
        },
        {
            "id": "23021669", 
            "name": "Trần Văn An", 
            "email": "tranvanan@gmail.com", 
            "file": "tranvanan.pdf",
            "processed_content": {
                "question_1_text": "Student Answer (Text) for Q2:\n...",
                "question_1_latex": "Student Answer (LaTeX) for Q2:\n..."
            }
        },
        {
            "id": "none", 
            "name": "none", 
            "email": "none", 
            "file": None,
            "processed_content": None
        }
    ]
if 'processed_questions' not in st.session_state:
    st.session_state.processed_questions = [
        { 
            "id": "q1", 
            "title": "Question 1", 
            "marks": 20, 
            "description": "Suppose the temporal activity of the space-clamped nerve axon is modelled with the two variable FitzHugh-Nagumo model...",
            "steps": [
                { 
                    "id": "s1-1", 
                    "title": "Step 1: Establish the equations governing the FitzHugh-Nagumo model and define critical terms.", 
                    "marks": 5,
                    "content": {
                        "solution": """
                        **Solution:**<br>
                        We begin with the given equations of the FitzHugh-Nagumo model:
                        $$
                        \\frac{dv}{dt} = f(v) - w + I_a, \quad \\frac{dw}{dt} = b v - \gamma w
                        $$
                        and the piecewise function:
                        $$
                        f(v) = \\begin{cases} -v, & \\text{for } v \le 1 \\\\ v - \\frac{3}{2}, & \\text{for } 1 \le v \le 5 \\\\ 6 - v, & \\text{for } v \ge 5 \\end{cases}
                        $$
                        """,
                        "expectation": """
                        **Expectation:**<br>
                        - Student must correctly state both differential equations.
                        - Student must correctly write all three parts of the piecewise function $f(v)$.
                        """,
                        "common_errors": """
                        **Common Errors:**<br>
                        - Mixing up variables $v$ and $w$.
                        - Incorrect signs in the piecewise function.
                        """,
                        "marking": """
                        **Marking:**<br>
                        - **[2 Marks]** Correctly stating both $\\frac{dv}{dt}$ and $\\frac{dw}{dt}$.
                        - **[3 Marks]** Correctly defining all three conditions for $f(v)$.
                        """
                    }
                },
                { 
                    "id": "s1-2", 
                    "title": "Step 2: Analyze the slope criteria and derive the range for the parameter $b$.", 
                    "marks": 5,
                    "content": {
                        "solution": "Solution for Step 1.2...",
                        "expectation": "Expectation for Step 1.2...",
                        "common_errors": "Common Errors for Step 1.2...",
                        "marking": "Marking criteria for Step 1.2..."
                    }
                },
                { 
                    "id": "s1-3", 
                    "title": "Step 3: Assess conditions on points relative to the $bv-w$ equilibrium line...", 
                    "marks": 5,
                    "content": { "solution": "Solution for Step 1.3...", "expectation": "...", "common_errors": "...", "marking": "..." }
                },
                { 
                    "id": "s1-4", 
                    "title": "Step 4: Combine all derived conditions and synthesize the final parameter range...", 
                    "marks": 5,
                    "content": { "solution": "Solution for Step 1.4...", "expectation": "...", "common_errors": "...", "marking": "..." }
                },
            ],
            "grading_data": {
                "average_str": "7.6/10.0 (75.6%) Grade B",
                "statistics": {
                    "Average marks": "7.6/10.0 (75.6%) Grade B",
                    "Highest mark": "9.5/10.0 (95.0%) Grade A+",
                    "Lowest mark": "0.0/10.0 (0.0%) Grade F",
                    "Attempted by": "16 students"
                },
                "feedback": "The students demonstrated a good understanding of Question 1's concepts as evidenced by their solutions... (fake text)..."
            },
        },
        { 
            "id": "q2", 
            "title": "Question 2", 
            "marks": 20, 
            "description": "This is the description for Question 2. It involves different concepts.",
            "steps": [
                { 
                    "id": "s2-1", 
                    "title": "Step 1 (Q2): Define the problem context.", 
                    "marks": 10,
                    "content": {
                        "solution": "<strong>Solution (Q2):</strong><br>This is the solution for Question 2, Step 1.",
                        "expectation": "<strong>Expectation (Q2):</strong><br>Students must define the context.",
                        "common_errors": "<strong>Common Errors (Q2):</strong><br>Forgetting units.",
                        "marking": "<strong>Marking (Q2):</strong><br>10 marks for correct definition."
                    }
                },
                { 
                    "id": "s2-2", 
                    "title": "Step 2 (Q2): Apply the formula.", 
                    "marks": 10,
                    "content": { "solution": "Solution for Step 2.2...", "expectation": "...", "common_errors": "...", "marking": "..." }
                },
            ],
            "grading_data": {
                "average_str": "8.8/10.0 (88.0%) Grade A",
                "statistics": {
                    "Average marks": "8.8/10.0 (88.0%) Grade A",
                    "Highest mark": "10.0/10.0 (100%) Grade A+",
                    "Lowest mark": "5.0/10.0 (50.0%) Grade D",
                    "Attempted by": "16 students"
                },
                "feedback": "Feedback for Question 2... (fake text)..."
            }
        },
    ]

col_header, col_edit_btn = st.columns([8, 1])

with col_header:
    if st.session_state.edit_title_mode:
        # CHẾ ĐỘ SỬA: Hiển thị ô nhập liệu
        new_title = st.text_input(
            "Enter Exam Name", 
            value=st.session_state.exam_name, 
            label_visibility="collapsed" # Ẩn nhãn cho đẹp
        )
    else:
        # CHẾ ĐỘ XEM: Hiển thị Title bình thường
        st.title(st.session_state.exam_name)

with col_edit_btn:
    # Căn chỉnh nút bấm xuống dưới một chút cho thẳng hàng với Title
    st.write("") 
    st.write("") 
    
    if st.session_state.edit_title_mode:
        # Nút LƯU
        if st.button("💾", help="Save Title"):
            st.session_state.exam_name = new_title # Cập nhật tên mới
            st.session_state.edit_title_mode = False # Tắt chế độ sửa
            st.rerun()
    else:
        # Nút SỬA
        if st.button("✏️", help="Edit Title"):
            st.session_state.edit_title_mode = True # Bật chế độ sửa
            st.rerun()

# --- VẼ CÁC TABS (Giao diện chính) ---
tab_info, tab_rubric, tab_answers, tab_grading = st.tabs([
    "Info ℹ️", 
    "Rubric 📄", 
    "Student answers 🎓", 
    "Grading 📊"
])

# 3. Gọi hàm render() của mỗi tab
with tab_info:
    info_tab.render()

with tab_rubric:
    rubric_tab.render()

with tab_answers:
    answers_tab.render()

with tab_grading:
    grading_tab.render()


st.divider()

def nextStep(toast_message): # Thêm một tham số
    if st.session_state.current_step < 3:
        st.session_state.current_step += 1
        
        # THAY ĐỔI: Đặt "flag" thay vì gọi st.toast
        st.session_state.show_toast = toast_message 
        
        st.rerun() 

# SỬA ĐỔI: Hàm finish_exam
def finish_exam():
    # THAY ĐỔI: Đặt "flag" cho trang Dashboard
    st.session_state.show_toast = "Exam setup complete! 🎉"
    
    # st.success và time.sleep sẽ không chạy,
    # st.switch_page sẽ chuyển trang ngay lập tức
    st.switch_page("Dashboard.py") # Quay về trang chủ

if st.session_state.current_step == 0: # Tab Info
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Next: Rubric →", type="primary", use_container_width=True, 
                     disabled=(not st.session_state.info_complete)):
            nextStep("Info Saved! Rubric tab unlocked. 🔓")

elif st.session_state.current_step == 1: # Tab Rubric
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.rubric_status == "processed":
            
            # SỬA Ở ĐÂY: Thêm 'key' duy nhất
            st.button("⤓ Rubric Downloads", key="footer_download_rubric")
            
    with col2:
        if st.button("Next: Student answers →", type="primary", use_container_width=True,
                     key="footer_student_answers",disabled=(st.session_state.rubric_status != 'processed')):
            
            st.session_state.rubric_complete = True 
            nextStep("Rubric Processed! Student answers unlocked. 🔓")

elif st.session_state.current_step == 2: # Tab Student Answers
    col1, col2 = st.columns(2)
    with col1:
        # SỬA Ở ĐÂY: Thêm 'key' (Rất quan trọng cho các nút trong if/else)
        if st.button("⟲ Reset student answers?", key="footer_reset_answers"):
            
            st.session_state.answers_status = "pending"
            st.session_state.answers_processing_complete = False
            st.session_state.show_toast = "Student answers reset."
            st.rerun()
    with col2:
        if st.button("Next: Grading →", type="primary", use_container_width=True,
                     key="footer_grading",disabled=(not st.session_state.answers_processing_complete)):
            
            nextStep("Answers Finalized! Grading tab unlocked. 🔓")

elif st.session_state.current_step == 3: # Tab Grading (Mới)
    col1, col2 = st.columns(2)
    with col1:
        
        # SỬA Ở ĐÂY: Thêm 'key' duy nhất
        st.button("⤓ Grading Downloads", key="footer_download_grading")
        
    with col2:
        if st.button("Finish ✓", type="primary", use_container_width=True,
                     key="footer_finish", disabled=(st.session_state.grading_status != 'processed')):
            
            finish_exam()