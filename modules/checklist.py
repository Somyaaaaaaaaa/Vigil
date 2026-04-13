import streamlit as st
import pandas as pd
from datetime import datetime
import database as db
import calendar

def show():
    st.markdown("""
        <style>
        /* Hover effect for the underline */
        div[data-baseweb="select"]:hover, 
        div[data-baseweb="base-input"]:hover {
            border-bottom: 1px solid #00e5ff !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("◈ Peripheral Vision")

    def deploy_intel():
        item = st.session_state.wishlist_input
        if item:
            db.add_wishlist(item)
            st.session_state.wishlist_input = ""

    st.text_input("Recon Input", key="wishlist_input")

    st.button("Deploy Intel", on_click=deploy_intel)

    df = db.load_wishlist()

    if not df.empty:
        for _, row in df.iterrows():
            col1, col2 = st.columns([5,1])

            with col1:
                checked = st.checkbox(
                    row["item"],
                    value=bool(row["completed"]),
                    key=f"wish_{row['id']}"
                )

                if checked != bool(row["completed"]):
                    db.update_wishlist(row["id"], checked)
                    st.session_state["_refresh"] = not st.session_state.get("_refresh", False)

            with col2:
                if st.button("⊝", key=f"del_wish_{row['id']}"):
                    db.delete_wishlist(row["id"])
                    st.session_state["_refresh"] = not st.session_state.get("_refresh", False)
    else:
        st.info("Array clean. No intel on the horizon.")