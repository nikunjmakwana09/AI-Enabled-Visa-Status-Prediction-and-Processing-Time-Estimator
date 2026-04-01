import streamlit as st
import time

def run_ai_pipeline():

    progress = st.progress(0)

    status = st.empty()

    steps = [
        "✅ Validating Input",
        "🔧 Feature Engineering",
        "🧠  Running ML Model",
        "📊 Calculating Confidence",
        "📤 Preparing Output"
    ]

    for i, step in enumerate(steps):

        status.write(f"{step}...")
        progress.progress(int((i + 1) / len(steps) * 100))
        time.sleep(0.35)

    status.success("Prediction Ready")

    progress.empty()
