import streamlit as st
import os
from navbar import create_header

# --- 1. PAGE CONFIGURATION (MUST BE FIRST AND ONLY CALLED ONCE) ---
st.set_page_config(
    page_title="Project Inclusion | Globe Telecom",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CALL THE HEADER ---
create_header()

# --- 3. CSS STYLING (High-End Corporate) ---
st.markdown("""
<style>
    /* Global Settings */
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }

    /* Hide Streamlit Clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Typography - "Executive Report" Style */
    h1 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 900;
        color: #002e6e; /* Globe Navy */
        font-size: 3.8rem !important;
        line-height: 1.1 !important;
        margin-bottom: 25px;
        letter-spacing: -1.5px;
    }

    .subtitle {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 1.3rem;
        color: #555555;
        line-height: 1.5;
        margin-bottom: 40px;
        font-weight: 300;
    }

    /* The "Accent" Line */
    .accent-line {
        height: 6px;
        width: 100px;
        background: linear-gradient(90deg, #0057e7, #52a2ff); /* Globe Blue Gradient */
        margin-bottom: 30px;
        border-radius: 3px;
    }

    /* The Top Tag */
    .top-tag {
        font-size: 0.85rem;
        font-weight: 800;
        color: #0057e7;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 15px;
    }

    /* Modern "Pill" Button */
    .stButton button {
        background-color: #0057e7;
        color: white;
        border: none;
        padding: 16px 40px;
        font-size: 18px;
        border-radius: 50px;
        font-weight: 700;
        box-shadow: 0 10px 30px rgba(0, 87, 231, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #004ecf;
        transform: translateY(-4px);
        box-shadow: 0 15px 40px rgba(0, 87, 231, 0.5);
    }

    /* Hero Image Styling */
    .hero-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); /* Professional Deep Shadow */
        border: 1px solid #f0f0f0;
    }
    img {
        border-radius: 20px; /* Forces round corners on the image */
        display: block; /* Removes bottom whitespace */
    }
</style>
""", unsafe_allow_html=True)

# --- 4. LAYOUT ---

st.write("")
st.write("")

col_text, col_img = st.columns([1, 1])

with col_text:
    st.write("")
    st.write("")
    st.write("")

    # 1. The Tag
    st.markdown('<div class="top-tag">Globe Telecom • Service Strategy</div>', unsafe_allow_html=True)

    # 2. The Headline
    st.markdown('<h1>Bridging the<br>Communication Gap</h1>', unsafe_allow_html=True)

    # 3. The Line
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)

    # 4. The Subtitle
    st.markdown("""
    <div class="subtitle">
        A comprehensive business case for integrating Deaf talent to solve <br>
        critical service barriers and optimize workforce efficiency.
        <br><br>
        <strong>Core Insight:</strong> 71% of surveyed customers report critical service failures.
    </div>
    """, unsafe_allow_html=True)

    # 5. The Button
    st.write("")
    if st.button("Explore The Data →"):
        st.switch_page("pages/1_Problem.py")

with col_img:
    # --- THE HERO IMAGE (Live URL) ---
    image_url = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop"

    st.markdown(f"""
    <div class="hero-container">
        <img src="{image_url}" width="100%">
    </div>
    """, unsafe_allow_html=True)

# --- 5. FOOTER ---
st.markdown("""
<div style="position: fixed; bottom: 30px; left: 30px; color: #aaa; font-size: 11px; letter-spacing: 1px;">
    CONFIDENTIAL • INTERNAL USE ONLY • 2026
</div>
""", unsafe_allow_html=True)