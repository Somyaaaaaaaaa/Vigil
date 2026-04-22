import streamlit as st
import pandas as pd
import database as db
import calendar

def show():

    missions = db.load_missions()
    df_all = pd.DataFrame(missions)

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

            existing_domains = []
            if not df_all.empty:
                existing_domains = df_all["category"].dropna().unique().tolist()

            mode_select = st.radio("Sector Origin", ["EXISTING", "NEW"], horizontal=True)

            if mode_select == "EXISTING" and existing_domains:
                category = st.selectbox("Designation", existing_domains)
            else:
                category = st.text_input("New Designation", placeholder="ALPHA-01")

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
                db.add_mission(goal_input, category, mode, str(time_value), duration)
                st.rerun()

    st.write("---")

    details = db.load_goal_details_all()  
    details_df = pd.DataFrame(details, columns=[
        "goal_id", "section", "content"
    ])

    if not df_all.empty:
        sectors = df_all["category"].unique().tolist()
        if "selected_sector" not in st.session_state:
            st.session_state.selected_sector = sectors[0]

        selected_sector = st.selectbox(
            "◈ Active Theatre View",
            sectors,
            key="selected_sector"
        )
        filtered_df = df_all[df_all["category"] == selected_sector]

        if filtered_df.empty:
            st.info("Sector Dark. No Active Missions.")
        else:
            st.markdown(f"## // {selected_sector.upper()}")
            
            for _, row in filtered_df.iterrows():
                col_check, col_del = st.columns([6, 1])

                with col_check:
                    checked = st.checkbox(
                        row["title"],
                        value=bool(row["completed"]),
                        key=f"chk_{row['id']}"
                    )

                    if checked != bool(row["completed"]):
                        db.update_mission_status(row["id"], checked)
                        st.rerun()

                with col_del:
                    if st.button("-", key=f"del_{row['id']}"):
                        db.delete_mission(row["id"])
                        st.rerun()


                with st.expander("File Intel"):
                    if not details_df.empty and "goal_id" in details_df.columns:
                        mission_intel = details_df[details_df['goal_id'] == row['id']]
                    else:
                        mission_intel = pd.DataFrame()
                    
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

                    sub_c1, sub_c2 = st.columns([1, 2])
                    with sub_c1:
                        custom_tag = st.text_input("Intel Tag", placeholder="RECON", key=f"tag_{row['id']}")
                    with sub_c2:
                        intel_data = st.text_area("Data Input", key=f"data_{row['id']}", height=68)
                    
                    if st.button("Upload Intel", key=f"up_{row['id']}"):
                        if custom_tag and intel_data:
                            db.save_goal_detail(row['id'], custom_tag, intel_data)
                            st.toast(f"INTEL {custom_tag.upper()} SECURED.")
                            st.rerun()
    else:
        st.info("Sector Dark. No Active Missions.")
