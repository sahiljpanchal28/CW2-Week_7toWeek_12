# services/openai_service.py
import streamlit as st
from openai import OpenAI

class OpenAIService:
    def __init__(self):
        try:
            self.api_key = st.secrets.get("OPENAI_API_KEY")
            if not self.api_key:
                st.error("❌ OpenAI API key not found in secrets.toml")
                st.info("Add to .streamlit/secrets.toml: OPENAI_API_KEY = 'your-key-here'")
                st.stop()
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            st.error(f"OpenAI init error: {e}")
            self.client = None
    
    def get_domain_prompt(self, domain):
        prompts = {
            "Cybersecurity": "You are a cybersecurity expert. Provide threat analysis and security recommendations.",
            "Data Analytics": "You are a data science expert. Help with analysis, visualization, and statistics.",
            "IT Operations": "You are an IT operations expert. Help with troubleshooting and system management."
        }
        return prompts.get(domain, "You are a helpful assistant.")
    
    def chat_completion(self, messages, model="gpt-4o", stream=True):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream
            )
            return response
        except Exception as e:
            st.error(f"API Error: {e}")
            return None

ai_service = OpenAIService()