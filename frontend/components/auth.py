from datetime import datetime, timedelta
import streamlit as st
from app import handle_logout
from utils.api import APIClient

   
def login_form():
    """Display login form."""
    with st.form("Login"):
        email = st.text_input("Email/Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            client = APIClient()
            # Call API to authenticate
            payload = {
                "username": email,
                "password": password
            }
            try:
                response = client.post("/auth/login", json=payload, raise_for_status=False)
                
                if response.status_code in (200, 201):
                    data = response.json().get("data", {})
                    # Store session
                    from utils.session import login as save_session
                    save_session(
                        user=data.get("user"),
                        token=data.get("access_token"),
                        expires_at=datetime.utcnow() + timedelta(seconds=data.get("expires_in", 1800))
                    )
                    st.success("Login successful! 🎉")
                    st.rerun()
                elif response.status_code == 401:
                    st.error("❌ Invalid email/username or password")
                else:
                    st.error(f"Login failed: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")
   
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