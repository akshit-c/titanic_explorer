#!/usr/bin/env python3
"""
Data Preprocessing Script

This script preprocesses the Titanic dataset and saves it to the processed directory.
"""

import os
import sys
import pandas as pd

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.analytics.processor import preprocess_data


def main():
    """Main function to preprocess the Titanic dataset."""
    # Define paths
    raw_path = os.path.join("data", "raw", "titanic.csv")
    processed_path = os.path.join("data", "processed", "titanic_clean.csv")
    
    # Check if the raw dataset exists
    if not os.path.exists(raw_path):
        print(f"Error: Raw dataset not found at {raw_path}")
        sys.exit(1)
    
    print(f"Loading raw dataset from {raw_path}...")
    
    # Load the raw dataset
    df = pd.read_csv(raw_path)
    
    print(f"Raw dataset loaded. Shape: {df.shape}")
    
    # Preprocess the dataset
    print("Preprocessing dataset...")
    df_processed = preprocess_data(df)
    
    print(f"Preprocessing complete. Shape: {df_processed.shape}")
    
    # Create the processed directory if it doesn't exist
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    
    # Save the processed dataset
    print(f"Saving processed dataset to {processed_path}...")
    df_processed.to_csv(processed_path, index=False)
    
    print("Preprocessing complete!")


if __name__ == "__main__":
    main()
