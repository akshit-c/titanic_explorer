import base64
import os
from typing import Dict, Any, Optional


def format_visualization_for_api(filepath: str) -> Dict[str, Any]:
    """
    Format a visualization for API response.
    
    Args:
        filepath: The path to the visualization file
        
    Returns:
        A dictionary containing the visualization data
    """
    # Check if the file exists
    if not os.path.exists(filepath):
        return {
            "error": f"Visualization file not found at {filepath}"
        }
    
    # Get the file extension
    _, ext = os.path.splitext(filepath)
    
    # Read the file as binary
    with open(filepath, "rb") as f:
        image_data = f.read()
    
    # Encode the image as base64
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    
    # Determine the MIME type
    mime_type = "image/png"
    if ext.lower() == ".jpg" or ext.lower() == ".jpeg":
        mime_type = "image/jpeg"
    elif ext.lower() == ".svg":
        mime_type = "image/svg+xml"
    
    # Create the data URI
    data_uri = f"data:{mime_type};base64,{encoded_image}"
    
    return {
        "data_uri": data_uri,
        "mime_type": mime_type,
        "filename": os.path.basename(filepath)
    }


def format_visualization_for_streamlit(filepath: str) -> str:
    """
    Format a visualization for Streamlit display.
    
    Args:
        filepath: The path to the visualization file
        
    Returns:
        The HTML code to display the visualization in Streamlit
    """
    # Check if the file exists
    if not os.path.exists(filepath):
        return f"<p>Visualization file not found at {filepath}</p>"
    
    # Get the file extension
    _, ext = os.path.splitext(filepath)
    
    # Read the file as binary
    with open(filepath, "rb") as f:
        image_data = f.read()
    
    # Encode the image as base64
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    
    # Determine the MIME type
    mime_type = "image/png"
    if ext.lower() == ".jpg" or ext.lower() == ".jpeg":
        mime_type = "image/jpeg"
    elif ext.lower() == ".svg":
        mime_type = "image/svg+xml"
    
    # Create the HTML
    html = f'<img src="data:{mime_type};base64,{encoded_image}" alt="Visualization" style="width:100%;">'
    
    return html


def format_text_response(text: str, visualization_type: Optional[str] = None) -> str:
    """
    Format a text response for display.
    
    Args:
        text: The text response
        visualization_type: The type of visualization
        
    Returns:
        The formatted text response
    """
    # Split the text into paragraphs
    paragraphs = text.split("\n\n")
    
    # Format each paragraph
    formatted_paragraphs = []
    for paragraph in paragraphs:
        if paragraph.strip():
            formatted_paragraphs.append(f"<p>{paragraph}</p>")
    
    # Join the formatted paragraphs
    formatted_text = "\n".join(formatted_paragraphs)
    
    # Add a note about the visualization if provided
    if visualization_type:
        formatted_text += f"\n<p><em>A {visualization_type} chart has been generated to illustrate this data.</em></p>"
    
    return formatted_text
