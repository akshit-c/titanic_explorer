import os
import streamlit as st
import base64
from typing import Optional


def display_visualization(filepath: Optional[str]) -> None:
    """
    Display a visualization.
    
    Args:
        filepath: The path to the visualization file
    """
    if not filepath:
        return
    
    # Check if the file exists
    if not os.path.exists(filepath):
        st.warning(f"Visualization file not found: {filepath}")
        return
    
    # Get the file extension
    _, ext = os.path.splitext(filepath)
    
    # Determine the MIME type
    mime_type = "image/png"
    if ext.lower() == ".jpg" or ext.lower() == ".jpeg":
        mime_type = "image/jpeg"
    elif ext.lower() == ".svg":
        mime_type = "image/svg+xml"
    
    # Read the file as binary
    with open(filepath, "rb") as f:
        image_data = f.read()
    
    # Encode the image as base64
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    
    # Create the data URI
    data_uri = f"data:{mime_type};base64,{encoded_image}"
    
    # Display the image
    st.image(data_uri, use_column_width=True)


def display_visualization_gallery(filepaths: list[str]) -> None:
    """
    Display a gallery of visualizations.
    
    Args:
        filepaths: A list of paths to visualization files
    """
    if not filepaths:
        return
    
    # Determine the number of columns based on the number of visualizations
    num_cols = min(3, len(filepaths))
    
    # Create columns
    cols = st.columns(num_cols)
    
    # Display each visualization in a column
    for i, filepath in enumerate(filepaths):
        with cols[i % num_cols]:
            display_visualization(filepath)


def display_visualization_with_caption(
    filepath: Optional[str],
    caption: Optional[str] = None
) -> None:
    """
    Display a visualization with a caption.
    
    Args:
        filepath: The path to the visualization file
        caption: The caption for the visualization
    """
    if not filepath:
        return
    
    # Create a container for the visualization and caption
    with st.container():
        # Display the visualization
        display_visualization(filepath)
        
        # Display the caption if provided
        if caption:
            st.caption(caption)


def display_visualization_comparison(
    filepaths: list[str],
    titles: Optional[list[str]] = None
) -> None:
    """
    Display a comparison of visualizations.
    
    Args:
        filepaths: A list of paths to visualization files
        titles: A list of titles for the visualizations
    """
    if not filepaths:
        return
    
    # Create columns
    col1, col2 = st.columns(2)
    
    # Display the first visualization
    with col1:
        if titles and len(titles) > 0:
            st.subheader(titles[0])
        display_visualization(filepaths[0])
    
    # Display the second visualization if provided
    if len(filepaths) > 1:
        with col2:
            if titles and len(titles) > 1:
                st.subheader(titles[1])
            display_visualization(filepaths[1])
    
    # Display additional visualizations if provided
    if len(filepaths) > 2:
        for i in range(2, len(filepaths)):
            if titles and len(titles) > i:
                st.subheader(titles[i])
            display_visualization(filepaths[i])
