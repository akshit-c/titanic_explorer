import os
import sys
import streamlit as st

# Initialize session state before importing the main app
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'username' not in st.session_state:
    st.session_state.username = "default_user"

if 'query_input' not in st.session_state:
    st.session_state.query_input = ""


sys.path.append(os.path.join(os.path.dirname(__file__), "frontend"))


from standalone import main

if __name__ == "__main__":
    main() 
