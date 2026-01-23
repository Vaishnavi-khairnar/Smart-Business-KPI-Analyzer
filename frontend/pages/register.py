import streamlit as st
from utils.api import APIClient


def show():
    if st.session_state.get("authenticated", False):
        st.session_state.current_page = "Dashboard"
        st.rerun()

    st.title("📝 Register")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):

        # ✅ correct validation
        if not username or not email or not password or not confirm_password:
            st.error("All fields are required")
            return

        if password != confirm_password:
            st.error("Passwords do not match")
            return

        payload = {
            "username": username,
            "email": email,
            "password": password
        }

        with st.spinner("Registering user..."):
            try:
                client = APIClient()
                response = client.post("/auth/register", json=payload, raise_for_status=False)
            except Exception as e:
                st.error("🚨 Unable to connect to backend. Please ensure the server is running.")
                st.code(str(e))
                return

        if response.status_code in (200, 201):
            st.success("Registration successful 🎉 Please log in.")
            st.info("Redirecting to login...")
            st.session_state.current_page = "Login"
            st.rerun()
        else:
            try:
                error_data = response.json()
                # Try to get detail from either 'detail' or 'error' key
                error_msg = error_data.get("detail") or error_data.get("error", {}).get("detail", "Registration failed")
            except Exception:
                error_msg = response.text

            st.error(f"❌ {error_msg}")
