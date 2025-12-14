import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analytics", layout="wide")
st.title("Advanced Analytics")

try:
    df = pd.read_csv("DATA/cyber_incidents.csv")
except:
    df = pd.DataFrame({
        'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'count': [12, 8, 15]
    })

st.subheader("Incident Trend Analysis")
if 'date' in df.columns and 'count' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['date'], df['count'], marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Incidents')
    ax.set_title('Daily Incident Trends')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.subheader("Distribution Analysis")
col1, col2 = st.columns(2)
with col1:
    if 'count' in df.columns:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df['count'], bins=5, color='skyblue', edgecolor='black')
        ax.set_xlabel('Incident Count')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

st.subheader("Statistical Summary")
if not df.empty:
    stats = df.describe()
    st.dataframe(stats)

if st.button("Return to Home"):
    st.switch_page("Home.py")