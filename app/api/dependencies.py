from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.crud import get_user, get_user_by_username
from app.db.models import User
from app.db.session import get_db


def get_current_user(
    username: str = "default_user",
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current user based on the username.
    If the username is not provided, use the default user.
    
    Args:
        username: The username of the user
        db: The database session
        
    Returns:
        The user object
        
    Raises:
        HTTPException: If the user is not found
    """
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
