import os
import sys
import argparse
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.routes import router as api_router
from app.core.config import settings
from app.db.session import engine, Base, get_db
from app.db.models import User
from app.db.crud import create_user, get_user_by_username
from app.data.loader import load_titanic_data

# Create the FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Create database tables
Base.metadata.create_all(bind=engine)

# Create data directories if they don't exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.VISUALIZATIONS_DIR, exist_ok=True)

# Initialize the database with a default user if it doesn't exist
def init_db():
    db = next(get_db())
    # Create a default user if it doesn't exist
    default_username = "default_user"
    user = get_user_by_username(db, default_username)
    if not user:
        create_user(db, default_username)
        print(f"Created default user: {default_username}")
    
    # Load the Titanic dataset
    load_titanic_data()
    print("Titanic dataset loaded successfully")

@app.on_event("startup")
async def startup_event():
    init_db()
    print(f"Application started. API available at http://{settings.API_HOST}:{settings.API_PORT}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the TailorTalk API server")
    parser.add_argument("--host", type=str, default=settings.API_HOST, help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=settings.API_PORT, help="Port to bind the server to")
    args = parser.parse_args()
    
    # Run the server
    # When running as a script directly, use the module name
    if os.path.basename(sys.argv[0]) == "main.py":
        uvicorn.run("app.main:app", host=args.host, port=args.port, reload=True)
    else:
        # When running as a module, use the current module
        uvicorn.run("app.main:app", host=args.host, port=args.port, reload=True) 