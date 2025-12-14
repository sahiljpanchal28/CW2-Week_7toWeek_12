import streamlit as st

st.set_page_config(page_title="AI Assistant", layout="wide")
st.title("AI Assistant")

from services.openai_service import ai_service

domain = st.selectbox("Select Domain:", ["Cybersecurity", "Data Analytics", "IT Operations"])

user_input = st.text_input(f"Ask about {domain}:")

if user_input:
    response = ai_service.get_ai_response(user_input, domain)
    st.markdown("---")
    st.markdown("**Response:**")
    st.success(response)

st.markdown("---")
if st.button("Return to Home"):
    st.switch_page("Home.py")