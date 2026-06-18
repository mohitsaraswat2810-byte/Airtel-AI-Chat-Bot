"""Registration Page Component."""

import streamlit as st
from auth.auth import register_user, login_user


def show_register_page():
    """Render the registration page with a styled sign-up form."""

    # ── Centered layout ──
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # ── Branding header ──
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 2rem; margin-top: 3rem;">
                <p style="font-size: 4rem; margin-bottom: 0.5rem;">🤖</p>
                <h1 style="
                    font-size: 2.8rem;
                    background: linear-gradient(135deg, #ff4d4d 0%, #c70000 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 0.5rem;
                    font-weight: 700;
                    letter-spacing: -0.02em;
                ">AI Chatbot</h1>
                <p style="color: #8888aa; font-size: 1.05rem; font-weight: 300;">
                    Create your account to get started
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Registration form ──
        with st.form("register_form", clear_on_submit=False):
            st.markdown(
                "<h3 style='text-align:center; margin-bottom:1.5rem;'>Create Account</h3>",
                unsafe_allow_html=True,
            )

            username = st.text_input(
                "Username",
                placeholder="Letters, numbers, and underscores (3-50 chars)",
                key="reg_username",
            )
            email = st.text_input(
                "Email",
                placeholder="your@email.com",
                key="reg_email",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Minimum 6 characters",
                key="reg_password",
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                key="reg_confirm_password",
            )

            st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

            submit = st.form_submit_button(
                "Create Account", use_container_width=True, type="primary"
            )

            if submit:
                if password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message, user_id = register_user(
                        username, email, password
                    )
                    if success:
                        st.success(message)
                        # Auto-login after successful registration
                        login_user(username, password)
                        st.rerun()
                    else:
                        st.error(message)

        # ── Back to login ──
        st.markdown(
            """
            <div style="text-align: center; margin-top: 1.5rem;">
                <p style="color: #8888aa; font-size: 0.95rem;">Already have an account?</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Sign In", use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()
