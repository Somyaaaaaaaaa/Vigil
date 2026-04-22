import streamlit as st
import pandas as pd
import database as db

def show():
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border: 1px solid rgba(0, 229, 255, 0.2);
            padding: 10px 20px;
            font-family: monospace;
        }
        .stTabs [aria-selected="true"] {
            border: 1px solid #00e5ff !important;
            box-shadow: 0px 0px 10px rgba(0, 229, 255, 0.2);
        }
                
        div[data-baseweb="select"]:hover, 
        div[data-baseweb="base-input"]:hover {
            border-bottom: 1px solid #00e5ff !important;
        }

        </style>
    """, unsafe_allow_html=True)

    st.header("◈ Chronos Protocol")
    st.caption("Time blocks and weekly routines.")

    with st.expander("✚ Allocate time block", expanded=False):
        day = st.selectbox(
            "Operational Day",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )

        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input("START")
        with col2:
            end_time = st.time_input("END")

        task = st.text_area("Objective Description")

        if st.button("Lock Protocol"):
            if not task:
                st.warning("Enter a task.")
            elif start_time >= end_time:
                st.warning("Invalid time range.")
            else:
                db.add_routine(day, start_time.strftime("%H:%M"), end_time.strftime("%H:%M"), task)
                st.toast(f"PROTOCOL LOCKED FOR {day.upper()}.")
                st.rerun()

    st.write("---")

    data = db.load_routines()
    df = pd.DataFrame(data)

    if not df.empty:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        tabs = st.tabs([d.upper()[:3] for d in days]) 

        for i, d in enumerate(days):
            with tabs[i]:
                day_df = df[df["day"] == d]
                
                if not day_df.empty:
                    day_df["start_time"] = pd.to_datetime(day_df["start_time"], format="%H:%M")
                    day_df = day_df.sort_values("start_time")

                    for _, row in day_df.iterrows():
                        st.markdown(f"""
                        <div style="
                            border-left: 2px solid #00e5ff;
                            background: rgba(0, 229, 255, 0.05);
                            padding: 15px;
                            margin-bottom: 10px;
                        ">
                            <div style="font-family: monospace; color: #00e5ff; font-size: 12px; letter-spacing: 1px;">
                                {row['start_time']} >> {row['end_time']}
                            </div>
                            <div style="font-size: 16px; margin-top: 5px; text-transform: uppercase;">
                                {row['task']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("No protocols deployed. Temporal block empty.")
    else:
        st.info("Temporal Block Empty.")

