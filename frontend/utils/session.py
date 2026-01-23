from datetime import datetime
from typing import Any, Dict, Optional
import streamlit as st


# =====================================================
# AUTH STATE HELPERS
# =====================================================

def is_authenticated() -> bool:
    """Internal auth check."""
    return st.session_state.get("authenticated", False)


def is_logged_in() -> bool:
    """Alias for is_authenticated to prevent attribute errors."""
    return is_authenticated()


def check_authentication() -> bool:
    """Public auth check (used by pages)."""
    return is_authenticated()


def get_user() -> Optional[Dict[str, Any]]:
    """Get current user."""
    if is_authenticated():
        return st.session_state.get("user")
    return None


def set_user(user: Dict[str, Any]) -> None:
    """Set user in session."""
    st.session_state.user = user


# =====================================================
# TOKEN HELPERS
# =====================================================

def get_token() -> Optional[str]:
    """Internal token getter."""
    return st.session_state.get("token")


def get_auth_token() -> Optional[str]:
    """Public token getter (used by components)."""
    return get_token()


def set_token(token: str, expires_at: Optional[datetime] = None) -> None:
    """Store token and expiry."""
    st.session_state.token = token
    st.session_state.token_expires_at = expires_at


def get_auth_headers() -> Dict[str, str]:
    """Authorization header for API calls."""
    token = get_token()
    if not token:
        return {}
    return {
        "Authorization": f"Bearer {token}"
    }


# =====================================================
# SESSION CONTROL
# =====================================================

def login(user: Dict[str, Any], token: str, expires_at: Optional[datetime] = None) -> None:
    """Login and initialize session."""
    st.session_state.authenticated = True
    st.session_state.user = user
    st.session_state.token = token
    st.session_state.token_expires_at = expires_at
    st.session_state.current_page = "Dashboard"


def logout() -> None:
    """Clear session completely."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None
    st.session_state.token_expires_at = None
    st.session_state.current_page = "Login"
