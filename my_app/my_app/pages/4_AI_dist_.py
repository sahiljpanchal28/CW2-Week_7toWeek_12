# pages/4_AI_dist.py
import streamlit as st
from services.openai_service import ai_service

st.set_page_config(
    page_title="AI Distribution Center",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Distribution Center")
st.markdown("### Centralized AI Assistant Hub")

# Create columns for domain cards
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 🛡️ Cybersecurity AI")
        st.write("Threat analysis, security guidance, incident response")
        if st.button("Open Cybersecurity Chat", use_container_width=True):
            st.switch_page("pages/1_Domain.py")

with col2:
    with st.container(border=True):
        st.markdown("### 📊 Data Analytics AI")
        st.write("Data analysis, visualization, statistical insights")
        if st.button("Open Data Analytics Chat", use_container_width=True):
            st.switch_page("pages/1_Domain.py")

with col3:
    with st.container(border=True):
        st.markdown("### ⚙️ IT Operations AI")
        st.write("Troubleshooting, system management, automation")
        if st.button("Open IT Operations Chat", use_container_width=True):
            st.switch_page("pages/1_Domain.py")

st.divider()

# Quick Chat
st.subheader("Quick Chat")
quick_domain = st.selectbox(
    "Select expertise:",
    ["General", "Cybersecurity", "Data Analytics", "IT Operations"]
)

# Initialize chat
if "quick_chat" not in st.session_state:
    st.session_state.quick_chat = []

# Display chat
for msg in st.session_state.quick_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask a question...")

if user_input:
    # Add user message
    st.session_state.quick_chat.append({"role": "user", "content": user_input})
    
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Prepare messages
        messages = [{"role": "user", "content": user_input}]
        if quick_domain != "General":
            system_msg = ai_service.get_domain_prompt(quick_domain)
            messages.insert(0, {"role": "system", "content": system_msg})
        
        # Get streaming response
        response = ai_service.chat_completion(messages)
        
        if response:
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Save to history
            st.session_state.quick_chat.append({"role": "assistant", "content": full_response})

# Clear button
with st.sidebar:
    if st.button("Clear Quick Chat", type="secondary"):
        st.session_state.quick_chat = []
        st.rerun()