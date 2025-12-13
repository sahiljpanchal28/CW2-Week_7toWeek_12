import streamlit as st

st.set_page_config(page_title="Platform", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.session_state.domain = "security"

st.title("Multi-Domain Platform")
st.markdown("---")

def check_login(user, pwd):
    try:
        with open('DATA/users.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 2 and parts[0] == user and parts[1] == pwd:
                    return True
        return False
    except:
        return False

if not st.session_state.logged_in:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username and password:
                if check_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.success(f"Welcome {username}")
                    st.rerun()
                else:
                    st.error("Wrong username/password")
            else:
                st.warning("Enter both fields")
    
    with col2:
        st.subheader("Demo Info")
        st.write("Username: admin")
        st.write("Password: admin123")
        st.markdown("---")
        st.write("Three Domains:")
        st.write("1. Security")
        st.write("2. Data Science")
        st.write("3. IT Operations")

else:
    st.success(f"Welcome {st.session_state.user}")
    
    st.sidebar.header("Navigation")
    domain = st.sidebar.selectbox(
        "Choose Domain",
        ["Security", "Data Science", "IT Operations"]
    )
    st.session_state.domain = domain.lower().replace(" ", "_")
    
    if st.sidebar.button("Go to Dashboard"):
        st.switch_page("pages/dashboard.py")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.write(f"Selected: {domain} Dashboard")
    st.write("Click 'Go to Dashboard' to continue")

st.markdown("---")
st.header(" Week 10: AI Integration")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    ** New AI Features:**
    
    • Domain-specific AI Assistants
    • Streaming ChatGPT responses
    • Cybersecurity threat analysis
    • Data analytics guidance
    • IT operations troubleshooting
    """)

with col2:
    st.success("""
    ** How to Setup:**
    
    1. Get OpenAI API key
    2. Add to `.streamlit/secrets.toml`
    3. Run `pip install openai`
    4. Restart Streamlit app
    """)

# Navigation buttons
st.subheader("Try the AI Features:")
col1, col2 = st.columns(2)

with col1:
    if st.button("Go to Domain AI Assistant", use_container_width=True):
        st.switch_page("pages/1_Domain.py")

with col2:
    if st.button("Go to AI Distribution Center", use_container_width=True):
        st.switch_page("pages/4_AI_dist.py")