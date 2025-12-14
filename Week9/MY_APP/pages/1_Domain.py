import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Domain Dashboard", layout="wide")
st.title("Multi-Domain Dashboard")

def load_data():
    try:
        cyber = pd.read_csv("DATA/cyber_incidents.csv")
    except:
        cyber = pd.DataFrame({
            'severity': ['High', 'Medium', 'Low', 'High', 'Medium'],
            'count': [12, 8, 3, 5, 7]
        })
    
    try:
        tickets = pd.read_csv("DATA/it_tickets.csv")
    except:
        tickets = pd.DataFrame({
            'priority': ['High', 'Medium', 'Low', 'High', 'Medium'],
            'status': ['Open', 'Closed', 'In Progress', 'Open', 'Closed']
        })
    
    try:
        datasets = pd.read_csv("DATA/datasets_metadata.csv")
    except:
        datasets = pd.DataFrame({
            'dataset': ['Sales', 'Logs', 'Metrics', 'Feedback'],
            'size_mb': [250.5, 120.3, 85.7, 45.2]
        })
    
    return cyber, tickets, datasets

cyber_df, tickets_df, datasets_df = load_data()

tab1, tab2, tab3, tab4 = st.tabs(["Charts", "Data Tables", "Metrics", "AI Assistant"])

with tab1:
    st.header("Data Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cybersecurity Incidents")
        severity_counts = cyber_df['severity'].value_counts()
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        ax1.bar(severity_counts.index, severity_counts.values, color=['red', 'orange', 'green'])
        ax1.set_xlabel('Severity Level')
        ax1.set_ylabel('Number of Incidents')
        ax1.set_title('Security Incidents by Severity')
        st.pyplot(fig1)
    
    with col2:
        st.subheader("IT Support Tickets")
        if 'priority' in tickets_df.columns:
            priority_counts = tickets_df['priority'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            ax2.pie(priority_counts.values, labels=priority_counts.index, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Tickets by Priority Level')
            st.pyplot(fig2)
    
    st.subheader("Dataset Storage Analysis")
    if not datasets_df.empty:
        if 'size' in datasets_df.columns and 'name' in datasets_df.columns:
            datasets_df.rename(columns={'name': 'dataset', 'size': 'size_mb'}, inplace=True)
            top_datasets = datasets_df.nlargest(10, 'size_mb')
            fig3, ax3 = plt.subplots(figsize=(12, 5))
            ax3.barh(top_datasets['dataset'], top_datasets['size_mb'])
            ax3.set_xlabel('Size (units)')
            ax3.set_ylabel('Dataset Name')
            ax3.set_title('Top 10 Largest Datasets')
            ax3.invert_yaxis()
            st.pyplot(fig3)

with tab2:
    st.header("Raw Data Tables")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cybersecurity Incidents")
        st.dataframe(cyber_df)
    with col2:
        st.subheader("IT Support Tickets")
        st.dataframe(tickets_df)
    st.subheader("Dataset Metadata")
    st.dataframe(datasets_df)

with tab3:
    st.header("Platform Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Incidents", len(cyber_df))
    with col2:
        high = len(cyber_df[cyber_df['severity'] == 'High']) if 'severity' in cyber_df.columns else 0
        st.metric("High Severity", high)
    with col3:
        open_tickets = len(tickets_df[tickets_df['status'] == 'Open']) if 'status' in tickets_df.columns else 0
        st.metric("Open Tickets", open_tickets)
    with col4:
        if 'size_mb' in datasets_df.columns:
            total = datasets_df['size_mb'].sum()
            st.metric("Total Data", f"{total:.1f} units")

with tab4:
    st.header("AI Assistant")
    
    from services.openai_service import ai_service
    
    domain = st.selectbox("Domain:", ["Cybersecurity", "Data Analytics", "IT Operations"])
    
    user_input = st.text_input(f"Ask about {domain}:")
    
    if user_input:
        response = ai_service.get_ai_response(user_input, domain)
        st.info(response)

st.markdown("---")
if st.button("Return to Home"):
    st.switch_page("Home.py")