#!/usr/bin/env python3
"""
Database Initialization Script

This script initializes the database for the Titanic Dataset Chat Agent.
"""

import os
import sys

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.models import Base, User, Passenger
from app.db.session import engine, SessionLocal
import pandas as pd


def init_database():
    """Initialize the database."""
    print("Creating database tables...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a default user
    with SessionLocal() as session:
        # Check if the default user already exists
        user = session.query(User).filter(User.username == "default_user").first()
        
        if not user:
            print("Creating default user...")
            user = User(username="default_user")
            session.add(user)
            session.commit()
    
    print("Database tables created successfully.")


def load_passengers():
    """Load passenger data into the database."""
    # Check if the processed dataset exists
    processed_path = os.path.join("data", "processed", "titanic_clean.csv")
    
    if not os.path.exists(processed_path):
        print("Processed dataset not found. Please run preprocess_data.py first.")
        return False
    
    print(f"Loading passenger data from {processed_path}...")
    
    # Load the dataset
    df = pd.read_csv(processed_path)
    
    # Create passenger records
    with SessionLocal() as session:
        # Check if passengers already exist
        passenger_count = session.query(Passenger).count()
        
        if passenger_count > 0:
            print(f"Database already contains {passenger_count} passengers. Skipping import.")
            return True
        
        print("Importing passenger data...")
        
        # Convert DataFrame to list of dictionaries
        passengers = []
        for _, row in df.iterrows():
            passenger = Passenger(
                passenger_id=row.get('passengerid'),
                survived=bool(row.get('survived')),
                pclass=row.get('pclass'),
                name=row.get('name'),
                sex=row.get('sex'),
                age=row.get('age'),
                sibsp=row.get('sibsp'),
                parch=row.get('parch'),
                ticket=row.get('ticket'),
                fare=row.get('fare'),
                cabin=row.get('cabin'),
                embarked=row.get('embarked')
            )
            passengers.append(passenger)
        
        # Add all passengers to the database
        session.add_all(passengers)
        session.commit()
        
        print(f"Successfully imported {len(passengers)} passengers.")
    
    return True


def main():
    """Main function."""
    # Initialize the database
    init_database()
    
    # Load passenger data
    load_passengers()
    
    print("Database initialization completed successfully.")


if __name__ == "__main__":
    main() 