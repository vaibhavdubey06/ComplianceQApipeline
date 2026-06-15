import streamlit as st
import requests
import os

st.set_page_config(page_title="Compliance QA Demo", layout="centered")

st.title("Compliance QA Pipeline — Demo")

api_host = st.text_input("API URL", value=os.getenv("API_URL", "http://localhost:8000"))

video_url = st.text_input("YouTube video URL", "https://youtu.be/dT7S75eYhcQ")

if st.button("Run Audit"):
    if not video_url:
        st.error("Please enter a video URL")
    else:
        with st.spinner("Running audit — this may take a few minutes while Azure processes the video..."):
            try:
                resp = requests.post(f"{api_host}/audit", json={"video_url": video_url})
                resp.raise_for_status()
                data = resp.json()
                st.success("Audit complete")
                st.subheader("Final Report")
                st.json(data)
            except Exception as e:
                st.error(f"Audit request failed: {e}")
