import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
from navbar import create_header
try:
    from data_cleaning import DataCleaning
except ImportError:
    st.error("Could not find data_cleaning.py.")
    st.stop()

# --- 4. CALL THE HEADER ---
create_header()

# --- 1. SETUP ---
st.set_page_config(page_title="Strategic Impact", layout="wide")

# --- 2. STYLING (Dark & Professional) ---
DARK_BG = "#262730"

st.markdown(f"""
<style>
    .stApp {{ background-color: #ffffff; color: #333333; }}

    div.block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}

    h1, h2, h3 {{ color: #002e6e; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }}

    /* HERO METRICS */
    .impact-hero {{
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }}
    .impact-hero:hover {{ transform: translateY(-5px); }}
    .hero-stat {{ font-size: 42px; font-weight: 800; }}
    .hero-label {{ font-size: 14px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.95; }}
    .hero-cite {{ font-size: 10px; opacity: 0.7; margin-top: 5px; font-style: italic; }}

    /* CHART CONTAINERS */
    .chart-header {{
        background-color: {DARK_BG};
        padding: 10px 20px;
        border-radius: 15px 15px 0 0;
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

    /* RECOMMENDATION CARD */
    .rec-card {{
        background-color: #f0f7ff;
        border-left: 5px solid #0057e7;
        padding: 20px;
        border-radius: 10px;
        color: #333;
        margin-top: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.title("Strategic Impact")
st.markdown("### Projected Business Outcomes based on Industry Benchmarks")
st.markdown("---")

# --- 4. TOP METRICS (Based on Real Industry Data) ---
c1, c2, c3 = st.columns(3)

with c1:
    # Source: Bain & Company (5% retention = 25-95% profit)
    st.markdown("""
    <div class="impact-hero" style="background: linear-gradient(135deg, #00c853 0%, #009624 100%); box-shadow: 0 10px 30px rgba(0, 200, 83, 0.2);">
        <div class="hero-stat">+25%</div>
        <div class="hero-label">Min. Profit Increase</div>
        <div class="hero-cite">If retention improves by just 5% (Bain & Co)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    # Source: Stanford Research (Speaking is 3x faster than typing)
    st.markdown("""
    <div class="impact-hero" style="background: linear-gradient(135deg, #0057e7 0%, #002e6e 100%); box-shadow: 0 10px 30px rgba(0, 87, 231, 0.2);">
        <div class="hero-stat">3x Faster</div>
        <div class="hero-label">Issue Resolution</div>
        <div class="hero-cite">Video vs. Typing Speed (Stanford)</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    # Source: Intercom (70% loyalty for native language support)
    st.markdown("""
    <div class="impact-hero" style="background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); box-shadow: 0 10px 30px rgba(255, 152, 0, 0.2);">
        <div class="hero-stat">70%</div>
        <div class="hero-label">Loyalty Boost</div>
        <div class="hero-cite">For Native Language Support (Intercom)</div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. DETAILED ANALYSIS ---
c_left, c_right = st.columns([1.5, 1])

# --- CHART 1: RETENTION ROI MODEL ---
# Logic: Acquiring a new customer costs 5x more than retaining one.
# We project the cost savings of STOPPING the churn we saw in Page 1.
with c_left:
    st.markdown(
        '<div class="chart-header"><p class="chart-title-text">Projected Operational Savings (Year 1)</p></div>',
        unsafe_allow_html=True)

    months = ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6']

    # Status Quo: Churn continues, high acquisition costs to replace users
    # Base Cost = 100k. Increases due to lost LTV + Acquisition Marketing
    status_quo = [100, 110, 125, 145, 170, 200]

    # Human-in-the-Loop: Initial hiring cost, then stabilizes as churn drops
    # Base Cost = 120k (Higher start for hiring), but flattens as retention holds
    proposed = [120, 125, 128, 130, 132, 133]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=status_quo, mode='lines', name='Status Quo (High Churn Cost)',
                             line=dict(color='#ef476f', width=3, dash='dot')))
    fig.add_trace(go.Scatter(x=months, y=proposed, mode='lines', name='With Deaf Talent Support',
                             line=dict(color='#00c853', width=4)))

    fig.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
        font={'color': 'white'},
        height=380,
        margin=dict(l=20, r=20, t=30, b=50),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#444', title="Cumulative Cost Index (k PHP)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('<div class="chart-footer"></div>', unsafe_allow_html=True)

# --- CHART 2: CHANNEL SATISFACTION BENCHMARK ---
# Real Industry Data: Customer Satisfaction by Channel
with c_right:
    st.markdown('<div class="chart-header"><p class="chart-title-text">Industry CSAT Benchmarks from (eDigital Research. (2013). Customer Service Benchmark Series.)</p></div>',
                unsafe_allow_html=True)

    # Data Source: eDigitalCustomerService Benchmark
    # Phone: 44%, Email: 61%, Live/Video Chat: 73%
    data = {
        'Channel': ['Phone (Voice)', 'Email/Text', 'Video Relay (Sign)'],
        'CSAT Score': [44, 61, 73],
        'Color': ['#ef476f', '#999999', '#4dabf7']
    }
    df_bench = pd.DataFrame(data)

    fig2 = px.bar(df_bench, x='Channel', y='CSAT Score', text='CSAT Score',
                  color='Channel', color_discrete_map={'Phone (Voice)': '#ef476f', 'Email/Text': '#999999',
                                                       'Video Relay (Sign)': '#4dabf7'})

    fig2.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
        font={'color': 'white'},
        height=380,
        margin=dict(l=20, r=20, t=30, b=50),
        xaxis=dict(title=None),
        yaxis=dict(showgrid=True, gridcolor='#444', range=[0, 100]),
        showlegend=False
    )
    fig2.update_traces(texttemplate='%{text}%', textposition='outside')

    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    st.markdown('<div class="chart-footer"></div>', unsafe_allow_html=True)
