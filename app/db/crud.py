from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models import Passenger, Query, Response, User


# User operations
def create_user(db: Session, username: str) -> User:
    """Create a new user."""
    db_user = User(username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()


def update_user_last_active(db: Session, user_id: int) -> Optional[User]:
    """Update a user's last active timestamp."""
    db_user = get_user(db, user_id)
    if db_user:
        db_user.last_active = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
    return db_user


# Query operations
def create_query(db: Session, user_id: int, query_text: str) -> Query:
    """Create a new query."""
    db_query = Query(user_id=user_id, query_text=query_text)
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


def get_query(db: Session, query_id: int) -> Optional[Query]:
    """Get a query by ID."""
    return db.query(Query).filter(Query.query_id == query_id).first()


def get_user_queries(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Query]:
    """Get all queries for a user."""
    return db.query(Query).filter(Query.user_id == user_id).order_by(Query.timestamp.desc()).offset(skip).limit(limit).all()


# Response operations
def create_response(
    db: Session, 
    query_id: int, 
    text_content: str, 
    visualization_type: Optional[str] = None,
    visualization_path: Optional[str] = None
) -> Response:
    """Create a new response."""
    db_response = Response(
        query_id=query_id,
        text_content=text_content,
        visualization_type=visualization_type,
        visualization_path=visualization_path
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def get_response(db: Session, response_id: int) -> Optional[Response]:
    """Get a response by ID."""
    return db.query(Response).filter(Response.response_id == response_id).first()


def get_response_by_query(db: Session, query_id: int) -> Optional[Response]:
    """Get a response by query ID."""
    return db.query(Response).filter(Response.query_id == query_id).first()


# Passenger operations
def get_all_passengers(db: Session, skip: int = 0, limit: int = 100) -> List[Passenger]:
    """Get all passengers."""
    return db.query(Passenger).offset(skip).limit(limit).all()


def get_passenger(db: Session, passenger_id: int) -> Optional[Passenger]:
    """Get a passenger by ID."""
    return db.query(Passenger).filter(Passenger.passenger_id == passenger_id).first()


def get_passengers_by_survival(db: Session, survived: bool) -> List[Passenger]:
    """Get passengers by survival status."""
    return db.query(Passenger).filter(Passenger.survived == survived).all()


def get_passengers_by_class(db: Session, pclass: int) -> List[Passenger]:
    """Get passengers by class."""
    return db.query(Passenger).filter(Passenger.pclass == pclass).all()


def get_passengers_by_sex(db: Session, sex: str) -> List[Passenger]:
    """Get passengers by sex."""
    return db.query(Passenger).filter(Passenger.sex == sex).all()


def get_passengers_by_embarked(db: Session, embarked: str) -> List[Passenger]:
    """Get passengers by port of embarkation."""
    return db.query(Passenger).filter(Passenger.embarked == embarked).all()
