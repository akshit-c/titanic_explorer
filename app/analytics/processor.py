import os
import pandas as pd
from typing import Dict, Any, List, Optional
import sys

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the loader function
from app.data.loader import load_titanic_data as load_data_from_loader

# Path to the Titanic dataset
DATASET_PATH = os.path.join("data", "processed", "titanic_clean.csv")


def load_titanic_data() -> pd.DataFrame:
    """
    Load the Titanic dataset.
    
    Returns:
        A pandas DataFrame containing the Titanic dataset
    """
    try:
        # Try to use the loader function
        df = load_data_from_loader()
        if df is not None:
            # Preprocess the dataset
            df = preprocess_data(df)
            
            # Save the processed dataset
            os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
            df.to_csv(DATASET_PATH, index=False)
            return df
    except Exception as e:
        print(f"Error loading data from loader: {str(e)}")
    
    # Fallback to the original method
    # Check if the processed dataset exists
    if not os.path.exists(DATASET_PATH):
        # If not, use the raw dataset
        raw_path = os.path.join("data", "raw", "titanic.csv")
        
        # Check if the raw dataset exists
        if not os.path.exists(raw_path):
            # Try to use the local file in app/data
            local_csv_path = os.path.join("app", "data", "titanic.csv")
            if os.path.exists(local_csv_path):
                print(f"Using local Titanic dataset from {local_csv_path}...")
                df = pd.read_csv(local_csv_path)
            else:
                raise FileNotFoundError(f"Titanic dataset not found at {raw_path} or {local_csv_path}")
        else:
            # Load the raw dataset
            df = pd.read_csv(raw_path)
        
        # Preprocess the dataset
        df = preprocess_data(df)
        
        # Save the processed dataset
        os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
        df.to_csv(DATASET_PATH, index=False)
    else:
        # Load the processed dataset
        df = pd.read_csv(DATASET_PATH)
    
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the Titanic dataset.
    
    Args:
        df: The raw Titanic dataset
        
    Returns:
        The preprocessed dataset
    """
    # Make a copy of the dataframe
    df = df.copy()
    
    # Standardize column names (convert to lowercase)
    df.columns = [col.lower() for col in df.columns]
    
    # Ensure all required columns exist
    required_columns = ['survived', 'pclass', 'name', 'sex', 'age', 'sibsp', 'parch', 'ticket', 'fare', 'cabin', 'embarked']
    for col in required_columns:
        if col not in df.columns:
            # Try to find a similar column
            similar_cols = [c for c in df.columns if col in c.lower()]
            if similar_cols:
                # Use the first similar column
                df[col] = df[similar_cols[0]]
            else:
                # Create an empty column
                df[col] = None
    
    # Convert 'survived' to boolean
    if 'survived' in df.columns:
        df['survived'] = df['survived'].astype(bool)
    
    # Fill missing age values with median
    if 'age' in df.columns:
        df['age'].fillna(df['age'].median(), inplace=True)
    
    # Fill missing embarked values with mode
    if 'embarked' in df.columns:
        df['embarked'].fillna(df['embarked'].mode()[0] if not df['embarked'].mode().empty else 'S', inplace=True)
    
    # Create a 'title' column from the 'name' column
    if 'name' in df.columns:
        df['title'] = df['name'].str.extract(' ([A-Za-z]+)\.', expand=False)
        
        # Map rare titles to more common ones
        title_mapping = {
            "Mr": "Mr",
            "Miss": "Miss",
            "Mrs": "Mrs",
            "Master": "Master",
            "Dr": "Officer",
            "Rev": "Officer",
            "Col": "Officer",
            "Major": "Officer",
            "Mlle": "Miss",
            "Mme": "Mrs",
            "Don": "Royalty",
            "Lady": "Royalty",
            "Countess": "Royalty",
            "Jonkheer": "Royalty",
            "Sir": "Royalty",
            "Capt": "Officer",
            "Ms": "Mrs"
        }
        df['title'] = df['title'].map(title_mapping)
        
        # Fill missing titles with 'Mr'
        df['title'].fillna('Mr', inplace=True)
    
    # Create a 'family_size' column
    if 'sibsp' in df.columns and 'parch' in df.columns:
        df['family_size'] = df['sibsp'] + df['parch'] + 1
    
    # Create a 'is_alone' column
    if 'family_size' in df.columns:
        df['is_alone'] = (df['family_size'] == 1).astype(int)
    
    # Create a 'fare_per_person' column
    if 'fare' in df.columns and 'family_size' in df.columns:
        df['fare_per_person'] = df['fare'] / df['family_size']
    
    # Fill missing fare values with median
    if 'fare' in df.columns:
        df['fare'].fillna(df['fare'].median(), inplace=True)
    
    # Create age groups
    if 'age' in df.columns:
        df['age_group'] = pd.cut(
            df['age'],
            bins=[0, 12, 18, 35, 60, 100],
            labels=['Child', 'Teenager', 'Young Adult', 'Adult', 'Senior']
        )
    
    # Create fare groups
    if 'fare' in df.columns:
        df['fare_group'] = pd.qcut(
            df['fare'],
            q=4,
            labels=['Low', 'Medium-Low', 'Medium-High', 'High']
        )
    
    return df


def analyze_data(analysis_type: str, query_text: str) -> Dict[str, Any]:
    """
    Analyze the Titanic dataset based on the analysis type.
    
    Args:
        analysis_type: The type of analysis to perform
        query_text: The original query text
        
    Returns:
        A dictionary containing the analysis results
    """
    # Load the dataset
    df = load_titanic_data()
    
    # Perform the analysis based on the analysis type
    if analysis_type == "survival_analysis":
        return analyze_survival(df, query_text)
    elif analysis_type == "class_analysis":
        return analyze_class(df, query_text)
    elif analysis_type == "age_analysis":
        return analyze_age(df, query_text)
    elif analysis_type == "gender_analysis":
        return analyze_gender(df, query_text)
    elif analysis_type == "fare_analysis":
        return analyze_fare(df, query_text)
    elif analysis_type == "embarked_analysis":
        return analyze_embarked(df, query_text)
    else:
        return analyze_general(df, query_text)


def analyze_survival(df: pd.DataFrame, query_text: str) -> Dict[str, Any]:
    """
    Analyze survival rates in the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        query_text: The original query text
        
    Returns:
        A dictionary containing the analysis results
    """
    # Calculate overall survival rate
    survival_rate = df['survived'].mean() * 100
    
    # Calculate survival rates by different factors
    survival_by_class = df.groupby('pclass')['survived'].mean() * 100
    survival_by_sex = df.groupby('sex')['survived'].mean() * 100
    survival_by_embarked = df.groupby('embarked')['survived'].mean() * 100
    
    # Prepare data for visualization
    if "class" in query_text.lower():
        data = survival_by_class.reset_index()
        data.columns = ['Passenger Class', 'Survival Rate (%)']
        viz_type = "bar"
        title = "Survival Rate by Passenger Class"
    elif "gender" in query_text.lower() or "sex" in query_text.lower():
        data = survival_by_sex.reset_index()
        data.columns = ['Sex', 'Survival Rate (%)']
        viz_type = "bar"
        title = "Survival Rate by Gender"
    elif "embarked" in query_text.lower() or "port" in query_text.lower():
        data = survival_by_embarked.reset_index()
        data.columns = ['Port of Embarkation', 'Survival Rate (%)']
        viz_type = "bar"
        title = "Survival Rate by Port of Embarkation"
    else:
        # Default to overall survival visualization
        data = pd.DataFrame({
            'Status': ['Survived', 'Did not survive'],
            'Percentage': [survival_rate, 100 - survival_rate]
        })
        viz_type = "pie"
        title = "Overall Survival Rate"
    
    # Create summary text
    summary = f"The overall survival rate was {survival_rate:.1f}%. "
    summary += f"First class passengers had a {survival_by_class[1]:.1f}% survival rate, "
    summary += f"second class had {survival_by_class[2]:.1f}%, and third class had {survival_by_class[3]:.1f}%. "
    summary += f"Women had a {survival_by_sex['female']:.1f}% survival rate, while men had only {survival_by_sex['male']:.1f}%."
    
    return {
        "data": data,
        "visualization_type": viz_type,
        "title": title,
        "summary": summary
    }


def analyze_class(df: pd.DataFrame, query_text: str) -> Dict[str, Any]:
    """
    Analyze passenger class distribution in the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        query_text: The original query text
        
    Returns:
        A dictionary containing the analysis results
    """
    # Calculate class distribution
    class_counts = df['pclass'].value_counts().sort_index()
    class_percentages = class_counts / class_counts.sum() * 100
    
    # Calculate survival rates by class
    survival_by_class = df.groupby('pclass')['survived'].mean() * 100
    
    # Prepare data for visualization
    if "survival" in query_text.lower() or "survived" in query_text.lower():
        data = survival_by_class.reset_index()
        data.columns = ['Passenger Class', 'Survival Rate (%)']
        viz_type = "bar"
        title = "Survival Rate by Passenger Class"
    else:
        data = class_counts.reset_index()
        data.columns = ['Passenger Class', 'Count']
        viz_type = "bar"
        title = "Passenger Class Distribution"
    
    # Create summary text
    summary = f"There were {class_counts[1]} first class passengers ({class_percentages[1]:.1f}%), "
    summary += f"{class_counts[2]} second class passengers ({class_percentages[2]:.1f}%), and "
    summary += f"{class_counts[3]} third class passengers ({class_percentages[3]:.1f}%). "
    summary += f"The survival rates were {survival_by_class[1]:.1f}% for first class, "
    summary += f"{survival_by_class[2]:.1f}% for second class, and {survival_by_class[3]:.1f}% for third class."
    
    return {
        "data": data,
        "visualization_type": viz_type,
        "title": title,
        "summary": summary
    }


def analyze_age(df: pd.DataFrame, query_text: str) -> Dict[str, Any]:
    """
    Analyze age distribution in the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        query_text: The original query text
        
    Returns:
        A dictionary containing the analysis results
    """
    # Calculate age statistics
    age_mean = df['age'].mean()
    age_median = df['age'].median()
    age_min = df['age'].min()
    age_max = df['age'].max()
    
    # Prepare data for visualization
    if "survival" in query_text.lower() or "survived" in query_text.lower():
        # Age distribution by survival status
        data = df.copy()
        viz_type = "histogram"
        title = "Age Distribution by Survival Status"
    else:
        # Overall age distribution
        data = df[['age']].copy()
        viz_type = "histogram"
        title = "Age Distribution of Titanic Passengers"
    
    # Create summary text
    summary = f"The average age of Titanic passengers was {age_mean:.1f} years, with a median of {age_median:.1f} years. "
    summary += f"The youngest passenger was {age_min:.1f} years old, and the oldest was {age_max:.1f} years old. "
    
    # Add survival information if relevant
    if "survival" in query_text.lower() or "survived" in query_text.lower():
        survived_mean_age = df[df['survived']]['age'].mean()
        not_survived_mean_age = df[~df['survived']]['age'].mean()
        summary += f"Survivors had an average age of {survived_mean_age:.1f} years, "
        summary += f"while those who did not survive had an average age of {not_survived_mean_age:.1f} years."
    
    return {
        "data": data,
        "visualization_type": viz_type,
        "title": title,
        "summary": summary
    }


def analyze_gender(df: pd.DataFrame, query_text: str) -> Dict[str, Any]:
    """
    Analyze gender distribution in the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        query_text: The original query text
        
    Returns:
        A dictionary containing the analysis results
    """
    # Calculate gender distribution
    gender_counts = df['sex'].value_counts()
    gender_percentages = gender_counts / gender_counts.sum() * 100
    
    # Calculate survival rates by gender
    survival_by_gender = df.groupby('sex')['survived'].mean() * 100
    
    # Prepare data for visualization
    if "survival" in query_text.lower() or "survived" in query_text.lower():
        data = survival_by_gender.reset_index()
        data.columns = ['Sex', 'Survival Rate (%)']
        viz_type = "bar"
        title = "Survival Rate by Gender"
    else:
        data = gender_counts.reset_index()
        data.columns = ['Sex', 'Count']
        viz_type = "pie"
        title = "Gender Distribution of Titanic Passengers"
    
    # Create summary text
    summary = f"There were {gender_counts['male']} male passengers ({gender_percentages['male']:.1f}%) and "
    summary += f"{gender_counts['female']} female passengers ({gender_percentages['female']:.1f}%). "
    summary += f"The survival rate for women was {survival_by_gender['female']:.1f}%, "
    summary += f"while for men it was only {survival_by_gender['male']:.1f}%."
    
    return {
        "data": data,
        "visualization_type": viz_type,
        "title": title,
        "summary": summary
    }


def analyze_fare(df: pd.DataFrame, query_text: str) -> Dict[str, Any]:
    """
    Analyze fare prices in the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        query_text: The original query text
        
    Returns:
        A dictionary containing the analysis results
    """
    # Calculate fare statistics
    fare_mean = df['fare'].mean()
    fare_median = df['fare'].median()
    fare_min = df['fare'].min()
    fare_max = df['fare'].max()
    
    # Calculate fare statistics by class
    fare_by_class = df.groupby('pclass')['fare'].agg(['mean', 'median'])
    
    # Check for distribution-related keywords
    distribution_keywords = ["distribution", "histogram", "spread", "range", "variation"]
    is_distribution_query = any(keyword in query_text.lower() for keyword in distribution_keywords)
    
    # Prepare data for visualization
    if "class" in query_text.lower():
        data = fare_by_class['mean'].reset_index()
        data.columns = ['Passenger Class', 'Average Fare']
        viz_type = "bar"
        title = "Average Fare by Passenger Class"
    elif "survival" in query_text.lower() or "survived" in query_text.lower() or "relationship" in query_text.lower():
        # For relationship or survival queries, use a violin plot instead of histogram
        data = df.copy()
        viz_type = "violin"
        title = "Fare Distribution by Survival Status"
    elif is_distribution_query:
        # Overall fare distribution as KDE plot
        data = df[['fare']].copy()
        viz_type = "kde"
        title = "Fare Distribution of Titanic Passengers"
    else:
        # Default to a bar chart showing fare distribution by passenger class
        data = fare_by_class['mean'].reset_index()
        data.columns = ['Passenger Class', 'Average Fare']
        viz_type = "bar"
        title = "Average Fare by Passenger Class"
    
    # Create summary text
    summary = f"The average fare was £{fare_mean:.2f}, with a median of £{fare_median:.2f}. "
    summary += f"Fares ranged from £{fare_min:.2f} to £{fare_max:.2f}. "
    summary += f"First class passengers paid an average of £{fare_by_class.loc[1, 'mean']:.2f}, "
    summary += f"second class paid £{fare_by_class.loc[2, 'mean']:.2f}, and "
    summary += f"third class paid £{fare_by_class.loc[3, 'mean']:.2f}."
    
    # Add survival information if relevant
    if "survival" in query_text.lower() or "survived" in query_text.lower() or "relationship" in query_text.lower():
        survived_mean_fare = df[df['survived']]['fare'].mean()
        not_survived_mean_fare = df[~df['survived']]['fare'].mean()
        summary += f" Passengers who survived paid an average fare of £{survived_mean_fare:.2f}, "
        summary += f"while those who did not survive paid an average of £{not_survived_mean_fare:.2f}."
        
        # Add more detailed information about the relationship between fare and survival
        if "relationship" in query_text.lower():
            summary += f" There appears to be a correlation between ticket prices and survival rates. "
            summary += f"Higher fares were generally associated with better accommodations and possibly "
            summary += f"better access to lifeboats, which may have contributed to higher survival rates "
            summary += f"among passengers who paid more for their tickets."
    
    return {
        "data": data,
        "visualization_type": viz_type,
        "title": title,
        "summary": summary
    }


def analyze_embarked(df: pd.DataFrame, query_text: str) -> Dict[str, Any]:
    """
    Analyze embarkation port distribution in the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        query_text: The original query text
        
    Returns:
        A dictionary containing the analysis results
    """
    # Calculate embarkation port distribution
    embarked_counts = df['embarked'].value_counts()
    embarked_percentages = embarked_counts / embarked_counts.sum() * 100
    
    # Calculate survival rates by embarkation port
    survival_by_embarked = df.groupby('embarked')['survived'].mean() * 100
    
    # Map port codes to names
    port_names = {
        'C': 'Cherbourg',
        'Q': 'Queenstown',
        'S': 'Southampton'
    }
    
    # Prepare data for visualization
    if "survival" in query_text.lower() or "survived" in query_text.lower():
        data = survival_by_embarked.reset_index()
        data['embarked'] = data['embarked'].map(port_names)
        data.columns = ['Port of Embarkation', 'Survival Rate (%)']
        viz_type = "bar"
        title = "Survival Rate by Port of Embarkation"
    else:
        data = embarked_counts.reset_index()
        data['embarked'] = data['embarked'].map(port_names)
        data.columns = ['Port of Embarkation', 'Count']
        viz_type = "pie"
        title = "Embarkation Port Distribution"
    
    # Create summary text
    summary = f"{embarked_percentages['S']:.1f}% of passengers embarked from Southampton, "
    summary += f"{embarked_percentages['C']:.1f}% from Cherbourg, and "
    summary += f"{embarked_percentages['Q']:.1f}% from Queenstown. "
    summary += f"The survival rates were {survival_by_embarked['S']:.1f}% for Southampton, "
    summary += f"{survival_by_embarked['C']:.1f}% for Cherbourg, and "
    summary += f"{survival_by_embarked['Q']:.1f}% for Queenstown."
    
    return {
        "data": data,
        "visualization_type": viz_type,
        "title": title,
        "summary": summary
    }


def analyze_general(df: pd.DataFrame, query_text: str) -> Dict[str, Any]:
    """
    Perform a general analysis of the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        query_text: The original query text
        
    Returns:
        A dictionary containing the analysis results
    """
    # Calculate overall statistics
    total_passengers = len(df)
    survival_rate = df['survived'].mean() * 100
    
    # Gender distribution
    gender_counts = df['sex'].value_counts()
    gender_percentages = gender_counts / gender_counts.sum() * 100
    
    # Class distribution
    class_counts = df['pclass'].value_counts().sort_index()
    class_percentages = class_counts / class_counts.sum() * 100
    
    # Age statistics
    age_mean = df['age'].mean()
    age_median = df['age'].median()
    
    # Prepare data for visualization
    # Default to survival rate by class and gender
    pivot_data = df.pivot_table(
        index='pclass',
        columns='sex',
        values='survived',
        aggfunc='mean'
    ) * 100
    
    data = pivot_data.reset_index()
    viz_type = "heatmap"
    title = "Survival Rate by Class and Gender"
    
    # Create summary text
    summary = f"The Titanic had {total_passengers} passengers, with an overall survival rate of {survival_rate:.1f}%. "
    summary += f"There were {gender_counts['male']} men ({gender_percentages['male']:.1f}%) and "
    summary += f"{gender_counts['female']} women ({gender_percentages['female']:.1f}%). "
    summary += f"The passengers were divided into first class ({class_percentages[1]:.1f}%), "
    summary += f"second class ({class_percentages[2]:.1f}%), and third class ({class_percentages[3]:.1f}%). "
    summary += f"The average age was {age_mean:.1f} years, with a median of {age_median:.1f} years."
    
    return {
        "data": data,
        "visualization_type": viz_type,
        "title": title,
        "summary": summary
    }
