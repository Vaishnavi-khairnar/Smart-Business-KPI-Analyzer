import streamlit as st
from datetime import datetime, timedelta

from utils.api import APIClient
from utils.session import login as save_session


def show():
    if st.session_state.get("authenticated", False):
        st.session_state.current_page = "Dashboard"
        st.rerun()

    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if not email or not password:
            st.error("Please enter email and password")
            return

        client = APIClient()

        # ✅ backend expects `username`
        payload = {
            "username": email,
            "password": password
        }

        try:
            # ✅ disable automatic raising to handle 401 manually
            response = client.post("/auth/login", json=payload, raise_for_status=False)

            # ✅ handle HTTP errors properly
            if response.status_code == 401:
                st.error("❌ Invalid email/username or password")
                return

            if response.status_code not in (200, 201):
                try:
                    error_detail = response.json().get("error", {}).get("detail", "Login failed")
                except:
                    error_detail = response.text
                st.error(f"❌ Login failed: {error_detail}")
                return

            # ✅ parse JSON correctly
            response_data = response.json()
            data = response_data["data"]

            token = data["access_token"]
            user = data["user"]
            expires_in = data.get("expires_in", 1800)

            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

            # ✅ SINGLE source of truth for session
            save_session(
                user=user,
                token=token,
                expires_at=expires_at
            )

            st.success("Login successful 🎉")
            st.rerun()

        except Exception as e:
            st.error("🚨 Unable to connect to backend. Please ensure the server is running.")
            st.code(str(e))
