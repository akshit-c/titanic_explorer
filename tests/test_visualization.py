#!/usr/bin/env python3
"""
Tests for the visualization module.

This script tests the functionality of the visualization module,
including chart generation and formatting.
"""

import os
import sys
import unittest
import pandas as pd
import numpy as np
import tempfile
import shutil

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.visualization.charts import (
    generate_visualization,
    create_bar_chart,
    create_histogram,
    create_scatter_plot,
    create_pie_chart,
    create_line_chart,
    create_heatmap,
    create_box_plot
)
from app.visualization.formatters import (
    format_visualization_for_api,
    format_visualization_for_streamlit,
    format_text_response
)


class TestVisualization(unittest.TestCase):
    """Test cases for the visualization module."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data and temporary directory."""
        # Create a sample DataFrame for testing
        cls.df = pd.DataFrame({
            'survived': [True, False, True, False, True],
            'pclass': [1, 3, 1, 2, 3],
            'sex': ['male', 'female', 'male', 'female', 'male'],
            'age': [25.0, 30.0, 45.0, 22.0, 18.0],
            'fare': [100.0, 15.0, 80.0, 40.0, 30.0],
            'embarked': ['C', 'S', 'C', 'Q', 'S']
        })
        
        # Create a temporary directory for test visualizations
        cls.temp_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up temporary directory."""
        shutil.rmtree(cls.temp_dir)
    
    def test_generate_visualization_bar(self):
        """Test generating a bar chart."""
        filepath = os.path.join(self.temp_dir, "bar_chart.png")
        result = generate_visualization(
            data=self.df,
            visualization_type="bar",
            filepath=filepath,
            title="Test Bar Chart",
            x_col="pclass",
            y_col="fare"
        )
        
        # Check that the file was created
        self.assertTrue(os.path.exists(filepath))
        
        # Check that the function returns the filepath
        self.assertEqual(result, filepath)
    
    def test_generate_visualization_histogram(self):
        """Test generating a histogram."""
        filepath = os.path.join(self.temp_dir, "histogram.png")
        result = generate_visualization(
            data=self.df,
            visualization_type="histogram",
            filepath=filepath,
            title="Test Histogram",
            x_col="age",
            bins=5
        )
        
        # Check that the file was created
        self.assertTrue(os.path.exists(filepath))
        
        # Check that the function returns the filepath
        self.assertEqual(result, filepath)
    
    def test_generate_visualization_scatter(self):
        """Test generating a scatter plot."""
        filepath = os.path.join(self.temp_dir, "scatter_plot.png")
        result = generate_visualization(
            data=self.df,
            visualization_type="scatter",
            filepath=filepath,
            title="Test Scatter Plot",
            x_col="age",
            y_col="fare",
            hue_col="survived"
        )
        
        # Check that the file was created
        self.assertTrue(os.path.exists(filepath))
        
        # Check that the function returns the filepath
        self.assertEqual(result, filepath)
    
    def test_generate_visualization_pie(self):
        """Test generating a pie chart."""
        # Create a DataFrame with counts
        counts = self.df['pclass'].value_counts().reset_index()
        counts.columns = ['pclass', 'count']
        
        filepath = os.path.join(self.temp_dir, "pie_chart.png")
        result = generate_visualization(
            data=counts,
            visualization_type="pie",
            filepath=filepath,
            title="Test Pie Chart",
            label_col="pclass",
            value_col="count"
        )
        
        # Check that the file was created
        self.assertTrue(os.path.exists(filepath))
        
        # Check that the function returns the filepath
        self.assertEqual(result, filepath)
    
    def test_format_visualization_for_api(self):
        """Test formatting a visualization for API response."""
        # Generate a test visualization
        filepath = os.path.join(self.temp_dir, "test_api.png")
        generate_visualization(
            data=self.df,
            visualization_type="bar",
            filepath=filepath,
            title="Test API Formatting"
        )
        
        # Format the visualization for API
        result = format_visualization_for_api(filepath)
        
        # Check that the function returns a dictionary
        self.assertIsInstance(result, dict)
        
        # Check that the dictionary contains the expected keys
        self.assertIn("data_uri", result)
        self.assertIn("mime_type", result)
        self.assertIn("filename", result)
        
        # Check that the data URI starts with the expected prefix
        self.assertTrue(result["data_uri"].startswith("data:image/png;base64,"))
    
    def test_format_visualization_for_streamlit(self):
        """Test formatting a visualization for Streamlit."""
        # Generate a test visualization
        filepath = os.path.join(self.temp_dir, "test_streamlit.png")
        generate_visualization(
            data=self.df,
            visualization_type="bar",
            filepath=filepath,
            title="Test Streamlit Formatting"
        )
        
        # Format the visualization for Streamlit
        result = format_visualization_for_streamlit(filepath)
        
        # Check that the function returns a string
        self.assertIsInstance(result, str)
        
        # Check that the string contains the expected HTML
        self.assertTrue(result.startswith('<img src="data:image/png;base64,'))
        self.assertTrue('alt="Visualization"' in result)
    
    def test_format_text_response(self):
        """Test formatting a text response."""
        text = "This is a test response.\n\nIt has multiple paragraphs."
        visualization_type = "bar"
        
        # Format the text response
        result = format_text_response(text, visualization_type)
        
        # Check that the function returns a string
        self.assertIsInstance(result, str)
        
        # Check that the string contains the expected HTML
        self.assertTrue("<p>This is a test response.</p>" in result)
        self.assertTrue("<p>It has multiple paragraphs.</p>" in result)
        self.assertTrue(f"<p><em>A {visualization_type} chart has been generated to illustrate this data.</em></p>" in result)


if __name__ == '__main__':
    unittest.main() 