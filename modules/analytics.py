import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import database as db
import calendar

def show():

    st.markdown("""
            <style>
            .stMetric { background: rgba(0, 229, 255, 0.05); padding: 15px; border-radius: 5px; border-left: 2px solid #00e5ff; }
            .stProgress > div > div > div > div { background-color: #00ff9f; }
            h3 { font-family: monospace; letter-spacing: 2px; text-transform: uppercase; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; }
            div[data-baseweb="select"]:hover, 
            div[data-baseweb="base-input"]:hover {
                border-bottom: 1px solid #00e5ff !important;
            }
            </style>
        """, unsafe_allow_html=True)

    st.title("Analytics")

    @st.cache_data
    def load_data():
        try:
            tasks = db.load_tasks_by_date("")  # we'll fix filtering below
            habits = db.load_all_habits()
            return tasks, habits
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return [], []
    

    tasks, habits = load_data()

    tasks_df = pd.DataFrame(tasks, columns=["id", "task", "date", "mission_id", "completed"])
    habits_df = pd.DataFrame(habits, columns=[
        "id", "date", "wake_time", "sleep_time",
        "water", "steps", "workout", "screen_time",
        "mood", "energy", "focus", "meals", "snacks", "night_issue"
    ])

    if not habits_df.empty:
        habits_df["date"] = pd.to_datetime(habits_df["date"], errors="coerce").dt.date

# STREAK CALCULATION
    st.subheader("Sector 1: Persistence Metrics")

    streak = 0

    if not habits_df.empty:
        habits_df["date"] = pd.to_datetime(habits_df["date"], errors="coerce").dt.date
        unique_dates = set(habits_df["date"])

        today = date.today()

        # if today not logged yet, start from yesterday
        current_day = today if today in unique_dates else today - timedelta(days=1)

        while current_day in unique_dates:
            streak += 1
            current_day -= timedelta(days=1)


        # historical best
        temp_streak = 1

        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                temp_streak += 1
                max_streak = max(max_streak, temp_streak)
            else:
                temp_streak = 1

        max_streak = max(max_streak, temp_streak)

    # display

    habits_df["date"] = pd.to_datetime(habits_df["date"]).dt.date

    # SCORECARD

    scores = []

    # workout mapping (behavioral input)
    workout_map = {
        "None": 0,
        "Light": 0.4,
        "Moderate": 0.7,
        "Intense": 1.0
    }

    for _, row in habits_df.iterrows():
        date_val = row["date"]

        tasks_today = tasks_df[tasks_df["date"] == date_val]

        # --- TASK SCORE ---
        if not tasks_today.empty:
            completed = tasks_today["completed"].sum()
            tasks_completed_ratio = completed / len(tasks_today)
        else:
            tasks_completed_ratio = None  # don't punish empty days

        # --- SAFE EXTRACTION ---
        water = row.get("water", 0) or 0
        steps = row.get("steps", 0) or 0
        screen_time = row.get("screen_time", 0) or 0
        focus = row.get("focus", 0) or 0
        energy = row.get("energy", 0) or 0
        workout = row.get("workout", "None")

        score = 0

        if tasks_completed_ratio is not None:
            score += tasks_completed_ratio * 30

        score += min(water / 2, 1) * 10
        score += min(steps / 7000, 1) * 10

        workout_score = workout_map.get(workout, 0) * 15
        score += workout_score

        score += max(0, 1 - screen_time / 8) * 15

        # reward pushing through low energy/focus
        if (focus < 4 or energy < 4) and tasks_completed_ratio is not None:
            if tasks_completed_ratio > 0.7:
                score += 5

        score = max(0, min(100, score))

        scores.append({
            "date": date_val,
            "score": score
        })

    scores_df = pd.DataFrame(scores)

    today_date = datetime.now().date()

    if not scores_df.empty and "date" in scores_df.columns:
        today_score = scores_df[scores_df["date"] == today_date]
    else:
        today_score = pd.DataFrame()

    best_score = scores_df["score"].max() if not scores_df.empty else 0

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Streak", streak)
    m2.metric("Best Streak", max_streak)
    m3.metric("Today's Score", int(today_score.iloc[0]["score"]) if not today_score.empty else 0)
    m4.metric("Best Score", int(best_score))

    today_score_val = 0

    if not scores_df.empty:
        today_score = scores_df[scores_df["date"] == today_date]
        if not today_score.empty:
            today_score_val = today_score.iloc[0]["score"]

    if today_score_val >= 80:
        st.success("Strong day. Stay consistent.")

    elif today_score_val >= 50:
        st.info("Decent. Tighten execution tomorrow.")

    else:
        st.warning("Low output today. Reset, don't spiral.")


