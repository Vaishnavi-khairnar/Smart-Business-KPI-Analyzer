from datetime import datetime
from typing import Any, Dict, Optional
import streamlit as st


# -------------------------
# AUTH STATE HELPERS
# -------------------------

def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)


def get_user() -> Optional[Dict[str, Any]]:
    """Get current user from session state."""
    if is_authenticated():
        return st.session_state.get("user")
    return None


def set_user(user: Dict[str, Any]) -> None:
    """Set user in session state."""
    st.session_state.user = user


# -------------------------
# TOKEN HELPERS
# -------------------------

def get_token() -> Optional[str]:
    """Get JWT token from session state."""
    return st.session_state.get("token")


def set_token(token: str, expires_at: Optional[datetime] = None) -> None:
    """Set JWT token in session state."""
    st.session_state.token = token
    st.session_state.token_expires_at = expires_at


def get_auth_headers() -> Dict[str, str]:
    """Get Authorization header for API calls."""
    token = get_token()
    if not token:
        return {}
    return {
        "Authorization": f"Bearer {token}"
    }


# -------------------------
# SESSION CONTROL
# -------------------------

def login(user, token, expires_at):
    st.session_state.authenticated = True
    st.session_state.user = user
    st.session_state.token = token
    st.session_state.token_expires_at = expires_at



def logout() -> None:
    """Clear authentication session."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None
    st.session_state.token_expires_at = None
