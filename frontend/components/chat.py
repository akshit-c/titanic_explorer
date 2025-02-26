import streamlit as st
from typing import Optional

from frontend.components.visualizations import display_visualization


def display_chat_message(
    role: str,
    content: str,
    visualization_path: Optional[str] = None
) -> None:
    """
    Display a chat message with a modern, minimalistic design.
    
    Args:
        role: The role of the message sender (user or assistant)
        content: The message content
        visualization_path: The path to the visualization file
    """
    # Determine the avatar, background color, and alignment based on the role
    if role == "user":
        avatar = "👤"
        bg_color = "#f0f2f6"
        text_color = "#1e1e1e"
        border_radius = "18px 18px 0 18px"
        align = "flex-end"
        padding = "0 10px 0 60px"  # Less padding on left, more on right
    else:  # assistant
        avatar = "🚢"
        bg_color = "#2e7bf6"
        text_color = "white"
        border_radius = "18px 18px 18px 0"
        align = "flex-start"
        padding = "0 60px 0 10px"  # More padding on left, less on right
    
    # Create a container for the message with custom CSS
    st.markdown(
        f"""
        <div style='display: flex; flex-direction: column; align-items: {align}; margin-bottom: 15px; {padding};'>
            <div style='display: flex; align-items: center; margin-bottom: 5px;'>
                <div style='font-size: 14px; color: #555; margin-right: 5px;'>{role.capitalize()}</div>
            </div>
            <div style='background-color: {bg_color}; color: {text_color}; padding: 12px 16px; 
                 border-radius: {border_radius}; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                 line-height: 1.5;'>
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display the visualization if provided
    if visualization_path:
        with st.container():
            st.markdown(
                f"""
                <div style='display: flex; justify-content: {align}; padding: {padding};'>
                    <div style='background-color: #f8f9fa; border-radius: 12px; padding: 10px; 
                         max-width: 90%; box-shadow: 0 1px 2px rgba(0,0,0,0.05);'>
                """,
                unsafe_allow_html=True
            )
            display_visualization(visualization_path)
            st.markdown("</div></div>", unsafe_allow_html=True)


def display_chat_input(placeholder: str = "Ask a question about the Titanic dataset...") -> Optional[str]:
    """
    Display a modern chat input field.
    
    Args:
        placeholder: The placeholder text for the input field
        
    Returns:
        The user's input, or None if no input was provided
    """
    # Add some custom CSS to make the input field more modern
    st.markdown(
        """
        <style>
        .stTextInput > div > div > input {
            border-radius: 25px !important;
            padding: 12px 20px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
            border: 1px solid #e0e0e0 !important;
        }
        .stButton > button {
            border-radius: 50% !important;
            width: 45px !important;
            height: 45px !important;
            padding: 0 !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
            background-color: #2e7bf6 !important;
            color: white !important;
            border: none !important;
        }
        .stButton > button:hover {
            background-color: #1a56c7 !important;
            transform: translateY(-2px) !important;
            transition: all 0.2s ease !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Create a form for the chat input
    with st.form(key="chat_input_form", clear_on_submit=True):
        # Create a container for the input field and submit button
        col1, col2 = st.columns([6, 1])
        
        # Display the input field
        with col1:
            user_input = st.text_input(
                label="Message",
                placeholder=placeholder,
                label_visibility="collapsed"
            )
        
        # Display the submit button
        with col2:
            submit_button = st.form_submit_button(label="↑")
    
    # Return the user's input if the form was submitted
    if submit_button and user_input:
        return user_input
    
    return None
