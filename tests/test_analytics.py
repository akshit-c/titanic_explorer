#!/usr/bin/env python3
"""
Tests for the analytics module.

This script tests the functionality of the analytics module,
including statistics calculations and data processing.
"""

import os
import sys
import unittest
import pandas as pd
import numpy as np

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.analytics.statistics import (
    calculate_survival_stats,
    calculate_demographic_stats,
    calculate_fare_stats,
    calculate_correlation_stats,
    calculate_statistical_tests
)


class TestAnalytics(unittest.TestCase):
    """Test cases for the analytics module."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data."""
        # Create a sample DataFrame for testing
        cls.df = pd.DataFrame({
            'survived': [True, False, True, False, True],
            'pclass': [1, 3, 1, 2, 3],
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Tom Wilson'],
            'sex': ['male', 'female', 'male', 'female', 'male'],
            'age': [25.0, 30.0, 45.0, 22.0, 18.0],
            'sibsp': [1, 0, 1, 0, 2],
            'parch': [0, 0, 1, 1, 3],
            'ticket': ['A123', 'B456', 'C789', 'D012', 'E345'],
            'fare': [100.0, 15.0, 80.0, 40.0, 30.0],
            'cabin': ['C123', None, 'E45', None, 'G67'],
            'embarked': ['C', 'S', 'C', 'Q', 'S']
        })
        
        # Add derived columns
        cls.df['family_size'] = cls.df['sibsp'] + cls.df['parch'] + 1
        cls.df['is_alone'] = (cls.df['family_size'] == 1).astype(int)
        cls.df['fare_per_person'] = cls.df['fare'] / cls.df['family_size']
    
    def test_calculate_survival_stats(self):
        """Test the calculate_survival_stats function."""
        stats = calculate_survival_stats(self.df)
        
        # Check that the function returns a dictionary
        self.assertIsInstance(stats, dict)
        
        # Check that the overall survival rate is correct
        self.assertAlmostEqual(stats['overall'], 60.0)
        
        # Check that survival by class is calculated
        self.assertIn('by_class', stats)
        self.assertIn(1, stats['by_class'])
        self.assertIn(2, stats['by_class'])
        self.assertIn(3, stats['by_class'])
        
        # Check that survival by sex is calculated
        self.assertIn('by_sex', stats)
        self.assertIn('male', stats['by_sex'])
        self.assertIn('female', stats['by_sex'])
    
    def test_calculate_demographic_stats(self):
        """Test the calculate_demographic_stats function."""
        stats = calculate_demographic_stats(self.df)
        
        # Check that the function returns a dictionary
        self.assertIsInstance(stats, dict)
        
        # Check that the total passengers count is correct
        self.assertEqual(stats['total_passengers'], 5)
        
        # Check that class distribution is calculated
        self.assertIn('class_counts', stats)
        self.assertIn('class_percentages', stats)
        
        # Check that gender distribution is calculated
        self.assertIn('gender_counts', stats)
        self.assertIn('gender_percentages', stats)
        
        # Check that age statistics are calculated
        self.assertIn('age_stats', stats)
        self.assertAlmostEqual(stats['age_stats']['mean'], 28.0)
    
    def test_calculate_fare_stats(self):
        """Test the calculate_fare_stats function."""
        stats = calculate_fare_stats(self.df)
        
        # Check that the function returns a dictionary
        self.assertIsInstance(stats, dict)
        
        # Check that overall fare statistics are calculated
        self.assertIn('overall', stats)
        self.assertAlmostEqual(stats['overall']['mean'], 53.0)
        
        # Check that fare by class is calculated
        self.assertIn('by_class', stats)
        
        # Check that fare by survival status is calculated
        self.assertIn('by_survival', stats)
    
    def test_calculate_correlation_stats(self):
        """Test the calculate_correlation_stats function."""
        stats = calculate_correlation_stats(self.df)
        
        # Check that the function returns a dictionary
        self.assertIsInstance(stats, dict)
        
        # Check that survival correlation is calculated
        self.assertIn('survival_correlation', stats)
        
        # Check that top correlations are calculated
        self.assertIn('top_correlations', stats)
        self.assertIsInstance(stats['top_correlations'], list)
    
    def test_calculate_statistical_tests(self):
        """Test the calculate_statistical_tests function."""
        stats = calculate_statistical_tests(self.df)
        
        # Check that the function returns a dictionary
        self.assertIsInstance(stats, dict)
        
        # Check that t-tests are calculated
        self.assertIn('age_ttest', stats)
        self.assertIn('fare_ttest', stats)
        
        # Check that chi-squared tests are calculated
        self.assertIn('class_chi2', stats)
        self.assertIn('sex_chi2', stats)
        self.assertIn('embarked_chi2', stats)


if __name__ == '__main__':
    unittest.main()
