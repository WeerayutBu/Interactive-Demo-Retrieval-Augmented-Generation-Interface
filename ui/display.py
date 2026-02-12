import json
import streamlit as st
from utils import get_api_response


def init_state():
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("session_id", None)
    st.session_state.setdefault("model", "gpt-4o-mini")
    st.session_state.setdefault("show_details", False)


def display_sidebar():
    with st.sidebar:
        st.title("Chat Interface")
        st.selectbox(
            "Model",
            options=["gpt-4o-mini", "gpt-4o"],
            key="model",
        )
        st.toggle("Show technical details", True, key="show_details",)

        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = None
            st.rerun()


def render_message(role: str, content: str):
    avatars = {
        "user": "👤",        # human
        "assistant": "✨",   # chat bot
    }
    with st.chat_message(role, avatar=avatars.get(role, "💬")):
        st.markdown(content)


def render_details(response: dict):
    # Only show if toggled on
    if not st.session_state.show_details:
        return

    with st.expander("Technical details", expanded=False):
        st.caption("Context (facts)")
        st.code(
            json.dumps(response.get("facts", {}), indent=2, ensure_ascii=False),
            language="json",
        )

        st.caption("History")
        st.code(
            json.dumps(response.get("history", []), indent=2, ensure_ascii=False),
            language="json",
        )

        col1, col2 = st.columns(2)
        with col1:
            st.caption("Model")
            st.code(response.get("model", ""), language="text")
        with col2:
            st.caption("Session ID")
            st.code(str(response.get("session_id", "")), language="text")



def display_chat_interface():
    
    # History
    for m in st.session_state.messages:
        render_message(m["role"], m["content"])

    # Input
    prompt = st.chat_input("Type your message…")
    if not prompt:
        return

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", prompt)

    # Assistant response
    with st.spinner("Generating…"):
        response = get_api_response(
            prompt,
            st.session_state.session_id,
            st.session_state.model,
        )

    if not response or "answer" not in response:
        st.error("Couldn’t get a response. Please try again.")
        return

    # Persist session + message
    st.session_state.session_id = response.get("session_id", st.session_state.session_id)
    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

    render_message("assistant", response["answer"])
    render_details(response)

