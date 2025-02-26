"""
Streamlit Cloud Entry Point

This file serves as the entry point for Streamlit Cloud deployment.
It simply imports and runs the main frontend app.
"""

import os
import sys

# Add the frontend directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend')))

# Import and run the main app
from app import main

if __name__ == "__main__":
    main() 