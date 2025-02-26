import os
import sys
from sqlalchemy.orm import Session

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine, Base, get_db
from app.db.models import User
from app.db.crud import create_user, get_user_by_username
from app.data.loader import load_titanic_data
from app.core.config import settings

def init_db():
    """Initialize the database with the necessary tables and a default user."""
    print("Creating database tables...")
    
    # Create data directories if they don't exist
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.VISUALIZATIONS_DIR, exist_ok=True)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
    
    # Create a default user
    db = next(get_db())
    default_username = "default_user"
    user = get_user_by_username(db, default_username)
    if not user:
        user = create_user(db, default_username)
        print(f"Created default user: {default_username}")
    else:
        print(f"Default user already exists: {default_username}")
    
    # Load the Titanic dataset
    print("Loading Titanic dataset...")
    load_titanic_data()
    
    print("Database initialization complete!")

if __name__ == "__main__":
    init_db() 