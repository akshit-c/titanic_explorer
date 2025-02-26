import os
import uuid
from typing import Dict, Any, Optional, List, Tuple
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from app.analytics.processor import (
    analyze_data, analyze_survival, analyze_class, analyze_age,
    analyze_gender, analyze_fare, analyze_embarked, analyze_general,
    load_titanic_data, preprocess_data
)
from app.core.config import settings


class TitanicChatbot:
    """
    A rule-based chatbot for answering questions about the Titanic dataset.
    This replaces the LLM-based approach with a deterministic one.
    """
    
    def __init__(self):
        """Initialize the chatbot."""
        # Load the dataset once to ensure it's available
        self.df = load_titanic_data()
        if self.df is not None:
            # Preprocess the data
            self.df = preprocess_data(self.df)
        
        # Define keywords for different types of analyses
        self.keywords = {
            "survival": ["survival", "survived", "die", "died", "death", "alive", "dead"],
            "class": ["class", "pclass", "first class", "second class", "third class", "1st", "2nd", "3rd"],
            "age": ["age", "young", "old", "child", "children", "adult", "elderly", "baby", "infant"],
            "gender": ["gender", "sex", "male", "female", "men", "women", "man", "woman", "boy", "girl"],
            "fare": ["fare", "price", "ticket", "cost", "expensive", "cheap", "payment"],
            "embarked": ["embarked", "port", "boarding", "cherbourg", "queenstown", "southampton", "c", "q", "s"],
            "family": ["family", "sibling", "spouse", "sibsp", "parent", "child", "parch", "relative"],
            "cabin": ["cabin", "deck", "room", "accommodation"],
            "name": ["name", "title", "mr", "mrs", "miss", "master", "dr", "rev"],
            "correlation": ["correlation", "related", "relationship", "impact", "effect", "influence", "factor"]
        }
    
    def process_query(self, query_text: str) -> Dict[str, Any]:
        """
        Process a natural language query about the Titanic dataset.
        
        Args:
            query_text: The user's query text
            
        Returns:
            A dictionary containing:
            - text_content: The text response
            - visualization_type: The type of visualization generated
            - visualization_path: The path to the visualization file
        """
        # Check if the dataset is loaded
        if self.df is None:
            return {
                "text_content": "I'm sorry, but I couldn't load the Titanic dataset. Please check the data file and try again.",
                "visualization_type": None,
                "visualization_path": None
            }
        
        # Determine the analysis type based on the query
        analysis_type = self._determine_analysis_type(query_text)
        
        # Perform the data analysis
        analysis_result = analyze_data(analysis_type, query_text)
        
        # Generate visualization
        visualization_type = analysis_result.get("visualization_type", "bar")
        visualization_path = None
        
        if visualization_type:
            # Generate a unique filename for the visualization
            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join(settings.VISUALIZATIONS_DIR, filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Generate the visualization
            from app.visualization.charts import generate_visualization
            visualization_path = generate_visualization(
                data=analysis_result.get("data"),
                visualization_type=visualization_type,
                filepath=filepath,
                title=analysis_result.get("title", "Titanic Data Analysis"),
                color_scheme="viridis",
                annotations=[]
            )
        
        # Generate a text response based on the analysis result
        text_content = self._generate_response(query_text, analysis_type, analysis_result)
        
        return {
            "text_content": text_content,
            "visualization_type": visualization_type,
            "visualization_path": visualization_path
        }
    
    def _determine_analysis_type(self, query_text: str) -> str:
        """
        Determine the type of analysis to perform based on the query text.
        
        Args:
            query_text: The user's query text
            
        Returns:
            The analysis type
        """
        query_lower = query_text.lower()
        
        # Count keyword matches for each analysis type
        matches = {}
        for analysis_type, keywords in self.keywords.items():
            count = sum(1 for keyword in keywords if keyword in query_lower)
            matches[analysis_type] = count
        
        # Find the analysis type with the most keyword matches
        max_matches = max(matches.values())
        if max_matches == 0:
            return "general_analysis"
        
        # Get all analysis types with the maximum number of matches
        top_matches = [analysis_type for analysis_type, count in matches.items() if count == max_matches]
        
        # Map the analysis types to the function names
        analysis_mapping = {
            "survival": "survival_analysis",
            "class": "class_analysis",
            "age": "age_analysis",
            "gender": "gender_analysis",
            "fare": "fare_analysis",
            "embarked": "embarked_analysis",
            "family": "general_analysis",
            "cabin": "general_analysis",
            "name": "general_analysis",
            "correlation": "correlation_analysis"
        }
        
        # Return the first matching analysis type
        return analysis_mapping.get(top_matches[0], "general_analysis")
    
    def _generate_response(self, query_text: str, analysis_type: str, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a text response based on the analysis result.
        
        Args:
            query_text: The user's query text
            analysis_type: The type of analysis performed
            analysis_result: The result of the analysis
            
        Returns:
            The text response
        """
        # Get the summary from the analysis result
        summary = analysis_result.get("summary", "")
        
        # Create a response based on the analysis type
        if analysis_type == "survival_analysis":
            response = self._generate_survival_response(query_text, analysis_result)
        elif analysis_type == "class_analysis":
            response = self._generate_class_response(query_text, analysis_result)
        elif analysis_type == "age_analysis":
            response = self._generate_age_response(query_text, analysis_result)
        elif analysis_type == "gender_analysis":
            response = self._generate_gender_response(query_text, analysis_result)
        elif analysis_type == "fare_analysis":
            response = self._generate_fare_response(query_text, analysis_result)
        elif analysis_type == "embarked_analysis":
            response = self._generate_embarked_response(query_text, analysis_result)
        elif analysis_type == "correlation_analysis":
            response = self._generate_correlation_response(query_text, analysis_result)
        else:
            response = self._generate_general_response(query_text, analysis_result)
        
        # Add follow-up suggestions
        response += "\n\n" + self._generate_followup_suggestions(analysis_type)
        
        return response
    
    def _generate_survival_response(self, query_text: str, analysis_result: Dict[str, Any]) -> str:
        """Generate a response for survival analysis."""
        summary = analysis_result.get("summary", "")
        
        response = f"# Survival Analysis\n\n{summary}\n\n"
        response += "The Titanic disaster was one of the deadliest maritime disasters in history. "
        response += "The survival rates were significantly influenced by factors such as passenger class, gender, and age. "
        response += "First-class passengers had better access to lifeboats, and the 'women and children first' policy greatly affected survival rates by gender."
        
        return response
    
    def _generate_class_response(self, query_text: str, analysis_result: Dict[str, Any]) -> str:
        """Generate a response for class analysis."""
        summary = analysis_result.get("summary", "")
        
        response = f"# Passenger Class Analysis\n\n{summary}\n\n"
        response += "The Titanic had three passenger classes, each with different accommodations and ticket prices. "
        response += "First-class passengers were wealthy and had cabins on the upper decks, closer to the lifeboats. "
        response += "Second-class accommodations were comparable to first-class on other ships. "
        response += "Third-class passengers were in the lower decks and had more limited access to the lifeboats during the emergency."
        
        return response
    
    def _generate_age_response(self, query_text: str, analysis_result: Dict[str, Any]) -> str:
        """Generate a response for age analysis."""
        summary = analysis_result.get("summary", "")
        
        response = f"# Age Analysis\n\n{summary}\n\n"
        response += "Age played a significant role in survival rates on the Titanic. "
        response += "The 'women and children first' policy meant that children had a higher chance of survival. "
        response += "However, very young children, especially infants, had lower survival rates than older children. "
        response += "Elderly passengers also had lower survival rates, possibly due to mobility issues during the evacuation."
        
        return response
    
    def _generate_gender_response(self, query_text: str, analysis_result: Dict[str, Any]) -> str:
        """Generate a response for gender analysis."""
        summary = analysis_result.get("summary", "")
        
        response = f"# Gender Analysis\n\n{summary}\n\n"
        response += "Gender was one of the most significant factors in determining survival rates on the Titanic. "
        response += "The 'women and children first' policy for loading lifeboats meant that women had a much higher chance of survival. "
        response += "This policy was more strictly followed in first and second class, which is why the disparity between male and female survival rates is most pronounced in those classes."
        
        return response
    
    def _generate_fare_response(self, query_text: str, analysis_result: Dict[str, Any]) -> str:
        """Generate a response for fare analysis."""
        summary = analysis_result.get("summary", "")
        
        response = f"# Fare Analysis\n\n{summary}\n\n"
        response += "Ticket prices varied significantly on the Titanic, reflecting the different classes and accommodations. "
        response += "Higher fares generally corresponded to first-class accommodations, which were located on the upper decks closer to the lifeboats. "
        response += "This proximity to lifeboats, along with preferential treatment during evacuation, contributed to the higher survival rates among passengers who paid more for their tickets."
        
        return response
    
    def _generate_embarked_response(self, query_text: str, analysis_result: Dict[str, Any]) -> str:
        """Generate a response for embarkation port analysis."""
        summary = analysis_result.get("summary", "")
        
        response = f"# Embarkation Port Analysis\n\n{summary}\n\n"
        response += "The Titanic picked up passengers at three ports: Southampton (England), Cherbourg (France), and Queenstown (now Cobh, Ireland). "
        response += "The majority of passengers boarded at Southampton, the first stop. "
        response += "Interestingly, passengers who boarded at Cherbourg had the highest survival rate, possibly because they included a higher proportion of first-class passengers. "
        response += "Southampton had more third-class passengers, which may explain the lower survival rate for passengers who embarked there."
        
        return response
    
    def _generate_correlation_response(self, query_text: str, analysis_result: Dict[str, Any]) -> str:
        """Generate a response for correlation analysis."""
        summary = analysis_result.get("summary", "")
        
        response = f"# Correlation Analysis\n\n{summary}\n\n"
        response += "Several factors were correlated with survival rates on the Titanic. "
        response += "The strongest correlations were with passenger class, gender, and age. "
        response += "First-class passengers, women, and children had higher survival rates. "
        response += "These correlations reflect the evacuation procedures and social norms of the time, "
        response += "as well as the physical layout of the ship, with first-class accommodations being closer to the lifeboats."
        
        return response
    
    def _generate_general_response(self, query_text: str, analysis_result: Dict[str, Any]) -> str:
        """Generate a general response."""
        summary = analysis_result.get("summary", "")
        
        response = f"# Titanic Dataset Overview\n\n{summary}\n\n"
        response += "The Titanic sank on April 15, 1912, after colliding with an iceberg during her maiden voyage. "
        response += "Of the estimated 2,224 passengers and crew aboard, more than 1,500 died, making it one of the deadliest commercial peacetime maritime disasters in modern history. "
        response += "The dataset reveals significant disparities in survival rates based on factors such as passenger class, gender, and age. "
        response += "These disparities reflect the social norms and evacuation procedures of the time, particularly the 'women and children first' policy."
        
        return response
    
    def _generate_followup_suggestions(self, analysis_type: str) -> str:
        """Generate follow-up suggestions based on the analysis type."""
        suggestions = "## You might also be interested in:\n\n"
        
        if analysis_type != "survival_analysis":
            suggestions += "- What was the overall survival rate on the Titanic?\n"
        if analysis_type != "class_analysis":
            suggestions += "- How did passenger class affect survival rates?\n"
        if analysis_type != "age_analysis":
            suggestions += "- What was the age distribution of Titanic passengers?\n"
        if analysis_type != "gender_analysis":
            suggestions += "- How did gender affect survival rates?\n"
        if analysis_type != "fare_analysis":
            suggestions += "- What was the relationship between ticket price and survival?\n"
        if analysis_type != "embarked_analysis":
            suggestions += "- Did the port of embarkation affect survival rates?\n"
        
        return suggestions 