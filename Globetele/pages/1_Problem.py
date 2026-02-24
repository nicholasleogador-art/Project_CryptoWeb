import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import time
import textwrap
from navbar import create_header # Import the header

# 1. Setup
st.set_page_config(page_title="The Problem", layout="wide")

# 2. Call the header
create_header()

# --- 1. SETUP ---
st.set_page_config(page_title="The Problem", layout="wide")

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# --- 2. LOADING SCREEN ---
if 'problem_page_loaded' not in st.session_state:
    loader_spot = st.empty()
    st.markdown("""
    <style>
    .loader-container { display: flex; justify-content: center; align-items: center; flex-direction: column; height: 60vh; }
    .loading-text { font-family: 'Arial', sans-serif; font-size: 16px; color: #555; margin-top: 20px; font-weight: bold; }
    .pie-chart { width: 150px; height: 150px; border-radius: 50%; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: background 0.1s linear; }
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = "#d9534f", "#428bca", "#f0ad4e", "#5cb85c"

    for percent in range(0, 101, 2):
        gradient = ""
        if percent > 0: gradient += f"{c1} 0% {min(percent, 25)}%"
        if percent > 25: gradient += f", {c2} 25% {min(percent, 50)}%"
        if percent > 50: gradient += f", {c3} 50% {min(percent, 75)}%"
        if percent > 75: gradient += f", {c4} 75% {min(percent, 100)}%"
        gradient += f", #f0f0f0 {percent}% 100%"

        status = "Initializing..."
        if percent > 25: status = "Cleaning Data..."
        if percent > 50: status = "Parsing Challenges..."
        if percent > 75: status = "Calculating Friction..."
        if percent == 100: status = "Analysis Complete!"

        loader_spot.markdown(f"""
        <div class="loader-container">
        <div class="pie-chart" style="background: conic-gradient({gradient});"></div>
        <div class="loading-text">{status} {percent}%</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.01)

    time.sleep(0.3)
    loader_spot.empty()
    st.session_state['problem_page_loaded'] = True

# --- 3. DATA LOADING ---
try:
    from data_cleaning import DataCleaning
except ImportError:
    st.error("Could not find data_cleaning.py.")
    st.stop()


@st.cache_data
def load_and_process_data():
    csv_path = os.path.join(parent_dir, "Data1.csv")
    if not os.path.exists(csv_path):
        st.error(f"File not found: {csv_path}")
        st.stop()

    cleaner = DataCleaning(csv_path)
    df = cleaner.drop()
    stats = cleaner.indiv()
    return df, stats


df, stats = load_and_process_data()


# --- 4. SENTIMENT LOGIC ---
def get_simple_sentiment(text):
    if not isinstance(text, str): return "Neutral"
    text = text.lower()
    neg_words = ['slow', 'hard', 'bad', 'difficult', 'no', 'problem', 'fail', 'ignored', 'wait', 'rude', 'useless',
                 'none', 'lack']
    pos_words = ['good', 'great', 'fast', 'helpful', 'thanks', 'easy', 'love', 'excellent']
    score = 0
    for w in neg_words:
        if w in text: score -= 1
    for w in pos_words:
        if w in text: score += 1
    if score < 0: return "Negative"
    if score > 0: return "Positive"
    return "Neutral"


if 'comments' in df.columns:
    df['Sentiment_Calculated'] = df['comments'].apply(get_simple_sentiment)
else:
    df['Sentiment_Calculated'] = "Neutral"

# --- 5. PAGE STYLING (DARK CONTAINER MODE) ---
DARK_BG = "#262730"

st.markdown(f"""
<style>
    .stApp {{ background-color: #ffffff; color: #333333; }}

    div.block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}

    h1, h2, h3 {{ color: #002e6e; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }}

    /* KPI Cards */
    .kpi-card {{
        background-color: #f8f9fa;
        border-left: 5px solid #d9534f;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        text-align: center;
    }}
    .kpi-title {{ font-size: 13px; color: #888; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }}
    .kpi-value {{ font-size: 32px; color: #333; font-weight: 800; margin-top: 5px; }}

    /* --- DARK CARD STYLING --- */

    /* Top Bun (Header) */
    .card-header {{
        background-color: {DARK_BG};
        padding: 15px 20px 10px 20px;
        border-radius: 15px 15px 0 0;
        border: none;
    }}
    .card-title {{
        font-size: 16px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        text-align: center;
    }}

    /* Bottom Bun (Footer) */
    .card-footer {{
        background-color: {DARK_BG};
        height: 20px; 
        border-radius: 0 0 15px 15px;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        margin-top: -30px; /* Pulls footer up to close gap */
        position: relative;
        z-index: 1;
    }}
</style>
""", unsafe_allow_html=True)

st.title("The Operational Gap")
st.markdown("### Why the current model is failing Deaf customers.")
st.markdown("---")

# --- 6. KPI SECTION ---
total_respondents = len(df)

friction_rate = "N/A"
if 'encountered_challenges_bool' in df.columns:
    friction_count = df[df['encountered_challenges_bool'].astype(str).str.contains('Yes', case=False, na=False)].shape[
        0]
    friction_pct = int((friction_count / total_respondents) * 100) if total_respondents > 0 else 0
    friction_rate = f"{friction_pct}%"

