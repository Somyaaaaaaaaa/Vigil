import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import database as db
import calendar


def show():
    def load_all_data():
        conn = db.connect()
        habits = pd.read_sql_query("SELECT * FROM habits", conn)
        goals = pd.read_sql_query("SELECT * FROM goals", conn)
        notes = pd.read_sql_query("SELECT * FROM notes", conn)
        conn.close()
        return habits, goals, notes

    habits_df, goals_df, notes_df = load_all_data()

    if "goals" not in st.session_state:
        st.session_state.goals = goals_df.copy()

    # css
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600&family=Playfair+Display:italic@700&display=swap');
        
        html, body, [class*="ViewContainer"] {
            font-family: 'Inter', sans-serif;
            color: #FFFFFF;
        }

        /* Top Brand Label - Keeping opacity for that tech-ghost look but making it white */
        .brand-label { 
            text-transform: uppercase; 
            letter-spacing: 5px; 
            font-size: 10px; 
            color: #FFFFFF !important; 
            opacity: 0.5; 
            margin-bottom: 20px;
        }
                
        div[data-testid="stCheckbox"] label p {
            font-size:16px;
            font-weight:200;
            color: #FFFFFF !important;
        }
                
        /* Hover effect for the underline */
        div[data-baseweb="select"]:hover, 
        div[data-baseweb="base-input"]:hover {
            border-bottom: 1px solid #00e5ff !important;
        }

        /* HEADING OVERRIDES */
        h1 { 
            font-family: 'Playfair Display', serif; 
            font-weight: 700; 
            letter-spacing: -1.5px; 
            line-height: 1.1; 
            color: #FFFFFF !important; /* Forces White */
        }
        
        h4 { 
            font-family: 'Inter', sans-serif; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 2px; 
            font-size: 11px; 
            color: #FFFFFF !important; /* Forces White */
            opacity: 0.8; /* Increased from 0.6 for better readability */
            margin-bottom: 20px; 
        }

        /* Input styling: Clean underline */
        .stTextInput input {
            background-color: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            color: white !important;
        }
        
        /* Ghost Buttons for Calendar & Delete */
        div.stButton > button {
            background: transparent;
            border: none;
            color: rgba(255,255,255,0.4);
            transition: 0.3s ease;
        }
        div.stButton > button:hover {
            color: #00e5ff;
            background: transparent;
        }

        /* Strike-through for completed tasks */
        .completed-task { opacity: 0.3; text-decoration: line-through; font-weight: 200; color: #FFFFFF; }
        .active-task { opacity: 1; font-weight: 200; color: #FFFFFF; }
        </style>
    """, unsafe_allow_html=True)



    today = datetime.now()
    if "selected_year" not in st.session_state: st.session_state.selected_year = today.year
    if "selected_month" not in st.session_state: st.session_state.selected_month = today.month

    # header
    st.markdown('<p class="brand-label">VIGIL.</p>', unsafe_allow_html=True)
    
    col_greet, col_stat = st.columns([2,1])
    
    with col_greet:
        st.markdown(f"""
            <h1 style="font-size:48px;">Welcome back,<br><i>Asset</i></h1>
            <p style="color:rgba(255,255,255,0.6); font-size: 12px; letter-spacing:1px; margin-top:10px;">{today.strftime("%d %B, %Y").upper()}</p>
        """, unsafe_allow_html=True)

    with col_stat:
        # Streak Calculation Logic
        streak = 0

        if not habits_df.empty:
            habits_df["date"] = pd.to_datetime(habits_df["date"]).dt.date
            unique_dates = set(habits_df["date"])

            current_day = date.today()

            while current_day in unique_dates:
                streak += 1
                current_day -= timedelta(days=1)        
        
        st.markdown(f"""
            <div style="text-align:right; margin-top: 20px;">
                <p style="font-size:9px; opacity:0.4; letter-spacing:2px; margin-bottom:-5px;">Streak</p>
                <p style="font-size:48px; font-weight:200;">{streak:02d}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # main dashboard grid
    left_col, right_col = st.columns([1.8, 1.2], gap="large")

    with left_col:
        def render_goal_sector(title, category_key, mode_label):
            st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)

            conn = db.connect()
            goals_data = pd.read_sql_query(f"SELECT * FROM goals WHERE category='{category_key}'", conn)
            conn.close()

            if not goals_data.empty:
                for _, row in goals_data.iterrows():
                    c1, c2 = st.columns([12, 1])

                    with c1:
                        is_done = bool(row["completed"])

                        checked = st.checkbox(
                            row["title"],
                            value=is_done,
                            key=f"home_goal_{row['id']}"
                        )

                        if checked != is_done:
                            conn = db.connect()
                            conn.execute(
                                "UPDATE goals SET completed=? WHERE id=?",
                                (checked, row["id"])
                            )
                            conn.commit()
                            conn.close()
                            load_all_data.clear()

                    with c2:
                        if st.button("×", key=f"del_home_goal_{row['id']}"):
                            conn = db.connect()
                            conn.execute("DELETE FROM goals WHERE id=?", (row["id"],))
                            conn.commit()
                            conn.close()
                            load_all_data.clear()
                            st.rerun()


            new_goal = st.text_input(
                f"Add to {title}",
                placeholder=f"+ New {mode_label} Objective",
                label_visibility="collapsed",
                key=f"input_{category_key}"
            )

            if new_goal.strip() and new_goal != st.session_state.get(f"last_{category_key}", ""):
                conn = db.connect()
                cursor = conn.cursor()

                time_val = (
                    datetime.now().strftime("%b")
                    if mode_label == "Monthly"
                    else str(datetime.now().year)
                )
                    
                cursor.execute(
                    "INSERT INTO goals (title, category, mode, time_value, duration, completed) VALUES (?, ?, ?, ?, ?, ?)",
                    (new_goal, category_key, mode_label, time_val,
                    4 if mode_label == "Monthly" else 52, False)
                )
                
                conn.commit()
                conn.close()
                st.session_state[f"last_{category_key}"] = new_goal
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)


        render_goal_sector("Monthly Focus", "Monthly Focus", "Monthly")
        render_goal_sector("Yearly Vision", "Yearly Focus", "Yearly")

        st.markdown("<h4>System Status</h4>", unsafe_allow_html=True)

        monthly_data = goals_df[goals_df["mode"] == "Monthly"]

        progress = 0
        if not monthly_data.empty:
            progress = monthly_data["completed"].sum() / len(monthly_data)
            st.progress(progress)
        else:
            st.progress(0)

        st.markdown(
            f"<p style='font-size:11px; opacity:0.6;'>Completion: {int(progress*100)}%</p>",
            unsafe_allow_html=True
)

        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 5px; margin-top: 10px;">
            <p style="font-size: 10px; opacity: 0.5; margin-bottom: 2px;">VIGIL_OS_VERSION: 2.0.4</p>
            <p style="font-size: 10px; opacity: 0.5; margin-bottom: 2px;">ENCRYPTION: ACTIVE</p>
            <p style="font-size: 10px; opacity: 0.5;">LOCATION: KOLKATA_NODE_01</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="font-family:'Playfair Display', serif; font-size:18px; opacity:0.4; font-style:italic; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 20px;">
            IEnergy flows where attention goes. Focus on the signal, not the noise.
            </div>
        """, unsafe_allow_html=True)



    if "selected_date" not in st.session_state:
        st.session_state.selected_date = str(date.today())

    if "selected_month" not in st.session_state:
        st.session_state.selected_month = date.today().month

    if "selected_year" not in st.session_state:
        st.session_state.selected_year = date.today().year


    conn = db.connect()
    notes_df = pd.read_sql_query("SELECT * FROM notes ORDER BY date DESC", conn)
    conn.close()

    if not notes_df.empty:
        notes_df["date"] = notes_df["date"].astype(str)


    with right_col:
        st.markdown("<h4>Calendar</h4>", unsafe_allow_html=True)

        nav_prev, nav_label, nav_next = st.columns([1,3,1])

        with nav_prev:
            if st.button("—", key="cal_prev"):
                st.session_state.selected_month -= 1
                if st.session_state.selected_month == 0:
                    st.session_state.selected_month = 12
                    st.session_state.selected_year -= 1
                st.rerun()

        with nav_next:
            if st.button("+", key="cal_next"):
                st.session_state.selected_month += 1
                if st.session_state.selected_month == 13:
                    st.session_state.selected_month = 1
                    st.session_state.selected_year += 1
                st.rerun()

        with nav_label:
            st.markdown(
                f"<p style='text-align:center; font-size:11px; letter-spacing:2px; margin-top:10px; opacity:0.8;'>"
                f"{calendar.month_name[st.session_state.selected_month].upper()} {st.session_state.selected_year}</p>",
                unsafe_allow_html=True
            )

        dates_with_notes = set(notes_df["date"]) if not notes_df.empty else set()

        days_header = ["M", "T", "W", "T", "F", "S", "S"]
        cols = st.columns(7)
        for i, d in enumerate(days_header):
            cols[i].markdown(
                f"<p style='text-align:center; font-size:9px; opacity:0.3;'>{d}</p>",
                unsafe_allow_html=True
            )

        month_cal = calendar.monthcalendar(
            st.session_state.selected_year,
            st.session_state.selected_month
        )

        for week in month_cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0:
                    cols[i].write("")
                else:
                    date_key = f"{st.session_state.selected_year}-{st.session_state.selected_month:02d}-{day:02d}"
                    has_note = date_key in dates_with_notes

                    if cols[i].button(str(day), key=f"btn_{date_key}"):
                        st.session_state.selected_date = date_key
                        st.rerun()

                    if has_note:
                        cols[i].markdown(
                            "<div style='margin-top:-15px; text-align:center; color:#00e5ff; font-size:15px;'>•</div>",
                            unsafe_allow_html=True
                        )

        st.markdown("<br><br><h4>Intelligence Feed</h4>", unsafe_allow_html=True)

        selected_date = st.session_state.selected_date

        st.markdown(
            f"<p style='font-size:10px; opacity:0.5;'>Logging for: {selected_date}</p>",
            unsafe_allow_html=True
        )

        
        note_input = st.text_area(
            "Log intel:",
            key="intel_input"
        )

        clean_note = note_input.strip()

        if clean_note and clean_note != st.session_state.get("last_note", ""):
            conn = db.connect()
            conn.execute(
                "INSERT INTO notes (date, note) VALUES (?, ?)",
                (selected_date, clean_note)
            )
            conn.commit()
            conn.close()

            st.session_state.last_note = clean_note
            st.rerun()

        selected_date = st.session_state.selected_date
        filtered_notes = notes_df[notes_df["date"] == selected_date]

        if not filtered_notes.empty:
            for _, row in filtered_notes.iterrows():
                col1, col2 = st.columns([10,1])

                with col1:
                    st.markdown(f"""
                        <div style="margin-bottom:20px; border-left: 2px solid rgba(0,229,255,0.3); padding-left: 14px;">
                            <span style="font-size:11px; color:#00e5ff; letter-spacing:1px; opacity:0.75;">
                                {row['date']}
                            </span><br>
                            <span style="font-size:15px; font-weight:300; opacity:0.9;">
                                {row['note']}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    if st.button("-", key=f"del_{row['id']}"):
                        conn = db.connect()
                        conn.execute("DELETE FROM notes WHERE id=?", (row["id"],))
                        conn.commit()
                        conn.close()
                        st.rerun()
        else:
            st.markdown("<p style='font-size:12px; opacity:0.3;'>No intel logged for this date.</p>", unsafe_allow_html=True)
