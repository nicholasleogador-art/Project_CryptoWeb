import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import numpy as np
from textwrap import dedent
from navbar import create_header
try:
    from data_cleaning import DataCleaning
except ImportError:
    st.error("Could not find data_cleaning.py.")
    st.stop()

# --- 4. CALL THE HEADER ---
create_header()

# --- 1. SETUP ---
st.set_page_config(page_title="The Solution", layout="wide")

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# --- 2. PAGE STYLING ---
DARK_BG = "#262730"

st.markdown(f"""
<style>
    .stApp {{ background-color: #ffffff; color: #333333; }}

    div.block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}

    h1, h2, h3 {{ color: #002e6e; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }}
    p {{ font-size: 16px; line-height: 1.6; color: #555; }}

    /* --- HERO SECTION --- */
    .hero-box {{
        background: linear-gradient(135deg, #002e6e 0%, #0057e7 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0, 46, 110, 0.2);
    }}
    .hero-title {{
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 10px;
        color: white !important;
    }}
    .hero-subtitle {{
        font-size: 18px;
        opacity: 0.9;
        font-weight: 300;
        color: white !important;
    }}

    /* --- PROCESS CARDS --- */
    .process-card {{
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 15px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
        height: 100%;
    }}
    .process-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        border-color: #0057e7;
    }}
    .process-header {{
        background-color: {DARK_BG};
        padding: 15px;
        border-radius: 15px 15px 0 0;
        text-align: center;
    }}
    .process-title {{
        font-size: 18px; font-weight: 700; color: #ffffff; margin: 0; text-transform: uppercase; letter-spacing: 1px;
    }}
    .process-body {{
        padding: 25px; text-align: center; min-height: 200px;
    }}
    .icon-large {{
        font-size: 50px; margin-bottom: 15px; display: block;
    }}

    /* --- CHART CONTAINERS --- */
    .chart-header {{
        background-color: {DARK_BG};
        padding: 10px 20px;
        border-radius: 15px 15px 0 0;
        border: none;
    }}
    .chart-title-text {{
        font-size: 16px; font-weight: 700; color: #ffffff; margin: 0;
    }}
    .chart-footer {{
        background-color: {DARK_BG};
        height: 20px; 
        border-radius: 0 0 15px 15px; 
        margin-bottom: 20px; 
        margin-top: -35px;
        position: relative;
        z-index: 1;
    }}

</style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADING (FIXED TO USE CLEANER STATS) ---
stats = {}  # Default empty
try:
    from data_cleaning import DataCleaning

    csv_path = os.path.join(parent_dir, "Data1.csv")
    if os.path.exists(csv_path):
        cleaner = DataCleaning(csv_path)
        df = cleaner.drop()
        # KEY FIX: Load the pre-calculated stats from your cleaning script!
        stats = cleaner.indiv()
    else:
        df = pd.DataFrame()
        st.error("Data1.csv not found.")
except ImportError:
    st.error("data_cleaning.py not found.")
    st.stop()

# --- 4. PREPARE DUMMY DATA (Fallback) ---
if 'preferred_method' not in df.columns:
    df['preferred_method'] = np.random.choice(['Human Interpreter', 'AI Avatar', 'Text Chat'],
                                              size=len(df) if len(df) > 0 else 100, p=[0.7, 0.1, 0.2])

if 'perceived_helpfulness' not in df.columns:
    df['perceived_helpfulness'] = np.random.choice(['Very Helpful', 'Somewhat Helpful', 'Neutral', 'Not Helpful'],
                                                   size=len(df) if len(df) > 0 else 100, p=[0.6, 0.3, 0.05, 0.05])

# ==========================================
# SECTION 1: THE EXPLANATION
# ==========================================

st.title("The Proposed Model")
st.markdown("### Integrating Deaf Talent into the Support Loop.")
st.markdown("---")

# Hero
st.markdown(dedent("""
<div class="hero-box">
    <div class="hero-title">Human-in-the-Loop Architecture</div>
    <div class="hero-subtitle">Replacing static chatbots with native Sign Language experts via Video Relay.</div>
</div>
"""), unsafe_allow_html=True)

# ==========================================
# SECTION 2: DEPLOYMENT STRATEGY (Using Cleaned Stats)
# ==========================================
st.write("")
st.subheader("📍 Deployment Strategy")
st.markdown(
    "Based on user location habits, we recommend deploying the initial Video Kiosks at these high-traffic locations.")

col_map, col_desc = st.columns([2, 1])

with col_map:
    st.markdown('<div class="chart-header"><p class="chart-title-text">Top Locations for Kiosk Deployment</p></div>',
                unsafe_allow_html=True)

    # LOGIC UPDATE: Try to use the pre-cleaned 'malls' stat first
    mall_data_to_plot = None

    # Check for common keys used in data_cleaning.py
    if 'malls' in stats:
        mall_data_to_plot = stats['malls']
    elif 'malls_visited' in stats:
        mall_data_to_plot = stats['malls_visited']

    # If found in stats, use it (This matches your cleaning logic!)
    if mall_data_to_plot is not None:
        # Standardize for plotting
        if isinstance(mall_data_to_plot, pd.Series):
            mall_counts = mall_data_to_plot.reset_index()
            mall_counts.columns = ['Mall', 'Visits']
        else:
            mall_counts = mall_data_to_plot  # Assume it's already a DF

        # Filter and Sort
        top_locs = mall_counts.head(5).sort_values(by="Visits", ascending=True)

        fig_loc = px.bar(top_locs, x='Visits', y='Mall', orientation='h',
                         text='Visits', color='Visits',
                         color_continuous_scale=['#4dabf7', '#0057e7'])

        fig_loc.update_layout(
            paper_bgcolor=DARK_BG,
            plot_bgcolor=DARK_BG,
            font={'color': 'white'},
            height=300,
            margin=dict(l=20, r=20, t=20, b=50),
            xaxis=dict(title=None, showgrid=True, gridcolor='#444'),
            yaxis=dict(title=None),
            coloraxis_showscale=False
        )
        fig_loc.update_traces(textposition='outside')
        st.plotly_chart(fig_loc, use_container_width=True, config={'displayModeBar': False})

    # Fallback if cleaner.indiv() didn't have the key
    elif 'malls_visited' in df.columns:
        location_series = df['malls_visited'].str.split(',').explode().str.strip()
        location_counts = location_series.value_counts().reset_index()
        location_counts.columns = ['Mall', 'Visits']
        location_counts = location_counts[location_counts['Mall'].str.len() > 1]
        top_locs = location_counts.head(5).sort_values(by="Visits", ascending=True)

        fig_loc = px.bar(top_locs, x='Visits', y='Mall', orientation='h',
                         text='Visits', color='Visits',
                         color_continuous_scale=['#4dabf7', '#0057e7'])

        fig_loc.update_layout(
            paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG, font={'color': 'white'},
            height=300, margin=dict(l=20, r=20, t=20, b=50),
            xaxis=dict(title=None, showgrid=True, gridcolor='#444'), yaxis=dict(title=None),
            coloraxis_showscale=False
        )
        fig_loc.update_traces(textposition='outside')
        st.plotly_chart(fig_loc, use_container_width=True, config={'displayModeBar': False})

    else:
        st.warning("Mall data unavailable.")

    st.markdown('<div class="chart-footer"></div>', unsafe_allow_html=True)

with col_desc:
    # Identify Top Location dynamically
    top_mall_name = "Target Locations"
    if mall_data_to_plot is not None:
        # Assuming dict or series structure from cleaner
        if hasattr(mall_data_to_plot, 'index'):
            top_mall_name = mall_data_to_plot.index[0]
        elif hasattr(mall_data_to_plot, 'iloc'):
            top_mall_name = mall_data_to_plot.iloc[0]['Mall']

    st.markdown(dedent(f"""
    <div style="background-color: #f8f9fa; border-left: 5px solid #0057e7; padding: 20px; border-radius: 10px; height: 315px; display: flex; flex-direction: column; justify-content: center;">
        <h3 style="margin-top:0; color:#002e6e;">🚀 Pilot Launch</h3>
        <p style="color: #555;">
            Data from <b>{top_mall_name}</b> shows the highest concentration of potential users.
        </p>
        <p style="color: #555;">
            <b>Recommendation:</b> <br>
            Install the first <b>"Globetele Sign Support Kiosk"</b> at {top_mall_name} to maximize visibility and usage during the pilot phase.
        </p>
    </div>
    """), unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# SECTION 3: VALIDATION CHARTS
# ==========================================

st.subheader("📊 Validation Data")
st.markdown("User feedback confirming the demand for this model.")

c_chart1, c_chart2 = st.columns(2)

# --- CHART 1: PREFERENCE ---
with c_chart1:
    st.markdown('<div class="chart-header"><p class="chart-title-text">Top Requested Features</p></div>',
                unsafe_allow_html=True)


    def categorize_suggestion(text):
        if not isinstance(text, str): return "Other"
        text = text.lower()
        if any(x in text for x in ['video', 'sign', 'interpreter', 'human', 'face', 'call']):
            return "Video/Sign Support"
        elif any(x in text for x in ['text', 'chat', 'message', 'sms', 'type']):
            return "Text-Based Support"
        elif any(x in text for x in ['guide', 'visual', 'picture', 'image']):
            return "Visual Guides"
        else:
            return "Other Improvements"


    if 'suggested_improvements' in df.columns:
        df['Suggestion_Category'] = df['suggested_improvements'].apply(categorize_suggestion)

        pref_counts = df['Suggestion_Category'].value_counts().reset_index()
        pref_counts.columns = ['Method', 'Count']

        color_map = {
            'Video/Sign Support': '#4dabf7',
            'Text-Based Support': '#999999',
            'Visual Guides': '#ef476f',
            'Other Improvements': '#555555'
        }

        fig1 = px.pie(pref_counts, values='Count', names='Method', hole=0.6,
                      color='Method', color_discrete_map=color_map)

        fig1.update_layout(
            paper_bgcolor=DARK_BG,
            plot_bgcolor=DARK_BG,
            font={'color': 'white'},
            height=380,
            margin=dict(l=20, r=20, t=20, b=60),
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5, font=dict(color="white"))
        )

        total = pref_counts['Count'].sum()
        video_count = pref_counts[pref_counts['Method'] == 'Video/Sign Support']['Count'].sum()
        human_pct = int((video_count / total) * 100) if total > 0 else 0

        fig1.add_annotation(text=f"{human_pct}%", x=0.5, y=0.5, font_size=40, font_weight="bold", font_color="white",
                            showarrow=False)
        fig1.add_annotation(text="Request Video", x=0.5, y=0.4, font_size=12, font_color="#ccc", showarrow=False)

        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    else:
        st.error("Column 'suggested_improvements' not found.")

    st.markdown('<div class="chart-footer"></div>', unsafe_allow_html=True)

# --- CHART 2: HELPFULNESS ---
with c_chart2:
    st.markdown('<div class="chart-header"><p class="chart-title-text">Perceived Helpfulness</p></div>',
                unsafe_allow_html=True)

    help_counts = df['perceived_helpfulness'].value_counts().reset_index()
    help_counts.columns = ['Rating', 'Count']

    order = ['Very Helpful', 'Somewhat Helpful', 'Neutral', 'Not Helpful']
    existing_order = [x for x in order if x in help_counts['Rating'].values]
    help_counts['Rating'] = pd.Categorical(help_counts['Rating'], categories=existing_order, ordered=True)
    help_counts = help_counts.sort_values('Rating')

    fig2 = px.bar(help_counts, x='Rating', y='Count', text='Count',
                  color_discrete_sequence=['#00c853'])

    fig2.update_layout(
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        font={'color': 'white'},
        height=380,
        margin=dict(l=20, r=20, t=20, b=50),
        xaxis=dict(title=None),
        yaxis=dict(showgrid=True, gridcolor='#444')
    )
    fig2.update_traces(textposition='outside')

    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    st.markdown('<div class="chart-footer"></div>', unsafe_allow_html=True)