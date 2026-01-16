import streamlit as st
from datetime import datetime, timedelta

from utils.api import APIClient
from utils.session import login as save_session


def show():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if not email or not password:
            st.error("Please enter email and password")
            return

        client = APIClient()

        payload = {
            "username": email,
            "password": password
        }

        try:
            response = client.post("auth/login", json=payload)

            data = response["data"]
            token = data["access_token"]
            user = data["user"]

            expires_at = datetime.utcnow() + timedelta(minutes=60)

            # ✅ Save backend session
            save_session(user=user, token=token, expires_at=expires_at)

            # 🔥 REQUIRED FOR STREAMLIT ROUTING
            st.session_state.authenticated = True
            st.session_state.user = user
            st.session_state.token = token
            st.session_state.token_expires_at = expires_at
            st.session_state.current_page = "Dashboard"

            st.success("Login successful")
            st.rerun()

        except Exception as e:
            st.error("Login failed")

            if hasattr(e, "response") and e.response is not None:
                st.json(e.response.json())
            else:
                st.exception(e)