# XP LEVEL SYSTEM
    tasks_completed = tasks_df[tasks_df["completed"]]

    xp = len(tasks_completed) * 10

    if not scores_df.empty:
        xp += int(scores_df["score"].sum())

    import math

    level = int(math.sqrt(xp / 100))

    xp_for_current_level = (level ** 2) * 100
    xp_for_next_level = ((level + 1) ** 2) * 100

    progress = (xp - xp_for_current_level) / (xp_for_next_level - xp_for_current_level)
    progress = max(0, min(progress, 1))

    col1, col2 = st.columns(2)

    col1.metric("Level", int(level))
    col2.metric("Total XP", int(xp))

    st.progress(progress)

    st.expander("How is your daily score calculated?").markdown("""
    ### Scoring Breakdown

    **1. Task Execution (30 pts)**
    - Based on % of tasks completed for the day  
    - Completing all tasks = full score  

    **2. Physical Baseline (20 pts total)**
    - Water intake → up to 10 pts (≈3L for full score)  
    - Steps → up to 10 pts (scaled target, not fixed)  

    **3. Workout Effort (15 pts)**
    - None → 0  
    - Light → partial  
    - Moderate → high  
    - Intense → full score  

    **4. Screen Discipline (15 pts)**
    - Lower screen time = higher score  
    - Encourages focus and reduced distractions  

    ---

    ### Bonus (+5 pts)
    If your **focus or energy is low**, but you still complete most of your tasks,  
    you are rewarded for pushing through.

    ---

    ### Philosophy
    This is not a mood tracker.

    - Bad day but strong execution → high score  
    - Good mood but poor execution → low score  

    The system measures:
    > **How you operate under real conditions**

    ---

    ### Score Meaning

    - **50–65** → average day  
    - **65–75** → structured day  
    - **75–85** → disciplined day  
    - **85+** → high-performance day  
    """)
    
    # ACHIEVEMENTS
    st.markdown("### Sector 2: Achievements")

    achievements = []

    today_date = datetime.now().date()

    tasks_df["date"] = pd.to_datetime(tasks_df["date"], errors="coerce").dt.date
    scores_df["date"] = pd.to_datetime(scores_df["date"], errors="coerce").dt.date

    tasks_today = tasks_df[tasks_df["date"] == today_date]
    completed_today = int(tasks_today["completed"].sum()) if not tasks_today.empty else 0

    today_score_val = 0
    last_7_avg_score = 0

    if not scores_df.empty:
        scores_df = scores_df.sort_values("date")

        today_score = scores_df[scores_df["date"] == today_date]
        if not today_score.empty:
            today_score_val = today_score.iloc[0]["score"]

        last_7 = scores_df.tail(7)
        if not last_7.empty:
            last_7_avg_score = last_7["score"].mean()


    if streak >= 7:
        achievements.append("⚡ 7-Day Streak — Momentum locked")

    if streak >= 14:
        achievements.append("🔥 14-Day Streak — Consistency")

    if streak >= 30:
        achievements.append("👑 30-Day Streak — Discipline building")

    if last_7_avg_score >= 75:
        achievements.append("High achiever")

    if completed_today >= 5 and streak >= 3:
        achievements.append("Execution On Point")

    if today_score_val >= 90:
        achievements.append("Winner, aren't you?")

    if achievements:
        for ach in achievements:
            st.success(ach)
    else:
        st.info("No achievements yet. Earn them.")

    # task productivity
    st.subheader("Sector 3: Execution Pattern")

    if not tasks_df.empty:

        tasks_df["date"] = pd.to_datetime(tasks_df["date"], errors="coerce")

        daily = tasks_df.groupby("date")["completed"].mean()

        full_range = pd.date_range(start=daily.index.min(), end=daily.index.max())
        daily = daily.reindex(full_range, fill_value=0)

        weekly = daily.resample("W").mean()
        monthly = daily.resample("M").mean()

        if len(daily) >= 14:
            last_7 = daily.tail(7).mean()
            prev_7 = daily.tail(14).head(7).mean()
            delta = last_7 - prev_7

            st.metric(
                "Execution Change (Last 7 Days)",
                f"{last_7:.2f}",
                delta=f"{delta:+.2f}"
            )

        tab1, tab2, tab3 = st.tabs(["Daily", "Weekly", "Monthly"])

        with tab1:
            st.line_chart(daily)

        with tab2:
            st.line_chart(weekly)

        with tab3:
            st.line_chart(monthly)

    else:
        st.info("No task data yet.")

