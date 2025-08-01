import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Set page config
st.set_page_config(
    page_title="Login - YapYard",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Authentication function
def validate_groq_api_key(api_key):
    # Basic validation: check length and prefix
    # Groq API keys typically start with 'gsk_'
    if not api_key.startswith('gsk_') or len(api_key) < 40: # Groq keys are usually longer than 40 chars
        return False
    return True

def check_credentials(username, password, api_key):
    try:
        default_username = os.getenv('DEFAULT_USERNAME')
        default_password = os.getenv('DEFAULT_PASSWORD')
        
        if not default_username or not default_password:
            st.error("❌ Authentication credentials not properly configured. Please check .env file.")
            return False

        if not validate_groq_api_key(api_key):
            st.error("❌ Invalid GROQ API Key format. Please ensure it starts with 'gsk_' and is of correct length.")
            return False
            
        return username == default_username and password == default_password 
    except Exception as e:
        st.error(f"❌ Authentication error: {str(e)}")
        return False

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0

# Redirect if already authenticated
if st.session_state.authenticated:
    st.switch_page("app.py")

# Login page styling
st.markdown("""
<style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: black;
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .stButton > button {
        width: 100%;
        background-color: #3498db;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
</style>
""", unsafe_allow_html=True)

# Main login interface
st.markdown("<div class='login-container'>", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='login-header'>
    <h1>🗣️ YapYard</h1>
    <p>Please login to access </p>
</div>
""", unsafe_allow_html=True)

# Login form
with st.form("login_form", clear_on_submit=True):
    st.markdown("### 🔐 Login Credentials")
    
    username = st.text_input(
        "👤 Username",
        placeholder="Enter your username",
        help="Enter the username provided by your administrator"
    )
    
    password = st.text_input(
        "🔒 Password", 
        type="password",
        placeholder="Enter your password",
        help="Enter the password provided by your administrator"
    )

    api_key = st.text_input(
        "🔑 GROQ API KEY",
        type="password",
        placeholder="Enter your GROQ API Key",
        help="Enter your GROQ API Key from console.groq.com/keys"
    )

    st.markdown("### Note")
    st.markdown("""
    <div class='security-note'>
        <p>Your GROQ API Key is used to authenticate your requests. Do not share it with others.</p>
        <p>For security reasons, your API Key will not be stored in the database. It will be used only for the current session.</p>
        <p>Enter your GROQ API Key from <a href="https://console.groq.com/keys" target="_blank">console.groq.com/keys</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_button = st.form_submit_button("🚀 Login", use_container_width=True)
    
    # Handle login
    if login_button:
        if not username or not password or not api_key:
            st.error("⚠️ Please enter username, password, and API Key")
        else:
            if check_credentials(username, password, api_key):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.groq_api_key = api_key # Store the API key in session state
                st.session_state.login_attempts = 0
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.session_state.login_attempts += 1
                if st.session_state.login_attempts >= 3:
                    st.error("🚫 Too many failed login attempts. Please contact your administrator.")
                    st.stop()
                else:
                    remaining_attempts = 3 - st.session_state.login_attempts
                    st.error(f"❌ Invalid username, password, or API Key. {remaining_attempts} attempts remaining.")

st.markdown("</div>", unsafe_allow_html=True)

# Information section