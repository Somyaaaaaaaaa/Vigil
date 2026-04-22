import streamlit as st
from datetime import datetime
import database as db
from modules import analytics, home, checklist, goals, routines, tasks, habits
import os 
from dotenv import load_dotenv

load_dotenv()

def get_password():
    env_pass = os.getenv("APP_PASSWORD")

    try:
        secret_pass = st.secrets["APP_PASSWORD"]
    except Exception:
        secret_pass = None

    return env_pass or secret_pass

# configurations
LOGO_PATH = os.path.join("assets", "Untitled.png")

st.set_page_config(
    page_title="Vigil",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state= "collapsed"
)

# authentication logic
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

stored_password = get_password()

if not stored_password:
    st.error("APP_PASSWORD not set. Fix your config.")
    st.stop()

if not st.session_state.authenticated:
    _, col, _ = st.columns([1,1,1])

    with col:
        st.markdown("<h2 style='text-align:center;'>ACCESS REQUIRED</h2>", unsafe_allow_html=True)

        password = st.text_input("ENTER CODE", type="password", label_visibility="collapsed")

        if st.button("ENTER"):
            if password == stored_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("ACCESS DENIED")

    st.stop()

# interface

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400&family=Playfair+Display:ital,wght@0,600;1,400&display=swap');

/* Typography Fixes */
html, body, [class*="ViewContainer"], .stMarkdown {
    font-family: 'Inter', sans-serif !important;
}

h1, h2, h3, .playfair {
    font-family: 'Playfair Display', serif !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: url("assets/water.avif");       
    background-size: cover;
    background-position: center;
    border-right: 1px solid rgba(0,229,255,0.1);
}

[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(0, 5, 15, 0.95) 0%, rgba(0, 10, 25, 0.9) 100%);
}

/* Cleanup Sidebar content visibility */
[data-testid="stSidebarNav"] { background-color: transparent !important; }
[data-testid="stSidebar"] * { color: #cfe9ff !important; }

/* Radio Button "Luxe" Style */
div[role="radiogroup"] label {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 4px !important;
    margin-bottom: 5px !important;
    padding: 10px !important;
}

div[role="radiogroup"] label[aria-checked="true"] {
    background: rgba(0, 229, 255, 0.1) !important;
    border-left: 3px solid #00e5ff !important;
}

</style>
""", unsafe_allow_html=True)

# sidebar
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)

st.sidebar.markdown("<p style='letter-spacing:4px; font-size:10px; opacity:0.5; text-align:center;'>VIGIL CORE</p>", unsafe_allow_html=True)

if "main_nav" not in st.session_state:
    st.session_state.main_nav = "Dashboard"

main_nav = st.sidebar.radio("SYSTEMS", ["Dashboard", "Tracking", "Planning", "Insights"])

# Sub-navigation Logic
sub_page = None
if main_nav == "Tracking":
    st.sidebar.markdown("---")
    sub_page = st.sidebar.radio("DATA_TRACKS", ["Tasks", "Habits"])
elif main_nav == "Planning":
    st.sidebar.markdown("---")
    sub_page = st.sidebar.radio("STRATEGY", ["Goals", "Routines", "Checklist"])



if main_nav == "Dashboard":
    home.show()
elif main_nav == "Tracking":
    if sub_page == "Tasks": tasks.show()
    elif sub_page == "Habits": habits.show()
elif main_nav == "Planning":
    if sub_page == "Goals": goals.show()
    elif sub_page == "Routines": routines.show()
    elif sub_page == "Checklist": checklist.show()

elif main_nav == "Insights":
    analytics.show()
