import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import textwrap
from navbar import create_header
try:
    from data_cleaning import DataCleaning
except ImportError:
    st.error("Could not find data_cleaning.py.")
    st.stop()

# --- 4. CALL THE HEADER ---
create_header()

# --- 1. SETUP ---
st.set_page_config(page_title="Globe User Profile", layout="wide")

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# --- 2. DATA LOADING & FILTERING ---
try:
    from data_cleaning import DataCleaning
except ImportError:
    st.error("Could not find data_cleaning.py.")
    st.stop()


@st.cache_data
def load_globe_data():
    csv_path = os.path.join(parent_dir, "Data1.csv")
    if not os.path.exists(csv_path):
        st.error(f"File not found: {csv_path}")
        st.stop()

    cleaner = DataCleaning(csv_path)
    df = cleaner.drop()

    # Filter for ONLY Globe Users
    yes_df = df[df['globe_user'].astype(str).str.lower() == 'yes'].copy()
    return yes_df


yes_df = load_globe_data()

if yes_df.empty:
    st.warning("No Globe user data found.")
    st.stop()

# --- 3. PAGE STYLING (DARK CONTAINER MODE) ---
DARK_BG = "#262730"

st.markdown(f"""
<style>
    .stApp {{ background-color: #ffffff; color: #333333; }}
    div.block-container {{ padding-top: 2rem !important; padding-bottom: 2rem !important; }}
    h1, h2, h3 {{ color: #002e6e; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }}

    /* KPI Cards */
    .kpi-card {{
        background-color: #f8f9fa;
        border-left: 5px solid #0057e7; /* Globe Blue */
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
    }}
    .kpi-title {{ font-size: 13px; color: #888; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }}
    .kpi-value {{ font-size: 32px; color: #333; font-weight: 800; margin-top: 5px; }}

    /* Chart Containers */
    .card-header {{
        background-color: {DARK_BG};
        padding: 15px 20px 10px 20px;
        border-radius: 15px 15px 0 0;
        border: none;
    }}
    .card-title {{ font-size: 16px; font-weight: 700; color: #ffffff; margin: 0; }}
    .card-footer {{
        background-color: {DARK_BG};
        height: 20px; 
        border-radius: 0 0 15px 15px;
        border: none;
        margin-bottom: 20px;
        margin-top: -30px; 
        position: relative;
        z-index: 1;
    }}
</style>
""", unsafe_allow_html=True)

st.title("Existing Customer Profile")
st.markdown("### Ecosystem Buy-In & Churn Risk of Current Globe Subscribers")
st.markdown("---")

# --- 4. TOP ROW: KPI CARDS ---
total_globe_users = len(yes_df)

# Calculate Store Visitors
visited_count = yes_df[yes_df['visited_store_bool'].astype(str).str.contains('Yes', case=False, na=False)].shape[0]
visited_pct = int((visited_count / total_globe_users) * 100) if total_globe_users > 0 else 0

# Calculate Friction (Challenges)
challenged_count = \
yes_df[yes_df['encountered_challenges_bool'].astype(str).str.contains('Yes', case=False, na=False)].shape[0]
challenged_pct = int((challenged_count / total_globe_users) * 100) if total_globe_users > 0 else 0

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Verified Globe Users</div><div class="kpi-value">{total_globe_users}</div></div>',
        unsafe_allow_html=True)
with c2:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Require Physical Store Visits</div><div class="kpi-value">{visited_pct}%</div></div>',
        unsafe_allow_html=True)
with c3:
    st.markdown(
        f'<div class="kpi-card" style="border-left-color: #d9534f;"><div class="kpi-title">Report In-Store Friction (Churn Risk)</div><div class="kpi-value" style="color:#d9534f;">{challenged_pct}%</div></div>',
        unsafe_allow_html=True)

# --- 5. MIDDLE ROW: GLOBE SERVICES BAR CHART ---
st.markdown('<div class="card-header"><p class="card-title">Top Globe Services Utilized (Ecosystem Buy-In)</p></div>',
            unsafe_allow_html=True)

if 'globe_services' in yes_df.columns:
    # Clean and explode the services column
    split_services = yes_df['globe_services'].str.split(r'\s*,\s*|\s*&\s*|\s*/\s*|\s+and\s+|\s+AND\s+', regex=True)
    ind_services = split_services.explode().str.strip().str.title()  # Title Case looks better on charts

    # Remove junk/empty
    ind_services = ind_services.replace('', pd.NA).dropna()
    junk = ['Data', 'Wifi At Home', 'Pldt Wifi']
    ind_services = ind_services[~ind_services.isin(junk)]

    service_counts = ind_services.value_counts().reset_index().head(6)
    service_counts.columns = ['Service', 'Count']
    service_counts = service_counts.sort_values(by="Count", ascending=True)  # Ascending for horizontal bar

    fig_services = px.bar(service_counts, x='Count', y='Service', orientation='h', text='Count',
                          color_discrete_sequence=['#0057e7'])

    fig_services.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG, font={'color': 'white'},
        height=350, margin=dict(l=20, r=20, t=10, b=30),
        xaxis=dict(showgrid=True, gridcolor='#444444', title=None),
        yaxis=dict(title=None)
    )
    fig_services.update_traces(textposition='outside')
    st.plotly_chart(fig_services, use_container_width=True, config={'displayModeBar': False})
else:
    st.warning("Globe Services data missing.")

st.markdown('<div class="card-footer"></div>', unsafe_allow_html=True)

# --- 6. BOTTOM ROW: REASONS FOR VISITING ---
st.markdown('<div class="card-header"><p class="card-title">Primary Reasons for Visiting Physical Stores</p></div>',
            unsafe_allow_html=True)

if 'visit_reasons' in yes_df.columns:
    # Clean and explode visit reasons
    split_reasons = yes_df['visit_reasons'].str.split(r',\s*', regex=True)
    ind_reasons = split_reasons.explode().str.strip().dropna()

    # Filter out empty strings or people who said "None"
    ind_reasons = ind_reasons[ind_reasons.str.lower() != 'none']
    ind_reasons = ind_reasons[ind_reasons != '']

    reason_counts = ind_reasons.value_counts().reset_index().head(5)
    reason_counts.columns = ['Reason', 'Count']


    # Wrap long text so it fits on the chart
    def custom_wrap(text):
        return "<br>".join(textwrap.wrap(text, width=20))


    reason_counts['Reason'] = reason_counts['Reason'].apply(custom_wrap)

    fig_reasons = px.bar(reason_counts, x='Reason', y='Count', text='Count', color_discrete_sequence=['#f0ad4e'])

    fig_reasons.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG, font={'color': 'white'},
        height=400, margin=dict(l=20, r=20, t=10, b=90),
        xaxis=dict(title=None, tickangle=0),
        yaxis=dict(title=None, showgrid=True, gridcolor='#444444')
    )
    fig_reasons.update_traces(textposition='outside', width=0.5)
    st.plotly_chart(fig_reasons, use_container_width=True, config={'displayModeBar': False})
else:
    st.warning("Visit Reasons data missing.")

st.markdown('<div class="card-footer"></div>', unsafe_allow_html=True)