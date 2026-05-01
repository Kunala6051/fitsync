import streamlit as st
from modules.processor import process_data
import plotly.express as px
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide", page_title="Trends & Insights ")

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

        .card {{
            background: {card};
            padding: 18px;
            border-radius: 18px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
            margin-bottom: 10px;
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
st.markdown("# 📊 Trends & Insights")

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

# ---------------- SUMMARY STATS ----------------
st.markdown("## 📌 Summary Statistics")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">📈 <b>Recovery Score</b><br>'
                f"Mean: {round(filtered_df['Recovery_Score'].mean(),1)}<br>"
                f"Min: {filtered_df['Recovery_Score'].min()}<br>"
                f"Max: {filtered_df['Recovery_Score'].max()}</div>",
                unsafe_allow_html=True)

    st.markdown('<div class="card">😴 <b>Sleep Hours</b><br>'
                f"Mean: {round(filtered_df['Sleep_Hours'].mean(),1)}<br>"
                f"Min: {filtered_df['Sleep_Hours'].min()}<br>"
                f"Max: {filtered_df['Sleep_Hours'].max()}</div>",
                unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">🚶 <b>Steps</b><br>'
                f"Mean: {int(filtered_df['Steps'].mean())}<br>"
                f"Max: {filtered_df['Steps'].max()}</div>",
                unsafe_allow_html=True)

    st.markdown('<div class="card">🔥 <b>Calories Burned</b><br>'
                f"Mean: {round(filtered_df['Calories_Burned'].mean(),1)}<br>"
                f"Min: {filtered_df['Calories_Burned'].min()}<br>"
                f"Max: {filtered_df['Calories_Burned'].max()}</div>",
                unsafe_allow_html=True)

# ---------------- CHART THEME ----------------
template = "plotly_dark" if st.session_state.theme == "Dark" else "plotly_white"

# ---------------- MONTHLY TREND ----------------
filtered_df['Month'] = pd.to_datetime(filtered_df['Date']).dt.to_period('M')
monthly_avg = filtered_df.groupby('Month')['Recovery_Score'].mean().reset_index()
monthly_avg['Month'] = monthly_avg['Month'].astype(str)

st.markdown("## 📅 Monthly Recovery Trend")

fig1 = px.line(
    monthly_avg,
    x='Month',
    y='Recovery_Score',
    title='💪 Avg Recovery Score per Month',
    template=template
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------- HISTOGRAMS ----------------
st.markdown("## 📊 Distributions")

col1, col2 = st.columns(2)

def plot_hist(col, column, title):
    fig = px.histogram(filtered_df, x=column, nbins=20, title=title, template=template)
    st.plotly_chart(fig, use_container_width=True)

with col1:
    plot_hist(col1, 'Steps', "🚶 Steps Distribution")
    plot_hist(col1, 'Recovery_Score', "💪 Recovery Score Distribution")

with col2:
    plot_hist(col2, 'Calories_Burned', "🔥 Calories Distribution")
    plot_hist(col2, 'Sleep_Hours', "😴 Sleep Distribution")

st.markdown("---")