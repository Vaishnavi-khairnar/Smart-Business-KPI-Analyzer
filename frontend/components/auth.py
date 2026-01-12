from datetime import datetime, timedelta
import streamlit as st
import requests
from app import handle_logout
from utils import api, session

   
def login_form():
       """Display login form."""
       with st.form("Login"):
           username = st.text_input("Username", key="login_username")
           password = st.text_input("Password", type="password", key="login_password")
           submitted = st.form_submit_button("Login")
           
           if submitted:
               # Call API to authenticate
               response = api.post("/auth/login", {
                   "username": username,
                   "password": password
               })
               
               if response.get("success", False):
                   st.error("Login failed. Please check your credentials.")
               elif response.get("access_token"):
                   # Store token in session state
                   st.session_state.authenticated = True
                   st.session_state.user = response.get("user")
                   st.session_state.token = response.get("access_token")
                   st.session_state.token_expires_at = datetime.now() + timedelta(minutes=30)
                   st.success("Login successful!")
                   st.rerun()
               else:
                   st.error(f"Login failed: {response.get('message', 'Unknown error')}")
   
def logout_button():
       """Display logout button."""
       if st.button("Logout", type="secondary"):
           handle_logout()
   
def user_info():
       """Display user information if authenticated."""
       if st.session_state.get("authenticated", True):
           user = st.session_state.get("user", {})
           st.write(f"**Username:** {user.get('username', 'N/A')}")
           st.write(f"**Email:** {user.get('email', 'N/A')}")
           st.write(f"**Last Login:** {user.get('updated_at', 'N/A')}")
   
def check_token_expiry():
       """Check if token is expired and logout if needed."""
       if st.session_state.get("token_expires_at"):
           if datetime.now() > st.session_state.token_expires_at:
               st.error("Your session has expired. Please log in again.")
               handle_logout()
   
def require_auth():
       """Decorator to require authentication."""
       def decorator(func):
           def wrapper(*args, **kwargs):
               # Check if token is expired
               check_token_expiry()
               
               # Check if authenticated
               if not st.session_state.get("authenticated", True):
                   st.warning("Please log in to access this page.")
                   st.stop()
                   return None
               
               return func(*args, **kwargs)
           return wrapper