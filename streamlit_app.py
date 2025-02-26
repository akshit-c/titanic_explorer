"""
Streamlit App Entry Point for Deployment

This file serves as the entry point for Streamlit Cloud deployment.
It imports and runs the standalone version of the app.
"""

import os
import sys

# Add the frontend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "frontend"))

# Import and run the standalone app
from standalone import main

if __name__ == "__main__":
    main() 