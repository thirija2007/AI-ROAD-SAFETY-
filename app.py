import streamlit as st
from groq import Groq

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Road Safety Assistant",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; color: #e8eaed; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #111827 100%);
        border-right: 1px solid #2d3748;
    }

    /* Chat messages */
    .chat-user {
        background: linear-gradient(135deg, #1e3a5f, #1a2f4a);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
    }
    .chat-bot {
        background: linear-gradient(135deg, #1a2e1a, #162516);
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
    }

    /* SDG badges */
    .sdg-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
    }
    .sdg3  { background: #2d6a2d; color: #86efac; border: 1px solid #22c55e; }
    .sdg11 { background: #1a3a5c; color: #93c5fd; border: 1px solid #3b82f6; }

    /* Header */
    .hero-header {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        text-align: center;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3b82f6, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Input box */
    .stTextInput > div > div > input {
        background-color: #1e2533;
        border: 1px solid #374151;
        color: #e8eaed;
        border-radius: 8px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 20px;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        transform: translateY(-1px);
    }

    /* Tip cards */
    .tip-card {
        background: #1e2533;
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 14px;
        margin: 8px 0;
    }
    .tip-icon { font-size: 1.4rem; }

    /* Warning box */
    .warn-box {
        background: #2d1a0a;
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 10px 14px;
        color: #fcd34d;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── System Prompt ───────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a Road Safety Assistant — a knowledgeable, friendly, and responsible AI focused exclusively on road safety.

Your scope covers:
- Road safety tips for drivers, motorcyclists, cyclists, and pedestrians
- Traffic signs, signals, and road markings explained clearly
- Safe driving practices: speed limits, seatbelts, phone use, drunk driving, fatigue
- Pedestrian and cyclist safety rules
- Emergency procedures after road accidents
- Road safety for children and school zones
- Weather-related driving advice
- SDG 3 (Good Health & Well-being) and SDG 11 (Sustainable Cities) connections to road safety

Rules:
1. ONLY answer questions related to road safety. If asked about anything else, politely redirect: "I'm specialized in road safety topics only. Could you ask me something about road safety?"
2. Always be clear, practical, and actionable.
3. For emergencies, always advise calling local emergency services (e.g., 911 or local equivalent) first.
4. Use bullet points for tips and numbered steps for procedures.
5. Mention relevant SDG goals when appropriate.
6. Keep responses concise but complete — aim for 100–250 words.
7. Never provide legal advice; direct users to local traffic authorities for legal queries.
"""

# ─── Groq Client ─────────────────────────────────────────────────────────────
def get_groq_client(api_key: str):
    return Groq(api_key=api_key)

def chat_with_groq(client, messages: list) -> str:
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            max_tokens=512,
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ─── Session State ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚦 Road Safety Bot")
    st.markdown("---")

    # API Key input
    st.markdown("### 🔑 Groq API Key")
    api_key_input = st.text_input(
        "Enter your Groq API key",
        type="password",
        value=st.session_state.api_key,
        placeholder="gsk_..."
    )
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✅ API key set")

    st.markdown("---")

    # Quick prompts
    st.markdown("### 💬 Quick Questions")
    quick_prompts = [
        "What are the top 5 road safety tips?",
        "Explain what a yellow traffic light means",
        "How do I drive safely in heavy rain?",
        "What should I do after a car accident?",
        "Pedestrian safety rules for children",
    ]
    for prompt in quick_prompts:
        if st.button(prompt, use_container_width=True):
            st.session_state.pending_prompt = prompt

    st.markdown("---")

    # SDG Info
    st.markdown("### 🌍 SDG Alignment")
    st.markdown("""
    <span class="sdg-badge sdg3">SDG 3 — Good Health</span><br>
    <span class="sdg-badge sdg11">SDG 11 — Safe Cities</span>
    <p style="font-size:0.8rem; color:#94a3b8; margin-top:10px;">
    Road crashes kill ~1.35M people yearly. This chatbot supports safer roads for all.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ─── Main Area ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <p class="hero-title">🚦 Road Safety Assistant</p>
    <p style="color:#94a3b8; margin:4px 0 0;">Powered by Groq · Aligned with SDG 3 & SDG 11</p>
</div>
""", unsafe_allow_html=True)

# API key warning
if not st.session_state.api_key:
    st.markdown("""
    <div class="warn-box">
    ⚠️ <strong>No API key set.</strong> Enter your Groq API key in the sidebar to start chatting.
    Get a free key at <a href="https://console.groq.com" target="_blank" style="color:#fbbf24;">console.groq.com</a>
    </div>
    """, unsafe_allow_html=True)

# Chat history
chat_container = st.container()
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding: 40px; color:#64748b;">
            <div style="font-size:3rem;">🛣️</div>
            <p>Ask me anything about road safety!<br>
            Try: <em>"What are the top 5 driving tips?"</em></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-user">
                    <strong>🧑 You</strong><br>{msg["content"]}
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bot">
                    <strong>🚦 Assistant</strong><br>{msg["content"]}
                </div>""", unsafe_allow_html=True)

# ─── Input Area ───────────────────────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Ask about road safety...",
        key="chat_input",
        placeholder="e.g. What does a flashing red light mean?",
        label_visibility="collapsed"
    )

with col2:
    send_clicked = st.button("Send 🚀", use_container_width=True)

# Handle quick prompt buttons
if "pending_prompt" in st.session_state:
    user_input = st.session_state.pending_prompt
    del st.session_state.pending_prompt
    send_clicked = True

# Process message
if (send_clicked or user_input) and user_input.strip():
    if not st.session_state.api_key:
        st.error("Please enter your Groq API key in the sidebar first.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

        client = get_groq_client(st.session_state.api_key)
        with st.spinner("🚦 Thinking..."):
            reply = chat_with_groq(client, st.session_state.messages)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()