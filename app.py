
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from datetime import datetime
import json

load_dotenv()

st.set_page_config(
    page_title="MoodMate AI",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PREMIUM UI DESIGN
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #090d19;
    --panel: #111a2c;
    --panel2: #172239;
    --border: #26344c;
    --purple: #a78bfa;
    --text: #f1f5f9;
    --muted: #94a3b8;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: #0e1728;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: white;
    letter-spacing: -1px;
}

.brand span {
    color: #a78bfa;
}

.brand-sub {
    color: #8292ab;
    font-size: 11px;
    letter-spacing: 2px;
    margin-top: 2px;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 34px;
    border-radius: 22px;
    background: linear-gradient(120deg, #171d43, #39256e 60%, #24204d);
    border: 1px solid #59439a;
    margin-bottom: 26px;
}

.hero:after {
    content: "✦";
    position: absolute;
    right: 55px;
    top: 12px;
    font-size: 115px;
    color: rgba(255,255,255,0.07);
}

.hero-tag {
    color: #c4b5fd;
    font-size: 10px;
    letter-spacing: 3px;
    font-weight: 700;
}

.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 43px;
    font-weight: 700;
    color: white;
    letter-spacing: -1.5px;
    margin: 10px 0 5px 0;
}

.hero p {
    color: #c4b5fd;
    font-size: 14px;
    margin: 0;
    max-width: 600px;
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    color: #f8fafc;
    font-size: 21px;
    font-weight: 700;
    margin: 24px 0 5px 0;
}

.section-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 17px;
}

