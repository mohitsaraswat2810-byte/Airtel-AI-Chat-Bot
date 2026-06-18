"""
AI Chatbot Application — Main Entry Point.

A Streamlit-based chatbot powered by GPT-OSS with MySQL-backed
user authentication, conversation history, and session management.

Run with:
    streamlit run app.py
"""

import os
import base64
import streamlit as st
from db.connection import init_db
from auth.auth import is_authenticated
from pages.login import show_login_page
from pages.register import show_register_page
from pages.chat import show_chat_page


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# ═══════════════════════════════════════════════════════════════════════
# Page Configuration
# ═══════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="AI Chatbot — GPT-OSS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


if os.path.exists("bgimage.jpg"):
    bg_img_str = get_base64_of_bin_file("bgimage.jpg")
    app_bg = (
        f'background-image: linear-gradient(180deg, rgba(28, 0, 0, 0.68), rgba(16, 0, 0, 0.76)), '
        f'url("data:image/jpeg;base64,{bg_img_str}"); '
        "background-size: cover; background-position: center; background-repeat: no-repeat; "
        "background-attachment: fixed; background-blend-mode: overlay;"
    )
else:
    app_bg = (
        "background: radial-gradient(circle at top left, #ff4d4d 0%, #c70000 24%, #0c0c0c 100%);"
    )


# ═══════════════════════════════════════════════════════════════════════
# Global Styles
# ═══════════════════════════════════════════════════════════════════════

custom_css = f"""
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global typography ── */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* ── App background ── */
    .stApp {{
        {app_bg}
    }}
""" + """
    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a0505 0%, #380404 25%, #160606 100%);
        border-right: 1px solid rgba(255, 77, 77, 0.18);
    }

    section[data-testid="stSidebar"] .stButton button {
        border-radius: 12px;
        transition: all 0.3s ease;
        font-size: 0.85rem;
        color: #fff !important;
        background: linear-gradient(135deg, #ff4d4d 0%, #c70000 100%) !important;
        border: 1px solid rgba(255, 89, 89, 0.22) !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.12);
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(255, 77, 77, 0.32);
    }

    section[data-testid="stSidebar"] .stButton button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffebeb !important;
        border: 1px solid rgba(255, 77, 77, 0.16) !important;
    }

    section[data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
        background: rgba(255, 77, 77, 0.12) !important;
    }

    /* ── Chat messages — bold, high contrast ── */
    .stChatMessage {
        border-radius: 18px;
        margin-bottom: 1rem;
        padding: 1rem;
        background: rgba(12, 12, 12, 0.78) !important;
        border: 1px solid rgba(255, 80, 80, 0.12);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px);
        animation: msgFadeIn 0.35s ease-out;
        color: #fafafa !important;
        font-weight: 600;
    }

    .stChatMessage .markdown-text-container,
    .stChatMessage p,
    .stChatMessage li,
    .stChatMessage span {
        color: #f7f7f7 !important;
        font-weight: 600 !important;
    }

    @keyframes msgFadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Chat input ── */
    .stChatInput textarea {
        border-radius: 18px !important;
        border: 1px solid rgba(255, 85, 85, 0.25) !important;
        background: rgba(26, 8, 8, 0.7) !important;
        color: #fff !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }

    .stChatInput textarea:focus {
        border-color: #ff4d4d !important;
        box-shadow: 0 0 20px rgba(255, 77, 77, 0.25) !important;
    }

    /* ── Forms — glassmorphism in Airtel shade ── */
    .stForm {
        background: rgba(16, 8, 8, 0.7);
        border: 1px solid rgba(255, 70, 70, 0.16);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(14px);
    }

    /* ── Text inputs — Airtel accent ── */
    .stTextInput input {
        border-radius: 12px;
        border: 1px solid rgba(255, 89, 89, 0.22);
        background: rgba(25, 10, 10, 0.7);
        color: #fff;
        transition: all 0.3s ease;
    }

    .stTextInput input:focus {
        border-color: #ff4d4d;
        box-shadow: 0 0 18px rgba(255, 77, 77, 0.22);
    }

    /* ── Primary buttons — Airtel gradient ── */
    .stButton button[kind="primary"],
    button[data-testid="stFormSubmitButton"] {
        background: linear-gradient(135deg, #ff4d4d 0%, #c70000 100%) !important;
        border: 1px solid rgba(255, 89, 89, 0.25) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        color: white !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.12);
    }

    .stButton button[kind="primary"]:hover,
    button[data-testid="stFormSubmitButton"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(255, 77, 77, 0.35);
    }

    /* ── Dividers ── */
    hr {
        border-color: rgba(255, 77, 77, 0.16) !important;
    }

    /* ── Custom scrollbar ── */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 77, 77, 0.25);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 77, 77, 0.45);
    }

    /* ── Success / Error alerts — Airtel tone ── */
    .stAlert {
        border-radius: 12px;
        animation: msgFadeIn 0.3s ease-out;
        border: 1px solid rgba(255, 77, 77, 0.18);
        background: rgba(40, 8, 8, 0.85) !important;
        color: #fff !important;
    }
    .stAlert .stMarkdown > div {
        color: #fff !important;
    }
    </style>
    """

st.markdown(custom_css, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# Database Bootstrap (runs once per app lifecycle)
# ═══════════════════════════════════════════════════════════════════════

@st.cache_resource
def _setup_database():
    """Initialise the MySQL database. Returns True on success, error string on failure."""
    try:
        init_db()
        return True
    except Exception as e:
        return str(e)


db_status = _setup_database()
if db_status is not True:
    st.error(
        f"⚠️ **Database initialisation failed**\n\n"
        f"`{db_status}`\n\n"
        "Please ensure your MySQL server is running and the credentials in "
        "`.env` are correct."
    )
    st.stop()


# ═══════════════════════════════════════════════════════════════════════
# Routing — auth-gated page selection
# ═══════════════════════════════════════════════════════════════════════

if is_authenticated():
    show_chat_page()
else:
    page = st.session_state.get("page", "login")
    if page == "register":
        show_register_page()
    else:
        show_login_page()
