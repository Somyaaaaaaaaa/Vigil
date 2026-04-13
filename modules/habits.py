import streamlit as st
import pandas as pd
from datetime import datetime, date
import database as db

def show():
    # --- DIAGNOSTIC HUD STYLE ---
    st.markdown("""
        <style>
        section.main div[data-testid="stMarkdownContainer"] > p {
            font-family: 'Courier New', monospace;
            letter-spacing: 0.5px;
            font-size: 14px;
        }
        .stSlider [data-baseweb="slider"] { margin-top: 10px; }
        div[data-baseweb="select"]:hover, 
        div[data-baseweb="base-input"]:hover {
            border-bottom: 1px solid #00e5ff !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("◈ Biometric Log")
    st.caption("ASSET PERFORMANCE TRACKING // SYSTEM DIAGNOSTICS")

    habit_date = st.date_input("LOG PERIOD", value=date.today(), key="habit_date")

    st.subheader("Uptime Metrics")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        wake = st.time_input("Wake Signal")
    with col_t2:
        sleep = st.time_input("Sleep Signal")

    st.subheader("Physical Output")
    c1, c2 = st.columns(2)
    with c1:
        water = st.slider("Hydration Level (L)", 0.0, 5.0, 2.0)
        # Match case with analytics.py workout_map
        workout = st.selectbox("Intensity Level", ["None", "Light", "Moderate", "Intense"])
    with c2:
        steps = st.number_input("LOCOMOTION_STEPS", 0, 50000, 3000)
        # DEFINING WALK (Fixes the crash)
        walk = st.checkbox("OPTICAL_RECON_WALK?")

    st.subheader("Screen Time")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        hours = st.number_input("Hours", 0, 24, 1)
    with col_s2:
        minutes = st.number_input("Minutes", 0, 59, 0)
    screen_time = hours + (minutes / 60)

    st.subheader("Neural Load")
    mood = st.slider("Stability Index (MOOD)", 1, 10, 5)
    energy = st.slider("Reserve Power (ENERGY)", 1, 10, 5)
    focus = st.slider("Signal Clarity (FOCUS)", 1, 10, 5)

    st.subheader("Fuel Intake")
    f1, f2 = st.columns(2)
    with f1:
        meals = st.number_input("Primary meals", 0, 5, 2)
    with f2:
        snacks = st.number_input("Snacks", 0, 10, 1)

    night_issue = st.selectbox(
        "Sleep Distubances",
        ["NONE", "Nightmare", "Sleep Paralysis", "Dual Disturbance"]
    )

    conn = db.connect()
    if st.button("COMMIT TO LEDGER"):
        db.save_habits(
        str(habit_date),
        wake.strftime("%H:%M"),
        sleep.strftime("%H:%M"),
        water, 
        steps, 
        workout, 
        walk,
        screen_time, 
        mood, 
        energy, 
        focus,
        meals, 
        snacks, 
        night_issue
    )
        
        st.toast("LOG SAVED. ENTRY OVERWRITTEN IF IT EXISTED.")
       

    habits_df = pd.read_sql_query("SELECT * FROM habits", conn)
    conn.close()
    

    st.write("---")

    if not habits_df.empty:
        habits_df["date"] = pd.to_datetime(habits_df["date"]).dt.date
        selected_data = habits_df[habits_df["date"] == habit_date]

        if not selected_data.empty:
            st.subheader("Archived log readout")
            st.dataframe(selected_data, use_container_width=True)
        else:
            st.info("No log entry detected for this temporal marker.")
    else:
        st.info("Database Cold. No entries logged.")
