import streamlit as st
from modules.processor import process_data
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide", page_title="FitSync ✨")

# ---------------- THEME TOGGLE ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

theme = st.sidebar.toggle("🌙 Dark Mode", value=True)

st.session_state.theme = "Dark" if theme else "Light"

# ---------------- CSS STYLING ----------------
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
        heading = "#000000"  # 👈 black headings in light mode

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
            color: {heading};  /* 👈 fix applied here */
        }}

        .card {{
            background: {card};
            padding: 20px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
            text-align: center;
        }}

        .metric {{
            font-size: 28px;
            font-weight: bold;
        }}

        .subtext {{
            font-size: 14px;
            opacity: 0.7;
        }}

        .title {{
            font-size: 42px;
            font-weight: 800;
            text-align: center;
            margin-bottom: 10px;
        }}

        .subtitle {{
            text-align: center;
            font-size: 18px;
            opacity: 0.8;
        }}

        .stPlotlyChart {{
            background: transparent;
        }}

        </style>
    """, unsafe_allow_html=True)

load_css(st.session_state.theme)

# ---------------- DATA ----------------
@st.cache_data
def get_data():
    return process_data()

df = get_data()

# ---------------- HEADER ----------------
st.markdown('<div class="title">FitSync Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered health analytics </div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🎛 Filters")

time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# ---------------- FILTER ----------------
if time_range == "Last 7 Days":
    filtered_df = df.sort_values(by='Date', ascending=False).head(7)
elif time_range == "Last 30 Days":
    filtered_df = df.sort_values(by='Date', ascending=False).head(30)
else:
    filtered_df = df

# ---------------- METRICS ----------------
avg_steps = int(filtered_df['Steps'].mean())
avg_sleep = round(filtered_df['Sleep_Hours'].mean(), 1)
avg_recovery = round(filtered_df['Recovery_Score'].mean(), 1)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="metric">🚶 {avg_steps}</div>
        <div class="subtext">Avg Steps</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="metric">😴 {avg_sleep} hrs</div>
        <div class="subtext">Avg Sleep</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="metric">💪 {avg_recovery}</div>
        <div class="subtext">Recovery Score</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("## 📊 Insights & Trends")

# ---------------- CHART THEME ----------------
template = "plotly_dark" if st.session_state.theme == "Dark" else "plotly_white"

# ---------------- CHARTS ----------------
col_left, col_right = st.columns(2)

with col_left:
    fig1 = px.line(
        filtered_df, x='Date',
        y=['Recovery_Score', 'Sleep_Hours'],
        title='💤 Recovery & Sleep Trend',
        template=template
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    fig2 = px.scatter(
        filtered_df,
        x='Steps',
        y='Recovery_Score',
        color='Sleep_Hours',
        title=' Steps vs Recovery',
        template=template
    )
    st.plotly_chart(fig2, use_container_width=True)

col_left2, col_right2 = st.columns(2)

with col_left2:
    fig3 = px.scatter(
        filtered_df,
        x='Heart_Rate_bpm',
        y='Recovery_Score',
        title='❤️ Heart Rate vs Recovery',
        template=template
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    fig4 = px.line(
        filtered_df,
        x='Date',
        y='Calories_Burned',
        title='🔥 Calories Burned Trend',
        template=template
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

