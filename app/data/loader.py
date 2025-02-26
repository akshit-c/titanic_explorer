import os
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from app.core.config import settings

def load_titanic_data():
    """
    Load the Titanic dataset from the CSV file and store it in the database.
    
    Returns:
        The Titanic dataset as a pandas DataFrame
    """
    # Create data directory if it doesn't exist
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    
    # Path to the Titanic dataset
    csv_path = os.path.join(settings.DATA_DIR, "titanic.csv")
    
    # Check if the dataset exists
    if not os.path.exists(csv_path):
        # Use the local file in the app/data directory
        local_csv_path = os.path.join("app", "data", "titanic.csv")
        if os.path.exists(local_csv_path):
            print(f"Using local Titanic dataset from {local_csv_path}...")
            df = pd.read_csv(local_csv_path)
            
            # Save the dataset to the data directory
            df.to_csv(csv_path, index=False)
            print(f"Titanic dataset saved to {csv_path}")
        else:
            print(f"Error: Could not find Titanic dataset at {local_csv_path}")
            return None
    else:
        # Load the dataset from the CSV file
        df = pd.read_csv(csv_path)
        print(f"Titanic dataset loaded from {csv_path}")
    
    # Connect to the database
    engine = create_engine(settings.DATABASE_URL)
    
    # Store the dataset in the database
    df.to_sql("passengers", engine, if_exists="replace", index=False)
    print("Titanic dataset stored in the database")
    
    return df

if __name__ == "__main__":
    # Load the Titanic dataset
    df = load_titanic_data()
    
    if df is not None:
        # Print the first 5 rows
        print(df.head())
        
        # Print the shape of the dataset
        print(f"Dataset shape: {df.shape}")
        
        # Print the column names
        print(f"Column names: {df.columns.tolist()}")
        
        # Print the data types
        print(f"Data types:\n{df.dtypes}")
        
        # Print the number of missing values
        print(f"Missing values:\n{df.isnull().sum()}")
        
        # Print the number of unique values for categorical columns
        for col in ["Survived", "Pclass", "Sex", "Embarked"]:
            print(f"Unique values for {col}: {df[col].unique()}")
            print(f"Value counts for {col}:\n{df[col].value_counts()}")
            print()
        
        # Print the summary statistics
        print(f"Summary statistics:\n{df.describe()}") 