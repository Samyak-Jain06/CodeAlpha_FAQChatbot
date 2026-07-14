import time
import streamlit as st

from chatbot import FAQChatbot

# ====================================================
# PAGE CONFIG
# ====================================================

st.set_page_config(
    page_title="AI Tech Support Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================================================
# LOAD BOT
# ====================================================

bot = FAQChatbot()

# ====================================================
# SESSION STATE
# ====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ====================================================
# CUSTOM CSS
# ====================================================

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family:Inter,sans-serif;
}

.stApp{
    background:#F6F8FC;
}

.block-container{
    max-width:1100px;
    padding-top:1rem;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:white;
    border-right:1px solid #ECECEC;
}

/* Header */

.mainHeader{

background:white;

padding:20px;

border-radius:18px;

box-shadow:0 5px 18px rgba(0,0,0,.08);

margin-bottom:20px;

}

.mainHeader h1{

margin:0;

font-size:34px;

}

.mainHeader p{

margin-top:8px;

color:#666;

}

/* Bubble */

.userBubble{

background:#2563EB;

color:white;

padding:14px;

border-radius:18px 18px 4px 18px;

margin-left:18%;

margin-bottom:15px;

}

.botBubble{

background:white;

padding:14px;

border-radius:18px 18px 18px 4px;

border:1px solid #ECECEC;

margin-right:18%;

margin-bottom:18px;

}

.quickTitle{

font-weight:600;

font-size:20px;

margin-top:20px;

margin-bottom:10px;

}
/* ============================
   BUTTONS
============================ */

.stButton > button{
    width:100%;
    border-radius:14px;
    border:1px solid #E5E7EB;
    background:#FFFFFF;
    color:#111827;
    font-weight:600;
    transition:0.25s;
}

.stButton > button:hover{
    background:#2563EB;
    color:white;
    border-color:#2563EB;
}

/* ============================
   CHAT INPUT
============================ */

[data-testid="stChatInput"]{
    background:white;
    border-radius:18px;
    padding:6px;
    box-shadow:0 6px 20px rgba(0,0,0,.08);
}

/* ============================
   CHAT MESSAGES
============================ */

[data-testid="stChatMessage"]{
    border-radius:18px;
    padding:10px;
    margin-bottom:14px;
}

/* ============================
   PROGRESS BAR
============================ */

[data-testid="stProgressBar"]{
    height:8px;
}

/* ============================
   SIDEBAR BUTTON
============================ */

section[data-testid="stSidebar"] .stButton button{
    border-radius:12px;
}

/* ============================
   DIVIDER
============================ */

hr{
    margin-top:22px;
    margin-bottom:22px;
}

</style>
""", unsafe_allow_html=True)

# ====================================================
# SIDEBAR
# ====================================================

with st.sidebar:

    st.title("🤖 AI Assistant")

    st.success("🟢 Online")

    st.divider()

    if st.button("🗑 Clear Conversation", use_container_width=True):

        st.session_state.messages=[]

        st.rerun()

    st.divider()

    st.caption("Developer")

    st.write("**Samyak Jain**")

# ====================================================
# HEADER
# ====================================================

st.markdown("""

<div class="mainHeader">

<h1>🤖 AI Tech Support Assistant</h1>

<p>

Ask questions about Python, AI,
GitHub, Windows, Networking,
Linux and Computer Hardware.

</p>

</div>

""", unsafe_allow_html=True)
# ====================================================
# WELCOME
# ====================================================

if len(st.session_state.messages) == 0:

    st.markdown("""

### 👋 Welcome

I'm your **AI Tech Support Assistant**.

I can answer questions related to:

- 🐍 Python
- 🤖 Artificial Intelligence
- 💻 Windows
- 🌐 GitHub
- 📡 Networking
- 💾 Computer Hardware

""")

# ====================================================
# QUICK QUESTIONS
# ====================================================

st.markdown(
    "<div class='quickTitle'>💡 Quick Questions</div>",
    unsafe_allow_html=True
)

c1,c2,c3,c4,c5=st.columns(5)

questions={
    "🐍 Python":"What is Python?",
    "🤖 AI":"What is AI?",
    "🌐 GitHub":"What is GitHub?",
    "💻 Windows":"How do I update Windows?",
    "💾 RAM":"What is RAM?"
}

buttons=[
    ("🐍 Python",c1),
    ("🤖 AI",c2),
    ("🌐 GitHub",c3),
    ("💻 Windows",c4),
    ("💾 RAM",c5)
]

for label,col in buttons:

    with col:

        if st.button(label,use_container_width=True):

            question=questions[label]

            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":question
                }
            )

            with st.spinner("🤖 Thinking..."):

                time.sleep(.5)

                answer,confidence=bot.get_response(question)

            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":answer,
                    "confidence":confidence
                }
            )

            st.rerun()

st.divider()

# ====================================================
# CHAT HISTORY
# ====================================================

for msg in st.session_state.messages:

    if msg["role"]=="user":

        with st.chat_message("user"):

            st.markdown(msg["content"])

    else:

        with st.chat_message("assistant"):

            st.markdown(msg["content"])

            if "confidence" in msg:

                st.progress(
                    float(msg["confidence"])
                )

                st.caption(
                    f"Confidence : {msg['confidence']*100:.1f}%"
                )
# ====================================================
# CHAT INPUT
# ====================================================

prompt = st.chat_input("💬 Ask anything about technology...")

if prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # AI Thinking
    with st.spinner("🤖 Thinking..."):

        time.sleep(0.6)

        answer, confidence = bot.get_response(prompt)

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "confidence": confidence
        }
    )

    st.rerun()
