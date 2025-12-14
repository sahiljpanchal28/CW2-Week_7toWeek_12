import streamlit as st
import sqlite3
import hashlib

# Initialize database
def init_db():
    conn = sqlite3.connect('DATA/intelligence_platform.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create user
def create_user(username, password):
    conn = sqlite3.connect('DATA/intelligence_platform.db')
    cursor = conn.cursor()
    password_hash = hash_password(password)
    
    try:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                      (username, password_hash))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# Verify user
def verify_user(username, password):
    conn = sqlite3.connect('DATA/intelligence_platform.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0] == hash_password(password)
    return False

# Initialize
init_db()

# Page config
st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    layout="wide"
)

# Check login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login/Register interface
if not st.session_state.logged_in:
    st.title("Multi-Domain Platform Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        
        if st.button("Create Account"):
            if new_pass != confirm_pass:
                st.error("Passwords don't match")
            elif create_user(new_user, new_pass):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists")

# Main dashboard (only shown when logged in)
else:
    st.title("Multi-Domain Intelligence Platform")
    st.markdown(f"### Welcome, {st.session_state.username}")
    st.write("Navigate to different sections using the buttons below.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Dashboard", use_container_width=True):
            st.switch_page("pages/1_Domain.py")
    
    with col2:
        if st.button("Analytics", use_container_width=True):
            st.switch_page("pages/2_Analytics.py")
    
    with col3:
        if st.button("Settings", use_container_width=True):
            st.switch_page("pages/3_Settings.py")
    
    with col4:
        if st.button("AI Assistant", use_container_width=True):
            st.switch_page("pages/4_AI_dist.py")
    
    # Show platform status
    st.markdown("---")
    st.subheader("Platform Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.info("Cybersecurity: Active incidents")
    
    with status_col2:
        st.success("Data Analytics: Datasets loaded")
    
    with status_col3:
        st.warning("IT Operations: Open tickets")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("Multi-Domain Intelligence Platform - CST1510 Week 10 Lab")