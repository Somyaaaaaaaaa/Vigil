import streamlit as st
import pandas as pd
from datetime import datetime, date
import database as db

def show():
    st.markdown("""
        <style>
        .stCheckbox p { font-family: 'Courier New', monospace; font-size: 16px; letter-spacing: 1px; }
        div.stButton > button {
            border: 1px solid #ff4b4b !important;
            color: #ff4b4b !important;
            background: transparent;
            text-transform: uppercase;
            letter-spacing: 2px;
            width: 100%;
        }
        div.stButton > button:hover {
            background: rgba(255, 75, 75, 0.1) !important;
            box-shadow: 0px 0px 10px #ff4b4b;
        }
        div[data-baseweb="select"]:hover, 
        div[data-baseweb="base-input"]:hover {
            border-bottom: 1px solid #00e5ff !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("◈ The Hit List")
    st.caption("ACTIVE ENGAGEMENT // SELECT DATE")

    # ui controls
    col1, col2 = st.columns([1, 2])

    with col1:
        target_date = st.date_input(
            "TARGET_DATE",
            value=date.today(),
            key="task_date",
            label_visibility="collapsed"
        )
    
    def add_task_and_clear():
        task = st.session_state.task_input
        selected_date = st.session_state.task_date
        if not task or not task.strip():
            st.warning("You tried to submit nothing. Revolutionary.")
            return

        task = task.strip()
        db.add_task(task, str(selected_date), False)
    
    st.text_input(
        "Target",
        key="task_input",
        placeholder="Enter objective designation",
        on_change=add_task_and_clear # Trigger add on 'Enter' key
    )

    st.button("Confirm hit", on_click=add_task_and_clear)

    st.write("---")

    # display logic
    tasks = db.load_tasks_by_date(target_date)

    if tasks:
        for t in tasks:
            task_text = t[2] 
            is_done = bool(t[4])  

            prefix = "✓" if is_done else "⌖"
            label = f"{prefix} {task_text.upper()}"
            if is_done:
                label = f"~~{label}~~"

            col_check, col_del = st.columns([6, 1])
            
            with col_check:
                checked = st.checkbox(
                    label,
                    value=is_done,
                    key=f"task_chk_{t[0]}"
                )

                if checked != is_done:
                    db.update_task_status(t[0], checked)

            with col_del:
                if st.button("⊝", key=f"task_del_{t[0]}"):
                    db.delete_task(t[0])
                    st.rerun()  
    else:
        st.info("NO active targets for this date.")

