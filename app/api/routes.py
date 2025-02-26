from datetime import datetime
from typing import List, Optional, Dict, Any
import os
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.crud import (
    create_query, create_response, get_query, get_response_by_query,
    get_user_queries, update_user_last_active, create_user, get_user_by_username
)
from app.db.models import User, Query, Response
from app.db.session import get_db
from app.nlp.chain import process_query
from app.core.config import settings
from app.api.schemas import QueryRequest, QueryResponse, StatusResponse, ResponseContent, ChatResponse

router = APIRouter()


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """Check if the API is running."""
    return {
        "message": "Welcome to the Titanic Dataset Chat Agent API",
        "docs_url": "/docs",
        "status": "operational"
    }


@router.get("/data/visualizations/{filename}")
async def get_visualization(filename: str):
    """
    Serve a visualization file.
    
    Args:
        filename: The name of the visualization file
        
    Returns:
        The visualization file
    """
    # Construct the file path
    filepath = os.path.join(settings.VISUALIZATIONS_DIR, filename)
    
    # Check if the file exists
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Visualization file not found: {filename}"
        )
    
    # Return the file
    return FileResponse(
        filepath,
        media_type="image/png",
        filename=filename
    )


@router.post("/query", response_model=QueryResponse)
async def create_chat_query(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Process a natural language query about the Titanic dataset.
    
    Args:
        request: The query request containing the query text and username
        db: The database session
        
    Returns:
        The query response containing the generated text and visualization
    """
    # Get or create user
    username = request.username
    user = get_user_by_username(db, username)
    if not user:
        user = create_user(db, username)
    
    # Create query record
    query = create_query(db, user.user_id, request.query_text)
    
    # Process the query using our rule-based chatbot
    try:
        result = process_query(request.query_text)
        
        # Create response record
        response = create_response(
            db,
            query.query_id,
            result["text_content"],
            result.get("visualization_type"),
            result.get("visualization_path")
        )
        
        return {
            "query_id": query.query_id,
            "query_text": query.query_text,
            "timestamp": query.timestamp,
            "response": ResponseContent(
                text_content=result["text_content"],
                visualization_type=result.get("visualization_type"),
                visualization_path=result.get("visualization_path")
            )
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/history", response_model=List[ChatResponse])
async def get_chat_history(
    skip: int = 0,
    limit: int = 10,
    username: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Get the chat history for the specified user.
    """
    # Get user by username
    user = get_user_by_username(db, username)
    if not user:
        user = create_user(db, username)
    
    # Update user's last active timestamp
    update_user_last_active(db, user.user_id)
    
    # Get user's queries
    queries = get_user_queries(db, user.user_id, skip, limit)
    
    # Build response with queries and their responses
    chat_history = []
    for query in queries:
        response = get_response_by_query(db, query.query_id)
        if response:
            chat_history.append(ChatResponse(
                query=QueryResponse(
                    query_id=query.query_id,
                    query_text=query.query_text,
                    timestamp=query.timestamp
                ),
                response=ResponseContent(
                    text_content=response.text_content,
                    visualization_type=response.visualization_type,
                    visualization_path=response.visualization_path
                )
            ))
    
    return chat_history
