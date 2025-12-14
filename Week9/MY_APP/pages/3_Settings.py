import streamlit as st

st.set_page_config(page_title="Settings", layout="wide")
st.title("Platform Settings")

st.subheader("Configuration Options")
col1, col2 = st.columns(2)
with col1:
    theme = st.selectbox("Theme", ["Light", "Dark"])
    chart_style = st.selectbox("Chart Style", ["Default", "Minimal"])
with col2:
    refresh_rate = st.slider("Refresh Rate (minutes)", 1, 60, 5)

if st.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache cleared")

st.markdown("### Platform Information")
st.info("Version: 1.0.0 | Last Updated: 2024-12-14")

if st.button("Return to Home"):
    st.switch_page("Home.py")