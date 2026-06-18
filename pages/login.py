"""Login Page Component."""

import streamlit as st
from auth.auth import login_user


def show_login_page():
    """Render the login page with a styled sign-in form."""

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
                    Powered by GPT-OSS &bull; Your intelligent assistant
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Login form ──
        with st.form("login_form", clear_on_submit=False):
            st.markdown(
                "<h3 style='text-align:center; margin-bottom:1.5rem;'>Sign In</h3>",
                unsafe_allow_html=True,
            )

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
            )

            st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

            submit = st.form_submit_button(
                "Sign In", use_container_width=True, type="primary"
            )

            if submit:
                success, message = login_user(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        # ── Register link ──
        st.markdown(
            """
            <div style="text-align: center; margin-top: 1.5rem;">
                <p style="color: #8888aa; font-size: 0.95rem;">Don't have an account?</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Create Account", use_container_width=True):
            st.session_state["page"] = "register"
            st.rerun()
