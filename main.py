import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide", page_title="FitSync ✨")

# ---------------- THEME TOGGLE ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

theme = st.sidebar.toggle("🌙 Dark Mode", value=True)
st.session_state.theme = "Dark" if theme else "Light"

# ---------------- CSS ----------------
def load_css(theme):
    if theme == "Dark":
        bg = "linear-gradient(135deg, #1e1b2e, #2e2647)"
        card = "rgba(255,255,255,0.05)"
        text = "#ffffff"
        heading = "#ffffff"
    else:
        bg = "linear-gradient(135deg, #f3e8ff, #e9d5ff)"
        card = "rgba(255,255,255,0.7)"
        text = "#1f1f1f"
        heading = "#000000"

    st.markdown(f"""
        <style>
        .stApp {{
            background: {bg};
            color: {text};
            font-family: 'Poppins', sans-serif;
        }}

        h1, h2, h3 {{
            font-weight: 700;
            letter-spacing: 0.5px;
            color: {heading};
        }}

        .hero {{
            text-align: center;
            padding: 80px 20px;
        }}

        .hero-title {{
            font-size: 56px;
            font-weight: 800;
            margin-bottom: 10px;
        }}

        .hero-subtitle {{
            font-size: 20px;
            opacity: 0.85;
        }}

        .card {{
            background: {card};
            padding: 25px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
            text-align: center;
            margin-top: 30px;
        }}

        </style>
    """, unsafe_allow_html=True)

load_css(st.session_state.theme)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <div class="hero-title"> FitSync </div>
    <div class="hero-subtitle">
        Your AI-powered health analytics dashboard 
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- INFO CARD ----------------
st.markdown("""
<div class="card">
    🚀 Navigate using the sidebar to explore your health insights <br><br>
    📊 Track recovery, sleep, steps & performance <br>
    💡 Discover patterns and improve your lifestyle
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- FOOTER ----------------
st.markdown("### Stay consistent. Stay FitSync.")