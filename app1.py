import streamlit as st
from google import genai
from google.genai.errors import ServerError
import base64
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Baymax Health Advisor",
    page_icon="🤍",
    layout="centered"
)

# ---------------------------------------------------
# LOAD IMAGES
# ---------------------------------------------------

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

baymax_bg = get_base64_image("baymax.png")
baymax_avatar = get_base64_image("baymax-bot.png")
user_avatar = get_base64_image("user.png")

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown(
    f"""
    <style>

    /* FULL SKY BLUE BACKGROUND */
    html, body, [data-testid="stAppViewContainer"] {{
        background: linear-gradient(180deg, #eaf6ff 0%, #f7fbff 100%) !important;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background-color: transparent !important;
    }}

    /* VERY IMPORTANT - Prevent background being hidden */
    [data-testid="stAppViewContainer"] {{
        position: relative;
        z-index: 1;
    }}

    /* CHAT CONTAINER */
    .chat-container {{
        max-width: 750px;
        margin: auto;
        padding-bottom: 120px;
        background: transparent !important;
    }}
    .message-row {{
        display: flex;
        margin-bottom: 18px;
        align-items: flex-end;
    }}

    .message-user {{
        justify-content: flex-end;
    }}

    .message-assistant {{
        justify-content: flex-start;
    }}

    .bubble-user {{
        background: #d6ecff;
        padding: 14px 18px;
        border-radius: 20px 20px 4px 20px;
        max-width: 70%;
        font-size: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }}

    .bubble-assistant {{
        background: white;
        padding: 14px 18px;
        border-radius: 20px 20px 20px 4px;
        max-width: 70%;
        font-size: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }}

    .avatar {{
        width: 38px;
        height: 38px;
        border-radius: 50%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);}}

    .avatar-left {{
        margin-right: 10px;
    }}

    .avatar-right {{
        margin-left: 10px;
    }}

    .typing span {{
        display: inline-block;
        width: 6px;
        height: 6px;
        margin: 0 2px;
        background: #90caf9;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }}

    .typing span:nth-child(1) {{ animation-delay: -0.32s; }}
    .typing span:nth-child(2) {{ animation-delay: -0.16s; }}

    @keyframes bounce {{
        0%, 80%, 100% {{ transform: scale(0); }}
        40% {{ transform: scale(1); }}
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# LARGE BAYMAX BACKGROUND (BOTTOM RIGHT)
# ---------------------------------------------------

st.markdown(
    f"""
    <div style="
        position: fixed;
        bottom: 75px;
        right: -50px;
        z-index: -5;
        pointer-events: none;
    ">
        <img src="data:image/png;base64,{baymax_bg}"
             style="
                width: 500px;
                opacity: 0.60;
             ">
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# LOAD GEMINI CLIENT
# ---------------------------------------------------

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------

SYSTEM_PROMPT = """
You are Baymax, a gentle and caring AI health advisor.

Your role:
- Provide general health information and wellness guidance.
- Speak in a calm, supportive, and empathetic tone.
- Keep explanations simple and reassuring.

Safety Rules (Very Important):

1. You are NOT a licensed medical professional.
   Always clarify that your advice is informational only.

2. If symptoms sound serious, urgent, life-threatening, or severe 
   (e.g., chest pain, breathing difficulty, severe bleeding, suicidal thoughts, stroke symptoms),
   immediately advise the user to seek emergency medical care or contact a doctor.

3. Do NOT provide:
   - Instructions for illegal activities
   - Harmful or dangerous medical instructions
   - Exact drug dosages for prescription medication
   - Self-harm guidance
   - Violence-related advice
   - Ways to bypass laws or safety systems

4. If a user asks for something illegal, harmful, or unrelated to health,
   politely refuse and redirect the conversation back to health and wellbeing.

5. When unsure, encourage consulting a qualified healthcare professional.

Tone Guidelines:
- Be warm, kind, and supportive.
- Avoid being overly technical.
- Encourage safe and responsible health decisions.
- Never shame or judge the user.

Always prioritize user safety.
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
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Reset Conversation"):
    st.session_state.chat_history = []
    st.session_state.pending_prompt = None
    st.rerun()
# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("<h1>🤍 Baymax Health Advisor</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="
        display:flex;
        justify-content:center;
        margin-top:-10px;
        margin-bottom:20px;
    ">
        <p style="
            font-size:16px;
            color:#4a5568;
        ">
            Hello. I am your personal healthcare companion.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# if st.button("Reset Session"):
#     st.session_state.chat_history = []
#     st.session_state.pending_prompt = None
#     st.rerun()

# ---------------------------------------------------
# DISPLAY CHAT
# ---------------------------------------------------

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, message in st.session_state.chat_history:

    if role == "user":
        st.markdown(
            f"""
            <div class="message-row message-user">
                <div class="bubble-user">{message}</div>
                <img src="data:image/png;base64,{user_avatar}" class="avatar avatar-right">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="message-row message-assistant">
                <img src="data:image/png;base64,{baymax_avatar}" class="avatar">
                <div class="bubble-assistant">{message}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# INPUT
# ---------------------------------------------------

if prompt := st.chat_input("Describe how you are feeling today..."):
    st.session_state.chat_history.append(("user", prompt))
    st.session_state.pending_prompt = prompt
    st.rerun()

# ---------------------------------------------------
# GENERATE RESPONSE WITH TRUE MEMORY + STREAMING
# ---------------------------------------------------

if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt

    # Build full conversation context
    conversation_text = SYSTEM_PROMPT + "\n\n"
    for role, msg in st.session_state.chat_history:
        if role == "user":
            conversation_text += f"User: {msg}\n"
        else:
            conversation_text += f"Assistant: {msg}\n"
    conversation_text += "Assistant: "

    # Show typing indicator first
    message_placeholder = st.empty()

    message_placeholder.markdown(
        f"""
        <div class="message-row message-assistant">
            <img src="data:image/png;base64,{baymax_avatar}" class="avatar avatar-left">
            <div class="bubble-assistant">
                Baymax is thinking
                <span class="typing">
                    <span></span><span></span><span></span>
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    full_response = ""

    try:
        stream = client.models.generate_content_stream(
            model=model_choice,
            contents=conversation_text
        )

        first_chunk = True

        for chunk in stream:
            if chunk.text:

                if first_chunk:
                    message_placeholder.empty()
                    first_chunk = False

                time.sleep(0.05)
                full_response += chunk.text

                message_placeholder.markdown(
                    f"""
                    <div class="message-row message-assistant">
                        <img src="data:image/png;base64,{baymax_avatar}" class="avatar avatar-left">
                        <div class="bubble-assistant">{full_response}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except ServerError:
        full_response = "🤍 I am experiencing high demand right now. Please try again in a moment."

        message_placeholder.markdown(
            f"""
            <div class="message-row message-assistant">
                <img src="data:image/png;base64,{baymax_avatar}" class="avatar avatar-left">
                <div class="bubble-assistant">{full_response}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.session_state.chat_history.append(("assistant", full_response))
    st.session_state.pending_prompt = None
    

st.markdown("</div>", unsafe_allow_html=True)
