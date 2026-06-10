# app.py
from datetime import datetime

import streamlit as st

from chains.memory import add_message_to_memory
from guide import respond_user_using_local_model, respond_user_using_api
from ui import STYLES, MODEL_DESCRIPTIONS, page_title, layout


# ---------------------------------------------------------------------------
# Page config & styling
# ---------------------------------------------------------------------------

st.set_page_config(page_title=page_title, layout=layout)
st.markdown(STYLES, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

st.session_state.setdefault("history", [])
st.session_state.setdefault("messages", [])
st.session_state.setdefault("user_message", "")
st.session_state.setdefault("api_key", "")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def render_messages() -> None:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-msg"><strong>You</strong><br><br>{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            body = msg["content"].replace("\n", "<br>")
            st.markdown(
                f'<div class="assistant-msg"><strong>Assistant</strong><br><br>{body}</div>',
                unsafe_allow_html=True,
            )
            name = msg.get("model_name", "Unknown")
            desc = msg.get("model_description", "No description available.")
            with st.expander(f"🤖 Model: {name}"):
                st.caption(desc)
    st.markdown("</div>", unsafe_allow_html=True)


def handle_local_submission(prompt: str, model_selection: bool, fast_answer: bool, online_search: bool) -> tuple[str, str, str]:
    has_history = bool(st.session_state.history)
    st.session_state.history = add_message_to_memory(st.session_state.history, "user", prompt)
    choices = [model_selection, fast_answer, has_history, online_search]
    response, model_used = respond_user_using_local_model(
        prompt, st.session_state.history, choices, st.session_state.user_message
    )
    print(f"Model used: {model_used}")
    st.session_state.history = add_message_to_memory(st.session_state.history, "assistant", response)
    model_name, model_desc = MODEL_DESCRIPTIONS.get(model_used, ("Unknown", "No description available."))
    return response, model_name, model_desc


def handle_api_submission(prompt: str, provider: str, model_tier: str, fast_answer: bool, online_search: bool) -> tuple[str, str, str]:
    has_history = bool(st.session_state.history)
    st.session_state.history = add_message_to_memory(st.session_state.history, "user", prompt)
    choices = [provider, model_tier, st.session_state.api_key, fast_answer, has_history, online_search]
    response = respond_user_using_api(
        prompt, st.session_state.history, choices, st.session_state.user_message
    )
    st.session_state.history = add_message_to_memory(st.session_state.history, "assistant", response)
    key = f"{provider.lower()}_{model_tier.lower()}"
    model_name, model_desc = MODEL_DESCRIPTIONS.get(key, ("Unknown", "No description available."))
    return response, model_name, model_desc

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

render_messages()

st.markdown('<div class="bottom-bar"><div class="bottom-inner">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    provider = st.selectbox("Provider", ["Local", "OpenAI", "Anthropic", "Google"], key="provider_select")
with col2:
    if provider == "Local":
        model_type = st.selectbox("Model Type", ["Standard", "Specialized"], key="model_selection")
    else:
        model_tier = st.selectbox("Model Tier", ["Default", "Cheap", "Best"], key="model_tier_select")

with st.form("chat_form", clear_on_submit=True):
    prompt = st.text_area("", placeholder="What do you want to do?", height=70, label_visibility="collapsed")
    fast_answer  = st.checkbox("Request Fast and Simple Answer (1-2 sentences)", value=False)
    online_search = st.checkbox("Enable Online Search for Factual Queries", value=False)

    if provider == "Local":
        is_specialized = model_type == "Specialized"
        st.info(
            "The Specialized model is optimized for complex reasoning and multi-step tasks. "
            "It may take longer to respond but can provide more detailed and accurate answers."
            if is_specialized else
            "The Standard model is designed for general use and provides a balance of speed and accuracy. "
            "It is suitable for most queries and tasks."
        )
    else:
        api_key = st.text_input(f"{provider} API Key", type="password", placeholder=f"Enter your {provider} API key...")
        if api_key:
            st.session_state.api_key = api_key
        st.caption(
            f"Your API key is sent directly to {provider} and is never stored. "
            "It is required to authenticate your requests to their servers on your behalf."
        )

    submitted = st.form_submit_button("Send")

st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Submission handler
# ---------------------------------------------------------------------------

if submitted and prompt.strip():
    st.session_state.user_message += "\n" + prompt
    current_time = datetime.now().strftime("%I:%M %p")

    st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})

    if provider == "Local":
        response, model_name, model_desc = handle_local_submission(prompt, is_specialized, fast_answer, online_search)
    else:
        response, model_name, model_desc = handle_api_submission(prompt, provider, model_tier, fast_answer, online_search)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "time": current_time,
        "model_name": model_name,
        "model_description": model_desc,
    })

    st.rerun()