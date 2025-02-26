import json
import re
from typing import Dict, Any, List, Optional


def parse_llm_response(response: str) -> Dict[str, Any]:
    """
    Parse the response from the LLM to extract structured information.
    
    Args:
        response: The raw response from the LLM
        
    Returns:
        A dictionary containing the parsed information
    """
    # Extract any JSON blocks from the response
    json_blocks = extract_json_blocks(response)
    
    if json_blocks:
        # Use the first JSON block as the structured data
        try:
            structured_data = json.loads(json_blocks[0])
            return structured_data
        except json.JSONDecodeError:
            pass
    
    # If no valid JSON blocks, extract information using regex
    return {
        "text": response,
        "visualization_type": extract_visualization_type(response),
        "data_columns": extract_data_columns(response),
        "title": extract_title(response)
    }


def extract_json_blocks(text: str) -> List[str]:
    """
    Extract JSON blocks from text.
    
    Args:
        text: The text to extract JSON blocks from
        
    Returns:
        A list of JSON blocks
    """
    # Pattern to match JSON blocks
    pattern = r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}'
    
    # Find all matches
    matches = re.findall(pattern, text)
    
    return matches


def extract_visualization_type(text: str) -> Optional[str]:
    """
    Extract the visualization type from text.
    
    Args:
        text: The text to extract the visualization type from
        
    Returns:
        The visualization type, or None if not found
    """
    # Common visualization types
    viz_types = [
        "bar", "histogram", "scatter", "pie", "line", "heatmap",
        "bar chart", "histogram chart", "scatter plot", "pie chart", "line chart", "heatmap chart"
    ]
    
    # Check for each visualization type
    text_lower = text.lower()
    for viz_type in viz_types:
        if viz_type in text_lower:
            # Normalize to base type
            return viz_type.split()[0]
    
    return None


def extract_data_columns(text: str) -> List[str]:
    """
    Extract data columns from text.
    
    Args:
        text: The text to extract data columns from
        
    Returns:
        A list of data columns
    """
    # Common column names in the Titanic dataset
    columns = [
        "survived", "pclass", "name", "sex", "age", "sibsp",
        "parch", "ticket", "fare", "cabin", "embarked"
    ]
    
    # Check for each column
    text_lower = text.lower()
    found_columns = []
    
    for column in columns:
        if column in text_lower:
            found_columns.append(column)
    
    return found_columns


def extract_title(text: str) -> Optional[str]:
    """
    Extract a title from text.
    
    Args:
        text: The text to extract a title from
        
    Returns:
        The title, or None if not found
    """
    # Try to find a title-like sentence
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Check if line looks like a title (short, ends with no period)
        if 3 <= len(line) <= 100 and not line.endswith('.') and not line.endswith('?'):
            return line
    
    # If no good title found, use the first line
    if lines:
        return lines[0].strip()
    
    return None
