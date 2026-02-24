import streamlit as st


def create_header():
    # We use a single markdown block to inject both the CSS and the HTML
    st.markdown("""
        <style>
            /* 1. Hide Streamlit's default top bar and hamburger menu */
            header[data-testid="stHeader"] {display: none;}
            [data-testid="collapsedControl"] {display: none;}
            section[data-testid="stSidebar"] {display: none;}

            /* 2. Push the main app content down so it doesn't overlap with our fixed navbar */
            .block-container {
                padding-top: 5rem !important;
            }

            /* 3. The Custom Fixed Navbar */
            .custom-navbar {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 60px;
                background-color: #563d7c; /* The exact Bootstrap purple */
                display: flex;
                align-items: center;
                padding: 0 40px;
                z-index: 999999;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }

            /* Title / Logo Area */
            .nav-brand {
                color: white !important;
                font-size: 20px;
                font-weight: 700;
                text-decoration: none !important;
                margin-right: auto; /* Pushes the links to the far right */
                font-family: 'Helvetica Neue', sans-serif;
            }

            /* Links Container */
            .nav-links {
                display: flex;
                gap: 30px;
            }

            /* Individual Links */
            .nav-link {
                color: rgba(255, 255, 255, 0.75) !important;
                text-decoration: none !important;
                font-size: 16px;
                font-weight: 500;
                font-family: 'Helvetica Neue', sans-serif;
                transition: color 0.2s ease;
            }

            /* Hover effect (turns text bright white) */
            .nav-link:hover {
                color: white !important;
            }
        </style>

        <div class="custom-navbar">
            <a class="nav-brand" href="/" target="_self">Statistical Dashboard</a>
            <div class="nav-links">
                <a class="nav-link" href="/" target="_self">Home</a>
                <a class="nav-link" href="Problem" target="_self">The Problem</a>
                <a class="nav-link" href="Solution" target="_self">The Solution</a>
                <a class="nav-link" href="Impact" target="_self">Impact</a>
                <a class="nav-link" href="GlobeUser" target="_self">Globe Users</a>
            </div>
        </div>
    """, unsafe_allow_html=True)