# consequences + rewards

    if streak >= 30:
        st.snow()
        st.success("👑 30-Day Streak. This is discipline.")

    elif streak >= 14:
        st.balloons()
        st.success("🔥 14-Day Streak. You're locked in.")

    elif streak >= 7:
        st.balloons()
        st.success("⚡ 7-Day Streak. Momentum building.")

    elif streak >= 3:
        st.info("📈 3-Day Streak. Keep it alive.")

    elif streak == 0:
        st.error("Chain broken. Start again today.")

# win screen
    if streak >= 7:
        st.balloons()
        st.success("7-day streak. Keep going.")   

    # habit analysis
    st.subheader("Sector 4: Habit Correlations")
    if not habits_df.empty:
        habits_df = habits_df.sort_values("date")

        full_range = pd.date_range(
            start=habits_df["date"].min(),
            end=habits_df["date"].max()
        )
        
        habits_df["date"] = pd.to_datetime(habits_df["date"], errors="coerce")

        habits_df = habits_df.sort_values("date").drop_duplicates("date", keep="last")
        habits_df = habits_df.set_index("date")
        habits_df = habits_df.reindex(full_range)
        habits_df.index.name = "date"

        habits_df["mood"] = pd.to_numeric(habits_df["mood"], errors="coerce")
        habits_df["energy"] = pd.to_numeric(habits_df["energy"], errors="coerce")
        habits_df["focus"] = pd.to_numeric(habits_df["focus"], errors="coerce")

        # Sleep

        habits_df["wake_time"] = pd.to_datetime(habits_df["wake_time"], errors="coerce")
        habits_df["sleep_time"] = pd.to_datetime(habits_df["sleep_time"], errors="coerce")

        habits_df["wake_time"] = habits_df["wake_time"].dt.hour + habits_df["wake_time"].dt.minute/60
        habits_df["sleep_time"] = habits_df["sleep_time"].dt.hour + habits_df["sleep_time"].dt.minute/60

        # Workout mapping
        workout_map = {
            "None": 0,
            "Light": 1,
            "Moderate": 2,
            "Intense": 3
        }
        habits_df["workout_num"] = habits_df["workout"].map(workout_map)

        tab1, tab2, tab3, tab4 = st.tabs(["Mental", "Physical", "Lifestyle", "Workout Grid"])

        with tab1:
            st.subheader("Focus vs Water")
            scatter_df = habits_df[["focus", "water"]].dropna()
            st.scatter_chart(scatter_df, x="water", y="focus")
            st.subheader("Focus vs Screen Time")
            scatter_df2 = habits_df[["focus", "screen_time"]].dropna()
            st.scatter_chart(scatter_df2, x="screen_time", y="focus")
        
        with tab2:
            st.subheader("Physical Activity")
            st.line_chart(habits_df[["steps", "water"]])

        with tab3:
            st.subheader("Lifestyle & Recovery")
            
            st.line_chart(habits_df[["screen_time", "meals", "snacks"]])
            
            sleep_df = habits_df[["wake_time", "sleep_time"]].dropna()
            if not sleep_df.empty:
                st.subheader("Sleep Schedule")
                st.line_chart(sleep_df[["sleep_time", "wake_time"]])    
            else:
                st.info("No habit data yet.")
        
        with tab4:
            st.subheader("Workout Consistency")

            color_map = {
                "None": "#630e0e",
                "Light": "#fdff9f",
                "Moderate": "#8bef80",
                "Intense": "#2945c5"
            }

            today = datetime.now()
            year = today.year
            month = today.month

            month_days = calendar.monthcalendar(year, month)

            habits_df = habits_df.reset_index()
            habits_df["date"] = pd.to_datetime(habits_df["date"], errors="coerce").dt.date
            habits_df = habits_df.sort_values("date").drop_duplicates("date", keep="last")

            workout_lookup = dict(zip(habits_df["date"], habits_df["workout"]))

            days_header = ["M", "T", "W", "T", "F", "S", "S"]
            cols = st.columns(7)

            for i, d in enumerate(days_header):
                cols[i].markdown(f"<p style='text-align:center; opacity:0.5'>{d}</p>", unsafe_allow_html=True)

            for week in month_days:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    if day == 0:
                        cols[i].write("")
                    else:
                        date_key = datetime(year, month, day).date()

                        workout = workout_lookup.get(date_key)

                        if date_key > datetime.now().date():
                            color = "#111111"  
                            label = ""
                        else:
                            if pd.isna(workout) or workout is None:
                                workout = "None"

                            color = color_map.get(workout, "#1a1a1a")
                            label = str(day)

                        cols[i].markdown(f"""
                            <div style="
                                height:25px;
                                width:25px;
                                margin:auto;
                                border-radius:4px;
                                background-color:{color};
                                text-align:center;
                                font-size:10px;
                                line-height:25px;
                                opacity:0.9;
                            ">
                                {label}
                            </div>
                        """, unsafe_allow_html=True)

    # ANALYTICS
    st.markdown("### Sector 5: Insights")

    insights = []

    if not habits_df.empty:

        df = habits_df.copy()

        df["focus"] = pd.to_numeric(df["focus"], errors="coerce")
        df["energy"] = pd.to_numeric(df["energy"], errors="coerce")
        df["mood"] = pd.to_numeric(df["mood"], errors="coerce")
        df["water"] = pd.to_numeric(df["water"], errors="coerce")
        df["steps"] = pd.to_numeric(df["steps"], errors="coerce")
        df["screen_time"] = pd.to_numeric(df["screen_time"], errors="coerce")

        def safe_corr(col1, col2):
            if df[col1].notna().sum() > 3 and df[col2].notna().sum() > 3:
                return df[[col1, col2]].corr().iloc[0,1]
            return 0

        sleep_focus = safe_corr("sleep_time", "focus")
        workout_mood = safe_corr("workout_num", "mood")
        screen_energy = safe_corr("screen_time", "energy")
        water_focus = safe_corr("water", "focus")

        if sleep_focus > 0.3:
            insights.append("Better sleep → better focus.")
        elif sleep_focus < -0.3:
            insights.append("Your sleep is hurting your focus.")

        if workout_mood > 0.3:
            insights.append("Workouts improve your mood.")
        elif workout_mood < -0.3:
            insights.append("Your workouts are inconsistent with mood.")

        if screen_energy < -0.3:
            insights.append("More screen time → lower energy.")

        if water_focus > 0.3:
            insights.append("Hydration improves your focus.")

    # display
    if insights:
        for i in insights:
            st.info(i)
    else:
        st.write("Not enough data yet.")

