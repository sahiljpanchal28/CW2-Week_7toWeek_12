# utils/ai_helper.py
import streamlit as st

class AIHelper:
    @staticmethod
    def init_chat(domain):
        key = f"chat_{domain}"
        if key not in st.session_state:
            st.session_state[key] = []
        return st.session_state[key]
    
    @staticmethod
    def display_messages(messages):
        for msg in messages:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])