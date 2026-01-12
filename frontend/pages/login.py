import streamlit as st
from datetime import datetime, timedelta
from utils import api, session


def show():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Username and password are required")
            return

        payload = {
            "username": username,
            "password": password
        }

        with st.spinner("Logging in..."):
            response = api.post("/auth/login", json=payload)

        data = response.get("data")

        if data and "access_token" in data:
            expires_at = datetime.now() + timedelta(
                seconds=data.get("expires_in", 1800)
            )

            session.login(
                user=data.get("user"),
                token=data.get("access_token"),
                expires_at=expires_at
            )

            st.session_state.current_page = "Dashboard"
            st.success("Login successful")
            st.rerun()
        else:
            st.error(response.get("message", "Login failed"))
