from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Passenger(Base):
    """Model for Titanic passenger data."""
    __tablename__ = "passengers"
    
    passenger_id = Column(Integer, primary_key=True, index=True)
    survived = Column(Integer)
    pclass = Column(Integer)
    name = Column(String(100))
    sex = Column(String(10))
    age = Column(Float)
    sibsp = Column(Integer)
    parch = Column(Integer)
    ticket = Column(String(50))
    fare = Column(Float)
    cabin = Column(String(20))
    embarked = Column(String(1))


class User(Base):
    """Model for user data."""
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    queries = relationship("Query", back_populates="user")


class Query(Base):
    """Model for user queries."""
    __tablename__ = "queries"
    
    query_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    query_text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="queries")
    response = relationship("Response", back_populates="query", uselist=False)


class Response(Base):
    """Model for query responses."""
    __tablename__ = "responses"
    
    response_id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.query_id"))
    text_content = Column(Text)
    visualization_type = Column(String(50), nullable=True)
    visualization_path = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    query = relationship("Query", back_populates="response")
