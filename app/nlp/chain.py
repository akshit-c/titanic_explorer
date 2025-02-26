import os
import json
import logging
from typing import Dict, Any

from app.nlp.chatbot import TitanicChatbot

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the chatbot
chatbot = TitanicChatbot()

def process_query(query_text: str) -> Dict[str, Any]:
    """
    Process a natural language query about the Titanic dataset.
    
    Args:
        query_text: The user's query text
        
    Returns:
        A dictionary containing:
        - text_content: The text response
        - visualization_type: The type of visualization generated
        - visualization_path: The path to the visualization file
    """
    logger.info(f"Processing query: {query_text}")
    
    try:
        # Use our rule-based chatbot to process the query
        response = chatbot.process_query(query_text)
        
        logger.info(f"Generated response for query: {query_text}")
        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return {
            "text_content": "I'm sorry, I encountered an error while processing your query. Please try again.",
            "visualization_type": None,
            "visualization_path": None
        }
