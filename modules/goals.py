import streamlit as st
import pandas as pd
import database as db
import calendar

def show():

    if "selected_mission" not in st.session_state:
        st.session_state.selected_mission = None
    st.markdown("""
        <style>
        /* Transparency & Sharp Underlines */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="base-input"] > div,
        .stTextArea textarea, .stTextInput input {
            background-color: transparent !important;
            border-radius: 0px !important;
            border: none !important;
            border-bottom: 1px solid rgba(0, 229, 255, 0.2) !important;
            color: white !important;
            font-family: 'Courier New', monospace;
        }
                
        /* Hover effect for the underline */
        div[data-baseweb="select"]:hover, 
        div[data-baseweb="base-input"]:hover {
            border-bottom: 1px solid #00e5ff !important;
        }

        /* Tactical Checkbox Style */
        .stCheckbox { padding: 5px 0px; }
        .stCheckbox p { font-family: 'Courier New', monospace; text-transform: uppercase; letter-spacing: 1px; }

        /* Ghost Expander Headers */
        .streamlit-expanderHeader {
            background-color: transparent !important;
            border: none !important;
            color: #00e5ff !important;
            font-family: monospace;
            text-transform: uppercase;
        }

        /* Action Buttons */
        div.stButton > button {
            background-color: transparent;
            border: 1px solid #00ff9f;
            border-radius: 0px;
            color: #00ff9f;
            width: 100%;
            transition: 0.3s;
        }
        div.stButton > button:hover { background-color: rgba(0, 255, 159, 0.1); border: 1px solid #00ff9f; }
        </style>
    """, unsafe_allow_html=True)

    st.title("◈ Mission Planning")

    with st.expander("✚ Initiate New Mission", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            mode = st.selectbox("Execution Window", ["Daily", "Weekly", "Monthly"])
            conn = db.connect()
            df_domains = pd.read_sql_query("SELECT DISTINCT category FROM missions", conn)
            conn.close()
            existing_domains = df_domains["category"].dropna().tolist()
            mode_select = st.radio("Sector Origin", ["EXISTING", "NEW"], horizontal=True)
            category = st.selectbox("Designation", existing_domains) if mode_select == "EXISTING" and existing_domains else st.text_input("New Designation", placeholder="ALPHA-01")

        with c2:
            duration = st.slider("Operational Window (Weeks)", 1, 52, 8)
            if mode == "Daily":
                time_value = st.date_input("Target")
            elif mode == "Weekly":
                time_value = st.number_input("Op-Week", 1, 52, 1)
            elif mode == "Monthly":
                time_value = st.selectbox("Taerget Month", calendar.month_name[1:])
          
        goal_input = st.text_area("Objective Parameters")

        if st.button("Confirm Mission Deployment"):
            if goal_input and category:
                conn = db.connect()
                conn.execute(
                    "INSERT INTO missions (title, category, mode, time_value, duration, completed) VALUES (?, ?, ?, ?, ?, ?)",
                    (goal_input, category, mode, str(time_value), duration, False)
                )
                conn.commit()
                conn.close()
                st.rerun()

    st.write("---")

    conn = db.connect()
    df_all = pd.read_sql_query("SELECT * FROM missions", conn)
    details_df = pd.read_sql_query("SELECT * FROM goal_details", conn)

    if not df_all.empty:
        sectors = df_all["category"].unique().tolist()
        selected_sector = st.selectbox("◈ Active Theatre View", sectors)
        filtered_df = df_all[df_all["category"] == selected_sector]

        if filtered_df.empty:
            st.info("Sector Dark. No Active Missions.")
        else:
            st.markdown(f"## // {selected_sector.upper()}")
            
            for _, row in filtered_df.iterrows():
                checked = st.checkbox(
                    row["title"],
                    value=bool(row["completed"]),
                    key=f"chk_{row['id']}"
                )

                if checked != bool(row["completed"]):
                    conn.execute(
                        "UPDATE missions SET completed=? WHERE id=?",
                        (checked, row["id"])
                    )
                    conn.commit()
                    st.session_state["_refresh"] = not st.session_state.get("_refresh", False)


                with st.expander("File Intel"):
                    mission_intel = details_df[details_df['goal_id'] == row['id']]
                    
                    if not mission_intel.empty:
                        for _, intel_row in mission_intel.iterrows():
                            st.markdown(f"""
                                <div style="border-left: 2px solid #00ff9f; padding-left: 10px; margin-bottom: 10px;">
                                    <p style="font-family: monospace; font-size: 10px; color: #00e5ff; margin: 0;">
                                        // {intel_row['section'].upper()}
                                    </p>
                                    <p style="font-size: 14px; margin: 0;">{intel_row['content']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.caption("No intel secured for this mission.")

                    st.write("---")

                    # --- 2. INPUT NEW INTEL ---
                    sub_c1, sub_c2 = st.columns([1, 2])
                    with sub_c1:
                        custom_tag = st.text_input("Intel Tag", placeholder="RECON", key=f"tag_{row['id']}")
                    with sub_c2:
                        intel_data = st.text_area("Data Input", key=f"data_{row['id']}", height=68)
                    
                    if st.button("Upload Intel", key=f"up_{row['id']}"):
                        if custom_tag and intel_data:
                            db.save_goal_detail(row['id'], custom_tag, intel_data)
                            st.toast(f"INTEL {custom_tag.upper()} SECURED.")
                            # Standardizing to st.rerun() to ensure the list updates immediately
    else:
        st.info("Sector Dark. No Active Missions.")

    conn.close()