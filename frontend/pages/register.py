import streamlit as st
from utils import api


def show():
    st.title("📝 Register")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not username or not email or not password:
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
                response = api.post("/auth/register", json=payload)
            except Exception as e:
                st.error("Unable to connect to backend")
                return

        # 🔑 IMPORTANT: backend returns { message, data }
        if response.get("data"):
            st.success("Registration successful. Please log in.")
            st.session_state.current_page = "Login"
            st.rerun()
        else:
            st.error(response.get("message", "Registration failed"))