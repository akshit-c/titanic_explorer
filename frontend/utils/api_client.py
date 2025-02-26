import os
import httpx
from typing import Dict, Any, Optional
import json
import streamlit as st


class TitanicChatClient:
    """Client for interacting with the Titanic Chat API."""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the client.
        
        Args:
            base_url: The base URL of the API
        """
        # Get the base URL from environment variable or use default
        self.base_url = base_url or os.environ.get("BACKEND_API_URL", "http://localhost:8000")
        print(f"Initializing TitanicChatClient with base_url: {self.base_url}")
    
    def send_query(self, query_text: str, username: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a query to the API.
        
        Args:
            query_text: The query text
            username: The username
            
        Returns:
            The API response
        """
        # Construct the API endpoint URL
        url = f"{self.base_url}/api/query"
        print(f"Sending query to {url}")
        
        # Construct the request payload
        payload = {
            "query_text": query_text
        }
        
        # Add username if provided
        if username:
            payload["username"] = username
        
        # Send the request
        try:
            with httpx.Client(timeout=60.0) as client:
                print(f"Sending POST request to {url} with payload: {payload}")
                response = client.post(url, json=payload)
            
            # Check if the request was successful
            if response.status_code != 201:
                error_message = f"API request failed with status code {response.status_code}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_message = f"API error: {error_data['detail']}"
                except:
                    pass
                
                print(f"Error: {error_message}")
                print(f"Response content: {response.content}")
                raise Exception(error_message)
            
            # Parse the response
            return response.json()
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            st.error(f"Failed to connect to the backend server at {url}. Please check if the server is running.")
            raise
    
    def get_chat_history(self, username: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Get the chat history from the API.
        
        Args:
            username: The username
            limit: The maximum number of messages to retrieve
            
        Returns:
            The API response
        """
        # Construct the API endpoint URL
        url = f"{self.base_url}/api/history"
        print(f"Getting chat history from {url}")
        
        # Construct the query parameters
        params = {"limit": limit}
        
        # Add username if provided
        if username:
            params["username"] = username
        
        # Send the request
        try:
            with httpx.Client(timeout=30.0) as client:
                print(f"Sending GET request to {url} with params: {params}")
                response = client.get(url, params=params)
            
            # Check if the request was successful
            if response.status_code != 200:
                error_message = f"API request failed with status code {response.status_code}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_message = f"API error: {error_data['detail']}"
                except:
                    pass
                
                print(f"Error: {error_message}")
                print(f"Response content: {response.content}")
                raise Exception(error_message)
            
            # Parse the response
            return response.json()
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            st.error(f"Failed to connect to the backend server at {url}. Please check if the server is running.")
            raise
