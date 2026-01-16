import streamlit as st
from datetime import datetime, timezone

# Import pages
from pages import dashboard, upload, settings, login, register
from pages import reports

# -------------------------
# GLOBAL CSS
# -------------------------
def load_global_css():
    st.markdown(
        """
        <style>
        .main .stContainer {
            max-width: 1200px;
            padding: 2rem 1rem;
            background-color: #f0f2f6;
        }

        .stMetricCard {
            background-color: white;
            border: 1px solid #e6e6e9;
            border-radius: 0.5rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .stDataFrame {
            border: 1px solid #ddd;
            border-radius: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# -------------------------
# SESSION INIT
# -------------------------
def init_session():
    defaults = {
        "authenticated": False,
        "user": None,
        "token": None,
        "token_expires_at": None,
        "current_page": "Register"
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# -------------------------
# LOGOUT HANDLER
# -------------------------
def handle_logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None
    st.session_state.token_expires_at = None
    st.session_state.current_page = "Login"
    st.rerun()


# -------------------------
# NORMALIZE TOKEN EXPIRY (🔥 FIX)
# -------------------------
def normalize_token_expiry():
    """
    Ensures token_expires_at is timezone-aware (UTC)
    """
    expiry = st.session_state.token_expires_at

    if isinstance(expiry, datetime) and expiry.tzinfo is None:
        st.session_state.token_expires_at = expiry.replace(tzinfo=timezone.utc)


# -------------------------
# MAIN APP
# -------------------------
def main():
    st.set_page_config(
        page_title="Smart Business KPI Analyzer",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    load_global_css()
    init_session()

    # Normalize token expiry once per run
    if st.session_state.token_expires_at:
        normalize_token_expiry()

    # -------------------------
    # SIDEBAR
    # -------------------------
    with st.sidebar:
        st.title("Navigation")

        if st.session_state.authenticated:
            if st.button("Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"

            if st.button("Upload Data", use_container_width=True):
                st.session_state.current_page = "Upload"

            if st.button("Settings", use_container_width=True):
                st.session_state.current_page = "Settings"

            if st.button("Logout", use_container_width=True):
                handle_logout()

        else:
            if st.button("Login", use_container_width=True):
                st.session_state.current_page = "Login"

            if st.button("Register", use_container_width=True):
                st.session_state.current_page = "Register"

    # -------------------------
    # ROUTE PROTECTION
    # -------------------------
    page = st.session_state.current_page

    if not st.session_state.authenticated:
        if page not in ["Login", "Register"]:
            st.session_state.current_page = "Login"
            st.rerun()

    # -------------------------
    # PAGE ROUTING
    # -------------------------
    if page == "Register":
        register.show()

    elif page == "Login":
        login.show()

    elif page == "Dashboard":
        dashboard.show()

    elif page == "Upload":
        upload.show()

    elif page == "Settings":
        settings.show()

    else:
        login.show()

    # -------------------------
    # TOKEN EXPIRY CHECK (✅ SAFE)
    # -------------------------
    if st.session_state.authenticated and st.session_state.token_expires_at:
        if datetime.now(timezone.utc) > st.session_state.token_expires_at:
            handle_logout()
            st.error("Session expired. Please log in again.")
    
    if page == "Reports":
        reports.render_reports_page()


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    main()
