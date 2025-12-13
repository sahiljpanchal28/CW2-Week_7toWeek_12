import streamlit as st
import pandas as pd

if not st.session_state.get('logged_in', False):
    st.error("Please login first")
    st.stop()

domain = st.session_state.get('domain', 'security')
domain_name = domain.replace('_', ' ').title()

st.set_page_config(page_title="Dashboard", layout="wide")
st.title(f"{domain_name} Dashboard")
st.markdown("---")

# Show different content based on domain
if domain == "security":
    st.subheader("Security Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Threats Today", "12")
    with col2:
        st.metric("Incidents", "3")
    with col3:
        st.metric("Response Time", "1.4h")
    
    # Load your Week 8 security data
    try:
        df = pd.read_csv('DATA/cyber_incidents.csv')
        st.subheader("Recent Incidents")
        st.dataframe(df.head(5))
    except:
        st.info("Sample security data would appear here")

elif domain == "data_science":
    st.subheader("Data Science Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Data Size", "28.4 GB")
    with col2:
        st.metric("Models", "8")
    with col3:
        st.metric("Accuracy", "94.2%")
    
    # Load your Week 8 data science data
    try:
        df = pd.read_csv('DATA/datasets_metadata.csv')
        st.subheader("Datasets")
        st.dataframe(df.head(5))
    except:
        st.info("Sample data science data would appear here")

else:  # IT Operations
    st.subheader("IT Operations Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CPU Usage", "67%")
    with col2:
        st.metric("Uptime", "99.8%")
    with col3:
        st.metric("Tickets", "15")
    
    # Load your Week 8 IT data
    try:
        df = pd.read_csv('DATA/it_tickets.csv')
        st.subheader("Recent Tickets")
        st.dataframe(df.head(5))
    except:
        st.info("Sample IT operations data would appear here")

# Simple chart
st.markdown("---")
st.subheader("Simple Chart")
data = pd.DataFrame({
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    'Value': [12, 19, 15, 8, 22]
})
st.bar_chart(data.set_index('Day'))

st.markdown("---")
st.write(f"User: {st.session_state.user} | Domain: {domain_name}")