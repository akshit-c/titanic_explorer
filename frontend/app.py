import os
import sys
import requests
import streamlit as st
import time
import json

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

# Configure the page
st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API URL
BACKEND_URL = os.environ.get("BACKEND_URL", f"http://localhost:{settings.API_PORT}")
API_URL = f"{BACKEND_URL}/api"

# Custom CSS for Gemini-like appearance
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        font-family: 'Google Sans', Arial, sans-serif;
    }
    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 24px;
        border: 1px solid #dadce0;
        padding: 12px 16px;
        font-size: 16px;
    }
    .stButton > button {
        background-color: #8ab4f8;
        color: #202124;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 24px;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #aecbfa;
    }
    .user-message {
        background-color: #e8f0fe;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 16px;
        color: #202124;
    }
    .bot-message {
        background-color: white;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 16px;
        border: 1px solid #dadce0;
        color: #202124;
    }
    h1, h2, h3 {
        color: #202124;
        font-family: 'Google Sans', Arial, sans-serif;
    }
    .stSpinner > div > div {
        border-color: #8ab4f8 !important;
    }
    .css-18e3th9 {
        padding-top: 2rem;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'username' not in st.session_state:
    st.session_state.username = "default_user"

if 'query_input' not in st.session_state:
    st.session_state.query_input = ""

def check_api_status():
    """Check if the API is accessible."""
    try:
        response = requests.get(f"{API_URL}/status")
        return response.status_code == 200
    except:
        return False

def send_query(query_text):
    """Send a query to the API and return the response."""
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"query_text": query_text, "username": st.session_state.username}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def display_message(message, is_user=False):
    """Display a message in the chat interface."""
    if is_user:
        st.markdown(f'<div class="user-message"><strong>You:</strong> {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message"><strong>Bot:</strong> {message}</div>', unsafe_allow_html=True)

def main():
    """Main function for the Streamlit app."""
    # Sidebar
    with st.sidebar:
        st.title("Titanic Dataset AI")
        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "This AI assistant can answer questions about the Titanic dataset. "
            "Ask questions about survival rates, passenger demographics, and more!"
        )
        st.markdown("---")
        st.markdown("### Sample Questions")
        st.markdown("- What was the overall survival rate?")
        st.markdown("- How did passenger class affect survival?")
        st.markdown("- What was the age distribution of passengers?")
        st.markdown("- How did gender affect survival rates?")
        st.markdown("- What was the relationship between ticket price and survival?")
        st.markdown("- Did the port of embarkation affect survival rates?")
        
        # API Status
        st.markdown("---")
        api_status = check_api_status()
        if api_status:
            st.success("API Status: Connected")
        else:
            st.error("API Status: Disconnected")
    
    # Main content
    st.title("Titanic Dataset Explorer")
    st.markdown("Ask questions about the Titanic dataset and get AI-powered insights with visualizations.")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            display_message(message['text'], message['is_user'])
            if 'visualization_url' in message and message['visualization_url']:
                st.image(message['visualization_url'], use_column_width=True)
    
    # Create a form for the input field and submit button
    with st.form(key="query_form", clear_on_submit=True):
        # Query input
        query_text = st.text_input(
            "Ask a question about the Titanic dataset:", 
            key="query_input", 
            placeholder="Type your question here..."
        )
        
        # Send button
        send_button = st.form_submit_button("Send")
    
    if send_button and query_text:
        # Add user message to chat
        st.session_state.messages.append({
            'text': query_text,
            'is_user': True
        })
        
        # Display user message
        with chat_container:
            display_message(query_text, is_user=True)
        
        # Show spinner while waiting for response
        with st.spinner("Thinking..."):
            # Send query to API
            response = send_query(query_text)
            
            if response:
                # Process response
                text_content = response.get('response', {}).get('text_content', 'No response text available.')
                visualization_path = response.get('response', {}).get('visualization_path')
                
                # Add bot message to chat
                message_data = {
                    'text': text_content,
                    'is_user': False
                }
                
                if visualization_path:
                    # Convert local path to URL if needed
                    if visualization_path.startswith('./'):
                        visualization_path = visualization_path[2:]
                    visualization_url = f"{API_URL}/{visualization_path}"
                    message_data['visualization_url'] = visualization_url
                
                st.session_state.messages.append(message_data)
                
                # Display bot message
                with chat_container:
                    display_message(text_content)
                    if 'visualization_url' in message_data:
                        st.image(message_data['visualization_url'], use_column_width=True)
            else:
                # Add error message to chat
                error_message = "Sorry, I couldn't process your query. Please try again."
                st.session_state.messages.append({
                    'text': error_message,
                    'is_user': False
                })
                
                # Display error message
                with chat_container:
                    display_message(error_message)

if __name__ == "__main__":
    main()