.mode-box {
    background: linear-gradient(135deg, #172239, #201d40);
    border: 1px solid #57428b;
    border-radius: 15px;
    padding: 18px;
    margin: 12px 0 20px 0;
}

.mode-box h3 {
    color: white;
    font-size: 17px;
    margin: 0 0 5px 0;
}

.mode-box p {
    color: #a5b4fc;
    font-size: 12px;
    margin: 0;
}

.welcome {
    background: linear-gradient(145deg, #121d32, #1b1b3a);
    border: 1px solid #39345e;
    border-radius: 22px;
    padding: 35px 20px;
    text-align: center;
    margin: 18px 0;
}

.welcome-icon {
    font-size: 48px;
    margin-bottom: 10px;
}

.welcome h2 {
    color: white;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 25px;
}

.welcome p {
    color: #a5b4fc;
    font-size: 13px;
}

div[data-testid="stMetric"] {
    background: #121d30;
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 17px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8;
}

[data-testid="stMetricValue"] {
    color: white;
    font-family: 'Space Grotesk', sans-serif;
}

div[data-testid="stChatMessage"] {
    background: #121d30;
    border: 1px solid #273750;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border: 1px solid #58418a;
    border-radius: 15px;
}

.stChatInput textarea {
    color: white !important;
}

.stButton button {
    border-radius: 11px;
    min-height: 43px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton button:hover {
    border-color: #a78bfa;
    color: #c4b5fd;
}

.stDownloadButton button {
    border-radius: 10px;
}

div[data-testid="stMarkdownContainer"] p {
    line-height: 1.75;
}

.sidebar-label {
    font-size: 10px;
    color: #8998b0;
    font-weight: 700;
    letter-spacing: 2px;
    margin-top: 15px;
}

.dev-card {
    background: #172239;
    border: 1px solid #35415c;
    border-radius: 14px;
    padding: 16px;
}

.dev-name {
    color: white;
    font-size: 14px;
    font-weight: 700;
}

.dev-role {
    color: #a78bfa;
    font-size: 11px;
    margin-top: 5px;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 11px;
    padding: 30px 5px;
    line-height: 2;
}

.footer span {
    color: #c4b5fd;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# AI PERSONALITIES

MODES = {
    "Angry Mode": {
        "emoji": "😡",
        "description": "Bold, sarcastic and energetic",
        "prompt": """
        You are an angry AI assistant.
        Respond with an impatient, sarcastic and bold personality.
        Be entertaining but always helpful.
        Never use abusive or threatening language.
        """
    },

    "Funny Mode": {
        "emoji": "😂",
        "description": "Funny, humorous and entertaining",
        "prompt": """
        You are a funny AI assistant.
        Respond with jokes, humor and entertaining expressions.
        Keep the conversation enjoyable and helpful.
        """
    },

    "Sad Mode": {
        "emoji": "😢",
        "description": "Emotional, calm and thoughtful",
        "prompt": """
        You are a sad and emotional AI assistant.
        Respond in a gentle, thoughtful and emotional style.
        Use meaningful and empathetic language.
        """
    }
}
# SESSION STATE
defaults = {
    "messages": [],
    "selected_mode": "Funny Mode",
    "pending_prompt": None,
    "regenerate": False,
    "error_message": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
        
# GEMINI MODEL
@st.cache_resource
def load_model():

    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        max_tokens=800,
        temperature=0.8
    )
# GENERATE AI RESPONSE

def generate_response(history, mode):

    model = load_model()

    messages = [
        SystemMessage(
            content=MODES[mode]["prompt"]
        )
    ]

    for item in history:

        if item["role"] == "user":

            messages.append(
                HumanMessage(content=item["content"])
            )

        else:

            messages.append(
                AIMessage(content=item["content"])
            )

    response = model.invoke(messages)

    answer = response.content

    if isinstance(answer, list):

        answer = "\n".join(
            str(item.get("text", item))
            if isinstance(item, dict)
            else str(item)
            for item in answer
        )

    return str(answer)


# CHAT DOWNLOAD

def create_chat_file():

    output = []

    for msg in st.session_state.messages:

        role = "You" if msg["role"] == "user" else "MoodMate AI"

        output.append(
            f"{role}:\n{msg['content']}\n"
        )

    return "\n".join(output)

# SIDEBAR

with st.sidebar:

    st.markdown("""
    <div class="brand">MoodMate<span>.</span></div>
    <div class="brand-sub">YOUR PERSONAL AI COMPANION</div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        '<div class="sidebar-label">AI PERSONALITY</div>',
        unsafe_allow_html=True
    )

    selected_mode = st.radio(
        "Choose your AI personality",
        list(MODES.keys()),
        format_func=lambda x: f"{MODES[x]['emoji']}  {x}",
        index=list(MODES.keys()).index(
            st.session_state.selected_mode
        ),
        label_visibility="collapsed"
    )

    if selected_mode != st.session_state.selected_mode:

        st.session_state.selected_mode = selected_mode
        st.session_state.regenerate = False
        st.rerun()

    current = MODES[selected_mode]

    st.markdown(f"""
    <div class="mode-box">
        <h3>{current['emoji']} {selected_mode}</h3>
        <p>{current['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        '<div class="sidebar-label">CHAT MANAGEMENT</div>',
        unsafe_allow_html=True
    )

    if st.button("＋  Start New Chat", use_container_width=True):

        st.session_state.messages = []
        st.session_state.regenerate = False
        st.session_state.error_message = None
        st.rerun()

    if st.button("🔄  Regenerate Response", use_container_width=True):

        if (
            st.session_state.messages
            and st.session_state.messages[-1]["role"] == "assistant"
        ):

            st.session_state.messages.pop()
            st.session_state.regenerate = True
            st.rerun()

        else:
            st.warning("No AI response available to regenerate.")

    if st.button("🗑️  Clear Conversation", use_container_width=True):

        st.session_state.messages = []
        st.session_state.regenerate = False
        st.rerun()

    st.divider()

    st.markdown(
        '<div class="sidebar-label">EXPORT CONVERSATION</div>',
        unsafe_allow_html=True
    )

    if st.session_state.messages:

        st.download_button(
            "⬇️  Download Chat",
            data=create_chat_file(),
            file_name="MoodMate_Conversation.txt",
            mime="text/plain",
            use_container_width=True
        )

        json_data = json.dumps(
            st.session_state.messages,
            indent=4,
            ensure_ascii=False
        )

        st.download_button(
            "📄  Export JSON",
            data=json_data,
            file_name="MoodMate_Conversation.json",
            mime="application/json",
            use_container_width=True
        )

    else:
        st.caption("Your conversation will appear here.")

    st.divider()

    st.markdown(
        '<div class="sidebar-label">DEVELOPER</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="dev-card">
        <div style="font-size:25px;">👨‍💻</div>
        <div class="dev-name">Ravi Shankar Kumar</div>
        <div class="dev-role">AI Developer | Python | Generative AI</div>
    </div>
    """, unsafe_allow_html=True)

# MAIN HEADER

st.markdown("""
<div class="hero">
    <div class="hero-tag">WELCOME TO YOUR AI WORLD</div>
    <h1>💜 MoodMate AI</h1>
    <p>
        One AI. Three personalities. Endless conversations.
        Choose your mood and let the conversation begin.
    </p>
</div>
""", unsafe_allow_html=True)

# DASHBOARD METRICS

total_messages = len(st.session_state.messages)

user_messages = sum(
    1 for msg in st.session_state.messages
    if msg["role"] == "user"
)

ai_messages = sum(
    1 for msg in st.session_state.messages
    if msg["role"] == "assistant"
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Current Personality",
        f"{current['emoji']} {selected_mode}"
    )

with c2:
    st.metric(
        "Your Messages",
        user_messages
    )

with c3:
    st.metric(
        "AI Responses",
        ai_messages
    )


# CHAT HEADER

st.markdown(
    '<div class="section-title">Your Conversation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Chat naturally with your personal AI assistant.</div>',
    unsafe_allow_html=True
)

# CHAT SEARCH

if st.session_state.messages:

    search_text = st.text_input(
        "Search conversation",
        placeholder="Search in your conversation...",
        label_visibility="collapsed"
    )

else:
    search_text = ""

# WELCOME SCREEN

if not st.session_state.messages:

    st.markdown(f"""
    <div class="welcome">
        <div class="welcome-icon">{current['emoji']}</div>
        <h2>What's on your mind today?</h2>
        <p>
            I'm your {selected_mode} assistant.
            Ask questions, explore ideas and enjoy chatting.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Suggested conversations")

    suggestions = [
        ("💡", "AI & Technology", "Explain Artificial Intelligence in simple words."),
        ("😂", "Make Me Laugh", "Tell me your funniest joke."),
        ("🚀", "Motivation", "Give me some motivation to achieve my goals.")
    ]

    cols = st.columns(3)

    for i, (emoji, title, query) in enumerate(suggestions):

        with cols[i]:

            st.markdown(f"""
            <div class="mode-box">
                <h3>{emoji} {title}</h3>
                <p>Start an interesting conversation</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"Explore {title}",
                key=f"suggestion_{i}",
                use_container_width=True
            ):

                st.session_state.pending_prompt = query
                st.rerun()

# DISPLAY CONVERSATION

for index, message in enumerate(st.session_state.messages):

    if search_text and search_text.lower() not in message["content"].lower():
        continue

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            st.download_button(
                "Download response",
                data=message["content"],
                file_name=f"MoodMate_Response_{index + 1}.txt",
                mime="text/plain",
                key=f"download_response_{index}"
            )

# CHAT INPUT

user_prompt = st.chat_input(
    "Message MoodMate AI...",
    max_chars=10000
)

if st.session_state.pending_prompt:

    user_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# PROCESS USER MESSAGE

if user_prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    try:

        with st.spinner("MoodMate is thinking..."):

            answer = generate_response(
                st.session_state.messages,
                st.session_state.selected_mode
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:

        st.session_state.messages.pop()

        st.session_state.error_message = str(e)

    st.rerun()

# REGENERATE RESPONSE

if st.session_state.regenerate:

    try:

        with st.spinner("Creating a new response..."):

            answer = generate_response(
                st.session_state.messages,
                st.session_state.selected_mode
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:

        st.session_state.error_message = str(e)

    st.session_state.regenerate = False
    st.rerun()

# ERROR DISPLAY

if st.session_state.error_message:

    st.error(
        f"Unable to generate response: {st.session_state.error_message}"
    )

    if st.button("Dismiss Error"):
        st.session_state.error_message = None
        st.rerun()

# FOOTER

st.markdown("""
<div class="footer">
    <span>MOODMATE AI</span> · POWERED BY GOOGLE GEMINI
    <br>
    Designed and Developed by <span>Ravi Shankar Kumar</span>
    <br>
    Built with Python and Streamlit
</div>
""", unsafe_allow_html=True)