visual_issue_rate = "N/A"
if 'challenges_list' in df.columns:
    visual_count = df[df['challenges_list'].astype(str).str.contains('visual|display', case=False, na=False)].shape[0]
    visual_pct = int((visual_count / total_respondents) * 100) if total_respondents > 0 else 0
    visual_issue_rate = f"{visual_pct}%"

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Sample Size</div><div class="kpi-value">{total_respondents}</div></div>',
        unsafe_allow_html=True)
with c2:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Reported Difficulty</div><div class="kpi-value" style="color: #d9534f;">{friction_rate}</div></div>',
        unsafe_allow_html=True)
with c3:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Lack of Visual Info</div><div class="kpi-value">{visual_issue_rate}</div></div>',
        unsafe_allow_html=True)

# --- 7. CHARTS SECTION (3 COLUMNS NOW) ---
st.subheader("📊 Deep Dive Analysis")

# Splitting into 3 columns: Bar chart gets the most space (1.6), Donuts get equal space (1, 1)
col_bar, col_globe, col_pie = st.columns([1.6, 1, 1])

# --- 1. VERTICAL BAR CHART ---
with col_bar:
    st.markdown('<div class="card-header"><p class="card-title">Top 4 Reported Challenges</p></div>',
                unsafe_allow_html=True)

    if 'challenges' in stats:
        top_challenges = stats['challenges'].head(4)
        counts = top_challenges.reset_index()
        counts.columns = ['Barrier', 'Count']
        counts = counts.sort_values(by="Count", ascending=False)


        def custom_wrap(text):
            return "<br>".join(textwrap.wrap(text, width=15))


        counts['Barrier'] = counts['Barrier'].apply(custom_wrap)

        fig = px.bar(counts, x='Barrier', y='Count',
                     text='Count',
                     color_discrete_sequence=['#4dabf7'])

        fig.update_layout(
            paper_bgcolor=DARK_BG,
            plot_bgcolor=DARK_BG,
            font={'color': 'white'},
            height=450,
            margin=dict(l=20, r=20, t=10, b=90),
            xaxis=dict(title=None, tickangle=0),
            yaxis=dict(title=None, showgrid=True, gridcolor='#444444')
        )
        fig.update_traces(textposition='outside', width=0.5)

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning("Data missing for challenges.")

    st.markdown('<div class="card-footer"></div>', unsafe_allow_html=True)

# --- 2. GLOBE USERS DONUT CHART ---
with col_globe:
    st.markdown('<div class="card-header"><p class="card-title">Globe User Base</p></div>', unsafe_allow_html=True)

    if 'globe_user' in df.columns:
        # Clean up data just in case of typos
        df['globe_user_clean'] = df['globe_user'].astype(str).str.strip().str.title()
        globe_counts = df['globe_user_clean'].value_counts().reset_index()
        globe_counts.columns = ['Response', 'Count']

        # Custom colors: Globe Blue for Yes, Red for No
        color_map_globe = {"Yes": "#0057e7", "No": "#ef476f", "Nan": "#888888"}

        fig_globe = px.pie(globe_counts, values='Count', names='Response',
                           hole=0.6, color='Response', color_discrete_map=color_map_globe)

        fig_globe.update_layout(
            paper_bgcolor=DARK_BG,
            plot_bgcolor=DARK_BG,
            font={'color': 'white'},
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="white")),
            height=450,
            margin=dict(l=20, r=20, t=10, b=50)
        )

        # Get the "Yes" count to display in the center
        yes_data = globe_counts[globe_counts['Response'] == 'Yes']['Count']
        yes_count = yes_data.values[0] if not yes_data.empty else 0

        fig_globe.add_annotation(text=f"{yes_count}", x=0.5, y=0.5, font_size=30, showarrow=False, font_weight="bold",
                                 font_color="white")
        fig_globe.add_annotation(text="Current Users", x=0.5, y=0.4, font_size=12, showarrow=False,
                                 font_color="#cccccc")

        st.plotly_chart(fig_globe, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning("Globe User data unavailable.")

    st.markdown('<div class="card-footer"></div>', unsafe_allow_html=True)

# --- 3. SENTIMENT DONUT CHART ---
with col_pie:
    st.markdown('<div class="card-header"><p class="card-title">Sentiment Snapshot</p></div>', unsafe_allow_html=True)

    if 'Sentiment_Calculated' in df.columns:
        sent_counts = df['Sentiment_Calculated'].value_counts().reset_index()
        sent_counts.columns = ['Sentiment', 'Count']

        color_map_sent = {"Negative": "#ef476f", "Neutral": "#e9ecef", "Positive": "#06d6a0"}
        fig2 = px.pie(sent_counts, values='Count', names='Sentiment',
                      hole=0.6, color='Sentiment', color_discrete_map=color_map_sent)

        fig2.update_layout(
            paper_bgcolor=DARK_BG,
            plot_bgcolor=DARK_BG,
            font={'color': 'white'},
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="white")),
            height=450,
            margin=dict(l=20, r=20, t=10, b=50)
        )

        total_comments = sent_counts['Count'].sum()
        fig2.add_annotation(text=f"{total_comments}", x=0.5, y=0.5, font_size=30, showarrow=False, font_weight="bold",
                            font_color="white")
        fig2.add_annotation(text="Comments", x=0.5, y=0.4, font_size=12, showarrow=False, font_color="#cccccc")

        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning("Sentiment data unavailable.")

    st.markdown('<div class="card-footer"></div>', unsafe_allow_html=True)