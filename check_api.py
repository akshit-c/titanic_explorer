#!/usr/bin/env python3
"""
API Check Script

This script checks if the backend API is accessible.
"""

import requests
import sys

def check_api(url="http://localhost:8000/api/status"):
    """Check if the API is accessible."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"API is accessible! Response: {response.json()}")
            return True
        else:
            print(f"API returned status code {response.status_code}: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"Connection error: Could not connect to {url}")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = check_api()
    sys.exit(0 if success else 1) 