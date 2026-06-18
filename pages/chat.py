"""Chat Page Component — the main conversation interface."""

import streamlit as st
from db.connection import (
    create_conversation,
    get_conversations_by_user,
    get_messages_by_conversation,
    add_message,
    update_conversation_title,
    delete_conversation,
)
from models.gpt_oss import generate_response


# ═══════════════════════════════════════════════════════════════════════
# Sidebar — conversation history & controls
# ═══════════════════════════════════════════════════════════════════════

def _render_sidebar():
    """Render the sidebar with conversation list, new-chat button, and logout."""
    with st.sidebar:
        # ── Header ──
        st.markdown(
            """
            <div style="padding: 0.5rem 0 0.5rem 0;">
                <h2 style="
                    background: linear-gradient(135deg, #ff4d4d 0%, #c70000 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 0;
                    font-size: 1.5rem;
                ">💬 Conversations</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── New chat button ──
        if st.button("➕  New Chat", use_container_width=True, type="primary"):
            st.session_state["current_conversation_id"] = None
            st.session_state["messages"] = []
            st.rerun()

        st.markdown("---")

        # ── Conversation list ──
        user_id = st.session_state["user_id"]
        conversations = get_conversations_by_user(user_id)

        if not conversations:
            st.caption("No conversations yet. Start chatting!")
        else:
            for conv in conversations:
                col_title, col_delete = st.columns([5, 1])

                with col_title:
                    is_active = (
                        st.session_state.get("current_conversation_id") == conv["id"]
                    )
                    btn_type = "primary" if is_active else "secondary"
                    # Truncate long titles
                    title = conv["title"]
                    if len(title) > 28:
                        title = title[:25] + "..."
                    if st.button(
                        f"💬 {title}",
                        key=f"conv_{conv['id']}",
                        use_container_width=True,
                        type=btn_type,
                    ):
                        st.session_state["current_conversation_id"] = conv["id"]
                        st.session_state["messages"] = get_messages_by_conversation(
                            conv["id"]
                        )
                        st.rerun()

                with col_delete:
                    if st.button("🗑️", key=f"del_{conv['id']}", help="Delete"):
                        delete_conversation(conv["id"])
                        if (
                            st.session_state.get("current_conversation_id")
                            == conv["id"]
                        ):
                            st.session_state["current_conversation_id"] = None
                            st.session_state["messages"] = []
                        st.rerun()

        # ── User info & logout at bottom ──
        st.markdown("---")
        st.markdown(
            f"""
            <div style="
                padding: 0.5rem 0;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span style="
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    border-radius: 50%;
                    width: 32px;
                    height: 32px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                    font-size: 0.85rem;
                ">{st.session_state['username'][0].upper()}</span>
                <span style="font-weight: 500;">{st.session_state['username']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🚪  Logout", use_container_width=True):
            from auth.auth import logout_user

            logout_user()
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════

def _generate_title(user_message):
    """Create a short conversation title from the first user message."""
    title = user_message.strip().replace("\n", " ")
    return title[:57] + "..." if len(title) > 60 else title


def _msg_value(msg, key):
    """Extract a value from a message dict (handles both dict and obj)."""
    return msg[key] if isinstance(msg, dict) else getattr(msg, key)


# ═══════════════════════════════════════════════════════════════════════
# Main Chat Page
# ═══════════════════════════════════════════════════════════════════════

def show_chat_page():
    """Render the full chat interface: sidebar + message area + input."""

    # Initialise message buffer in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Draw sidebar
    _render_sidebar()

    # ── Header ──
    st.markdown(
        """
        <div style="text-align: center; padding: 0.25rem 0 1.25rem 0;">
            <h2 style="
                background: linear-gradient(135deg, #ff4d4d 0%, #c70000 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
                font-weight: 700;
            ">AI Assistant</h2>
            <p style="color: #666; font-size: 0.9rem; margin: 0.25rem 0 0 0;">
                Powered by GPT-OSS &bull; Ask me anything
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Display existing messages ──
    for msg in st.session_state["messages"]:
        role = _msg_value(msg, "role")
        content = _msg_value(msg, "content")
        if role != "system":
            with st.chat_message(role):
                st.markdown(content)

    # ── Welcome prompt when no messages ──
    if not st.session_state["messages"]:
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 4rem 1rem 2rem 1rem;
                color: #8888aa;
            ">
                <p style="font-size: 3.5rem; margin-bottom: 1rem; line-height: 1;">🤖</p>
                <h3 style="margin-bottom: 0.5rem; color: #aaa;">
                    How can I help you today?
                </h3>
                <p style="font-size: 0.95rem;">
                    Start a conversation by typing a message below.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Chat input ──
    if prompt := st.chat_input("Type your message..."):
        # Create conversation if needed
        if not st.session_state.get("current_conversation_id"):
            title = _generate_title(prompt)
            conv_id = create_conversation(st.session_state["user_id"], title)
            st.session_state["current_conversation_id"] = conv_id

        conv_id = st.session_state["current_conversation_id"]

        # Save & display user message
        add_message(conv_id, "user", prompt)
        st.session_state["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            # Build the full chat history for the model
            chat_history = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful, knowledgeable AI assistant. "
                        "Respond clearly and concisely. Use markdown formatting when appropriate."
                    ),
                },
            ]
            for msg in st.session_state["messages"]:
                chat_history.append(
                    {
                        "role": _msg_value(msg, "role"),
                        "content": _msg_value(msg, "content"),
                    }
                )

            try:
                # Stream the response token-by-token
                stream = generate_response(chat_history, stream=True)
                response = st.write_stream(stream)

                # Persist assistant message
                add_message(conv_id, "assistant", response)
                st.session_state["messages"].append(
                    {"role": "assistant", "content": response}
                )

                # Set title from first exchange
                db_messages = get_messages_by_conversation(conv_id)
                if len(db_messages) <= 2:
                    update_conversation_title(conv_id, _generate_title(prompt))

            except ConnectionError as e:
                st.error(
                    f"⚠️ {str(e)}\n\n"
                    "Make sure Ollama is running:\n"
                    "```\nollama run gpt-oss:20b\n```"
                )
            except RuntimeError as e:
                st.error(f"⚠️ Model error: {str(e)}")
            except Exception as e:
                st.error(f"⚠️ An unexpected error occurred: {str(e)}")
