from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class QueryRequest(BaseModel):
    """Schema for a query request."""
    query_text: str
    username: str = "default_user"

class ResponseContent(BaseModel):
    """Schema for a response content."""
    text_content: str
    visualization_type: Optional[str] = None
    visualization_path: Optional[str] = None

class QueryResponse(BaseModel):
    """Schema for a query response."""
    query_id: int
    query_text: Optional[str] = None
    timestamp: Optional[datetime] = None
    response: ResponseContent

class StatusResponse(BaseModel):
    """Schema for the API status response."""
    message: str
    docs_url: str
    status: str

class ChatResponse(BaseModel):
    """Schema for a chat history response."""
    query: QueryResponse
    response: ResponseContent 