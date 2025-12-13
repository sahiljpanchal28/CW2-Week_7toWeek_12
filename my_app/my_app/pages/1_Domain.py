# pages/1_Domain.py
import streamlit as st
from services.openai_service import ai_service
from utils.ai_helper import AIHelper

st.set_page_config(page_title="Domain Intelligence", layout="wide")
st.title("🌐 Domain Intelligence Dashboard")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🤖 AI Assistant", 
    "🛡️ Cybersecurity", 
    "📊 Data Analytics", 
    "⚙️ IT Operations"
])

# ===== TAB 1: AI Assistant =====
with tab1:
    st.header("Multi-Domain AI Assistant")
    
    # Domain selection
    domain = st.selectbox(
        "Select Domain Expertise:",
        ["Cybersecurity", "Data Analytics", "IT Operations"]
    )
    
    # Initialize chat
    chat_history = AIHelper.init_chat(domain)
    
    # Add system prompt if first time
    if not chat_history:
        system_prompt = ai_service.get_domain_prompt(domain)
        chat_history.append({"role": "system", "content": system_prompt})
    
    # Display chat history
    AIHelper.display_messages(chat_history)
    
    # Chat input
    prompt = st.chat_input(f"Ask about {domain}...")
    
    if prompt:
        # Add user message to history
        chat_history.append({"role": "user", "content": prompt})
        
        # Show user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Get streaming response
            response = ai_service.chat_completion(chat_history)
            
            if response:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        chunk_text = chunk.choices[0].delta.content
                        full_response += chunk_text
                        message_placeholder.markdown(full_response + "▌")
                
                # Show final response
                message_placeholder.markdown(full_response)
                
                # Save to history
                chat_history.append({"role": "assistant", "content": full_response})
    
    # Clear button
    if st.button("🗑️ Clear Chat", type="secondary"):
        chat_history.clear()
        st.rerun()

# ===== TAB 2: Cybersecurity (Keep your existing code) =====
with tab2:
    st.header("Cybersecurity Dashboard")
    st.write("Your cybersecurity content here...")
    # Keep your existing Week 9 code

# ===== TAB 3: Data Analytics (Keep your existing code) =====
with tab3:
    st.header("Data Analytics")
    st.write("Your data analytics content here...")
    # Keep your existing Week 9 code

# ===== TAB 4: IT Operations (Keep your existing code) =====
with tab4:
    st.header("IT Operations")
    st.write("Your IT operations content here...")
    # Keep your existing Week 9 code