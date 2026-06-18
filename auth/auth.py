"""
Authentication Module.

Handles user registration, login, password hashing (bcrypt),
and Streamlit session-state management.
"""

import re
import bcrypt
import streamlit as st
from db.connection import create_user, get_user_by_username, get_user_by_email


# ═══════════════════════════════════════════════════════════════════════
# Password Utilities
# ═══════════════════════════════════════════════════════════════════════

def hash_password(plain_password):
    """Hash a plaintext password with bcrypt (auto-salted)."""
    return bcrypt.hashpw(
        plain_password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(plain_password, hashed_password):
    """Verify a plaintext password against a stored bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ═══════════════════════════════════════════════════════════════════════
# Registration
# ═══════════════════════════════════════════════════════════════════════

def register_user(username, email, password):
    """
    Register a new user account.

    Validates inputs, checks uniqueness, hashes password, and creates the DB row.

    Args:
        username: Desired username (3-50 chars, alphanumeric + underscores).
        email: Valid email address.
        password: Plaintext password (min 6 characters).

    Returns:
        tuple[bool, str, int | None]: (success, message, user_id or None)
    """
    # ── Validate username ──
    if not username or len(username) < 3 or len(username) > 50:
        return False, "Username must be between 3 and 50 characters.", None
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores.", None

    # ── Validate email ──
    if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return False, "Please enter a valid email address.", None

    # ── Validate password ──
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long.", None

    # ── Check uniqueness ──
    if get_user_by_username(username):
        return False, "Username already taken. Please choose another.", None
    if get_user_by_email(email):
        return False, "An account with this email already exists.", None

    # ── Create user ──
    try:
        pw_hash = hash_password(password)
        user_id = create_user(username, email, pw_hash)
        return True, "Registration successful!", user_id
    except Exception as e:
        return False, f"Registration failed: {str(e)}", None


# ═══════════════════════════════════════════════════════════════════════
# Login / Logout / Session
# ═══════════════════════════════════════════════════════════════════════

def login_user(username, password):
    """
    Authenticate a user and populate Streamlit session state.

    Args:
        username: The username to authenticate.
        password: The plaintext password to verify.

    Returns:
        tuple[bool, str]: (success, message)
    """
    if not username or not password:
        return False, "Please enter both username and password."

    user = get_user_by_username(username)
    if not user:
        return False, "Invalid username or password."

    if not verify_password(password, user["password_hash"]):
        return False, "Invalid username or password."

    # Populate session
    st.session_state["authenticated"] = True
    st.session_state["user_id"] = user["id"]
    st.session_state["username"] = user["username"]
    st.session_state["current_conversation_id"] = None

    return True, f"Welcome back, {user['username']}!"


def logout_user():
    """Clear authentication data from session state."""
    for key in [
        "authenticated",
        "user_id",
        "username",
        "current_conversation_id",
        "messages",
    ]:
        st.session_state.pop(key, None)


def is_authenticated():
    """Return True if the current session is authenticated."""
    return st.session_state.get("authenticated", False)
