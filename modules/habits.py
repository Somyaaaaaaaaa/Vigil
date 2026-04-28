import streamlit as st
import pandas as pd
from datetime import datetime, date
import database as db
def show():

    def save_habit_log():
        data = {
            "date": str(st.session_state.habit_date),
            "wake": str(st.session_state.wake),
            "sleep": str(st.session_state.sleep),
            "water": st.session_state.water,
            "workout": st.session_state.workout,
            "steps": st.session_state.steps,
            "screen_time": st.session_state.hours + (st.session_state.minutes / 60),
            "mood": st.session_state.mood,
            "energy": st.session_state.energy,
            "focus": st.session_state.focus,
            "meals": st.session_state.meals,
            "snacks": st.session_state.snacks,
            "night_issue": st.session_state.night_issue
        }

        db.add_habit_log(data)

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
    existing = db.load_habits(str(habit_date))

    if existing:
        existing = existing[0]
    else:
        existing = {}

    # only update when date changes
    if "loaded_date" not in st.session_state or st.session_state.loaded_date != habit_date:
        st.session_state.loaded_date = habit_date

        st.session_state.wake = pd.to_datetime(existing.get("wake_time", "07:00")).time()
        st.session_state.sleep = pd.to_datetime(existing.get("sleep_time", "23:00")).time()
        st.session_state.water = existing.get("water", 2.0)
        st.session_state.workout = existing.get("workout", "None")
        st.session_state.steps = existing.get("steps", 3000)

        screen = existing.get("screen_time", 1.0)
        st.session_state.hours = int(screen)
        st.session_state.minutes = int((screen % 1) * 60)

        st.session_state.mood = existing.get("mood", 5)
        st.session_state.energy = existing.get("energy", 5)
        st.session_state.focus = existing.get("focus", 5)

        st.session_state.meals = existing.get("meals", 2)
        st.session_state.snacks = existing.get("snacks", 1)
        st.session_state.night_issue = existing.get("night_issue", "NONE")
        
    st.subheader("Uptime Metrics")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        wake = st.time_input("Wake Signal", key= "wake")
    with col_t2:
        sleep = st.time_input("Sleep Signal", key = "sleep")

    st.subheader("Physical Output")
    c1, c2 = st.columns(2)
    with c1:
        water = st.slider("Hydration Level (L)", 0.0, 5.0, 2.0, key = "water")
        workout = st.selectbox("Workout Intensity Level", ["None", "Light", "Moderate", "Intense"], key = "workout")
    with c2:
        steps = st.number_input("STEP_COUNT", 0, 50000, 3000, key = "steps")

    st.subheader("Screen Time")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        hours = st.number_input("Hours", 0, 24, 1, key = "hours")
    with col_s2:
        minutes = st.number_input("Minutes", 0, 59, 0, key = "minutes")
    screen_time = hours + (minutes / 60)

    st.subheader("Neural Load")
    mood = st.slider("Stability Index (MOOD)", 1, 10, 5, key = "mood")
    energy = st.slider("Reserve Power (ENERGY)", 1, 10, 5, key = "energy")
    focus = st.slider("Signal Clarity (FOCUS)", 1, 10, 5, key = "focus")

    st.subheader("Fuel Intake")
    f1, f2 = st.columns(2)
    with f1:
        meals = st.number_input("Primary meals", 0, 5, 2, key = "meals")
    with f2:
        snacks = st.number_input("Snacks", 0, 10, 1, key = "snacks")

    night_issue = st.selectbox(
        "Sleep Distubances",
        ["NONE", "Nightmare", "Sleep Paralysis", "Dual Disturbance"],
        key = "night_issue"
    )

    st.button("Log Entry", on_click=save_habit_log)
    st.write("---")

    habits = db.load_habits(str(habit_date))
    habits_df = pd.DataFrame(habits)
    
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

