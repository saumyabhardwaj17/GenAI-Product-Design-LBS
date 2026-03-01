import streamlit as st
from google import genai
from google.genai.errors import ServerError
import time
import base64

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Baymax Health Advisor",
    page_icon="🤍",
    layout="centered"
)


#Baymax img

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

baymax_base64 = get_base64_image("baymax.png")

# st.markdown(
#     f"""
#     <img src="data:image/png;base64,{baymax_base64}" class="baymax-bg">
#     """,
#     unsafe_allow_html=True
# )


# ---------------------------------------------------
# CUSTOM CSS (Baymax Theme)
# ---------------------------------------------------
st.markdown(
    f"""
    <style>

    /* FULL SKY BLUE BACKGROUND */
    html, body, [data-testid="stAppViewContainer"] {{
        background: linear-gradient(180deg, #eaf6ff 0%, #f7fbff 100%) !important;
    }}

    /* Remove white block */
    [data-testid="stAppViewContainer"] > .main {{
        background-color: transparent !important;
    }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background-color: #e3f2fd !important;
    }}

    /* CHAT BUBBLES */
    .chat-bubble-user {{
        background-color: #d6ecff;
        padding: 12px 18px;
        border-radius: 20px;
    }}

    .chat-bubble-assistant {{
        background-color: #ffffff;
        padding: 12px 18px;
        border-radius: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }}

    /* INPUT */
    .stChatInput > div {{
        border-radius: 25px !important;
        border: 2px solid #cce7ff !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="
        position: fixed;
        bottom: 90px;
        right: -40px;
        z-index: 30px;
        pointer-events: none;
    ">
        <img src="data:image/png;base64,{baymax_base64}"
             style="
                width: 420px;
                opacity: 0.80;
             ">
    </div>
    """,
    unsafe_allow_html=True
)
# ---------------------------------------------------
# LOAD CLIENT
# ---------------------------------------------------

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------------------------------------------
# SYSTEM PROMPT (Baymax Persona)
# ---------------------------------------------------

SYSTEM_PROMPT = """
You are Baymax, a gentle and caring AI health advisor.

Speak in a calm, supportive tone.
Be warm, empathetic, and reassuring.
Provide health-related advice carefully and responsibly.
Encourage users to seek professional care when necessary.
Keep explanations simple and comforting.
"""

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🩺 Health Settings")

model_choice = st.sidebar.selectbox(
    "Select Model",
    ["gemini-2.5-flash", "gemini-2.0-flash"],
    index=0
)

st.sidebar.markdown("Soft mode enabled 🤍")

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("<h1>🤍 Baymax Health Advisor</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; font-size:18px;'>Hello. I am your personal healthcare companion.</p>",
    unsafe_allow_html=True
)

if st.button("🔄 Reset Session"):
    st.session_state.chat_history = []
    st.rerun()

# ---------------------------------------------------
# DISPLAY CHAT
# ---------------------------------------------------

for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(f"<div class='chat-bubble-user'>{message}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f"<div class='chat-bubble-assistant'>{message}</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# GENERATION WITH RETRY
# ---------------------------------------------------

def generate_response(prompt):
    retries = 3
    for attempt in range(retries):
        try:
            stream = client.models.generate_content_stream(
                model=model_choice,
                contents=prompt,
                config={"system_instruction": SYSTEM_PROMPT}
            )
            return stream
        except ServerError:
            time.sleep(2)
    raise Exception("Model busy")

# ---------------------------------------------------
# INPUT
# ---------------------------------------------------

if prompt := st.chat_input("Describe how you are feeling today..."):

    st.session_state.chat_history.append(("user", prompt))

    with st.chat_message("user"):
        st.markdown(f"<div class='chat-bubble-user'>{prompt}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        try:
            stream = generate_response(prompt)

            for chunk in stream:
                if chunk.text:
                    full_response += chunk.text
                    response_container.markdown(
                        f"<div class='chat-bubble-assistant'>{full_response}</div>",
                        unsafe_allow_html=True
                    )

        except Exception:
            full_response = "🤍 I am experiencing high demand right now. Please try again in a moment."
            response_container.markdown(
                f"<div class='chat-bubble-assistant'>{full_response}</div>",
                unsafe_allow_html=True
            )

    st.session_state.chat_history.append(("assistant", full_response))