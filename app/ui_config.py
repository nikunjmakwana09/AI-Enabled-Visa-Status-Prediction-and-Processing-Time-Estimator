import streamlit as st
from pathlib import Path


# ==========================================================
# Page Configuration
# ==========================================================

def configure_page():

    st.set_page_config(
        page_title="AI-Enabled Visa Status Prediction & Processing Time Estimator",
        page_icon="app/assets/logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.session_state.page_config_set = True


# ==========================================================
# CSS Loader
# ==========================================================

def load_css():

    css_path = Path("app/assets/style.css")

    if css_path.exists():

        st.markdown(
            f"<style>{css_path.read_text()}</style>", 
            unsafe_allow_html=True)

    else:

        st.warning("⚠ UI stylesheet missing: app/assets/style.css")
