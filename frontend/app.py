import streamlit as st
from datetime import datetime

# Import pages
from pages import dashboard, upload, settings, login, register


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
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.token = None
        st.session_state.token_expires_at = None
        st.session_state.current_page = "Register"


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

    # -------------------------
    # SIDEBAR NAVIGATION
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
    # PAGE ROUTING
    # -------------------------
    page = st.session_state.current_page

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
    # TOKEN EXPIRY CHECK
    # -------------------------
    if st.session_state.authenticated and st.session_state.token_expires_at:
        if datetime.now() > st.session_state.token_expires_at:
            handle_logout()
            st.error("Session expired. Please log in again.")


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
# RUN APP
# -------------------------
if __name__ == "__main__":
    main()
