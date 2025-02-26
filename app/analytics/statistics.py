import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple


def calculate_survival_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate survival statistics for the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        
    Returns:
        A dictionary containing survival statistics
    """
    # Overall survival rate
    survival_rate = df['survived'].mean() * 100
    
    # Survival by class
    survival_by_class = df.groupby('pclass')['survived'].mean() * 100
    
    # Survival by sex
    survival_by_sex = df.groupby('sex')['survived'].mean() * 100
    
    # Survival by age group
    df['age_group'] = pd.cut(
        df['age'],
        bins=[0, 12, 18, 35, 60, 100],
        labels=['Child', 'Teen', 'Young Adult', 'Adult', 'Senior']
    )
    survival_by_age_group = df.groupby('age_group')['survived'].mean() * 100
    
    # Survival by embarkation port
    survival_by_embarked = df.groupby('embarked')['survived'].mean() * 100
    
    # Survival by family size
    df['family_size_group'] = pd.cut(
        df['sibsp'] + df['parch'],
        bins=[-1, 0, 3, 10],
        labels=['Alone', 'Small Family', 'Large Family']
    )
    survival_by_family_size = df.groupby('family_size_group')['survived'].mean() * 100
    
    return {
        'overall': survival_rate,
        'by_class': survival_by_class.to_dict(),
        'by_sex': survival_by_sex.to_dict(),
        'by_age_group': survival_by_age_group.to_dict(),
        'by_embarked': survival_by_embarked.to_dict(),
        'by_family_size': survival_by_family_size.to_dict()
    }


def calculate_demographic_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate demographic statistics for the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        
    Returns:
        A dictionary containing demographic statistics
    """
    # Total passengers
    total_passengers = len(df)
    
    # Class distribution
    class_counts = df['pclass'].value_counts().sort_index()
    class_percentages = (class_counts / total_passengers * 100).to_dict()
    
    # Gender distribution
    gender_counts = df['sex'].value_counts()
    gender_percentages = (gender_counts / total_passengers * 100).to_dict()
    
    # Age statistics
    age_stats = {
        'mean': df['age'].mean(),
        'median': df['age'].median(),
        'min': df['age'].min(),
        'max': df['age'].max(),
        'std': df['age'].std()
    }
    
    # Age distribution
    age_groups = pd.cut(
        df['age'],
        bins=[0, 12, 18, 35, 60, 100],
        labels=['Child', 'Teen', 'Young Adult', 'Adult', 'Senior']
    ).value_counts().sort_index()
    age_group_percentages = (age_groups / total_passengers * 100).to_dict()
    
    # Embarkation port distribution
    embarked_counts = df['embarked'].value_counts()
    embarked_percentages = (embarked_counts / total_passengers * 100).to_dict()
    
    # Family size distribution
    family_size = df['sibsp'] + df['parch']
    family_size_stats = {
        'mean': family_size.mean(),
        'median': family_size.median(),
        'min': family_size.min(),
        'max': family_size.max(),
        'std': family_size.std()
    }
    
    return {
        'total_passengers': total_passengers,
        'class_counts': class_counts.to_dict(),
        'class_percentages': class_percentages,
        'gender_counts': gender_counts.to_dict(),
        'gender_percentages': gender_percentages,
        'age_stats': age_stats,
        'age_group_percentages': age_group_percentages,
        'embarked_counts': embarked_counts.to_dict(),
        'embarked_percentages': embarked_percentages,
        'family_size_stats': family_size_stats
    }


def calculate_fare_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate fare statistics for the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        
    Returns:
        A dictionary containing fare statistics
    """
    # Overall fare statistics
    fare_stats = {
        'mean': df['fare'].mean(),
        'median': df['fare'].median(),
        'min': df['fare'].min(),
        'max': df['fare'].max(),
        'std': df['fare'].std()
    }
    
    # Fare by class
    fare_by_class = df.groupby('pclass')['fare'].agg(['mean', 'median', 'min', 'max', 'std'])
    
    # Fare by survival status
    fare_by_survival = df.groupby('survived')['fare'].agg(['mean', 'median', 'min', 'max', 'std'])
    
    # Fare by embarkation port
    fare_by_embarked = df.groupby('embarked')['fare'].agg(['mean', 'median', 'min', 'max', 'std'])
    
    return {
        'overall': fare_stats,
        'by_class': fare_by_class.to_dict(),
        'by_survival': fare_by_survival.to_dict(),
        'by_embarked': fare_by_embarked.to_dict()
    }


def calculate_correlation_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate correlation statistics for the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        
    Returns:
        A dictionary containing correlation statistics
    """
    # Create a copy of the dataframe with only numeric columns
    numeric_df = df.select_dtypes(include=[np.number]).copy()
    
    # Calculate correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Calculate correlation with survival
    survival_corr = corr_matrix['survived'].drop('survived').to_dict()
    
    # Calculate top correlations
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            corr = corr_matrix.iloc[i, j]
            corr_pairs.append((col1, col2, corr))
    
    # Sort by absolute correlation
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # Convert to dictionary
    top_correlations = [
        {'var1': pair[0], 'var2': pair[1], 'correlation': pair[2]}
        for pair in corr_pairs[:5]  # Top 5 correlations
    ]
    
    return {
        'survival_correlation': survival_corr,
        'top_correlations': top_correlations,
        'correlation_matrix': corr_matrix.to_dict()
    }


def calculate_statistical_tests(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate statistical tests for the Titanic dataset.
    
    Args:
        df: The Titanic dataset
        
    Returns:
        A dictionary containing statistical test results
    """
    from scipy import stats
    
    # T-test for age between survivors and non-survivors
    survived_age = df[df['survived']]['age']
    not_survived_age = df[~df['survived']]['age']
    age_ttest = stats.ttest_ind(survived_age, not_survived_age, equal_var=False)
    
    # T-test for fare between survivors and non-survivors
    survived_fare = df[df['survived']]['fare']
    not_survived_fare = df[~df['survived']]['fare']
    fare_ttest = stats.ttest_ind(survived_fare, not_survived_fare, equal_var=False)
    
    # Chi-squared test for class and survival
    class_survival_table = pd.crosstab(df['pclass'], df['survived'])
    class_chi2 = stats.chi2_contingency(class_survival_table)
    
    # Chi-squared test for sex and survival
    sex_survival_table = pd.crosstab(df['sex'], df['survived'])
    sex_chi2 = stats.chi2_contingency(sex_survival_table)
    
    # Chi-squared test for embarked and survival
    embarked_survival_table = pd.crosstab(df['embarked'], df['survived'])
    embarked_chi2 = stats.chi2_contingency(embarked_survival_table)
    
    return {
        'age_ttest': {
            'statistic': age_ttest.statistic,
            'pvalue': age_ttest.pvalue,
            'significant': age_ttest.pvalue < 0.05
        },
        'fare_ttest': {
            'statistic': fare_ttest.statistic,
            'pvalue': fare_ttest.pvalue,
            'significant': fare_ttest.pvalue < 0.05
        },
        'class_chi2': {
            'statistic': class_chi2[0],
            'pvalue': class_chi2[1],
            'significant': class_chi2[1] < 0.05
        },
        'sex_chi2': {
            'statistic': sex_chi2[0],
            'pvalue': sex_chi2[1],
            'significant': sex_chi2[1] < 0.05
        },
        'embarked_chi2': {
            'statistic': embarked_chi2[0],
            'pvalue': embarked_chi2[1],
            'significant': embarked_chi2[1] < 0.05
        }
    }
