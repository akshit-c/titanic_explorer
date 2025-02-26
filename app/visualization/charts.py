import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union


def generate_visualization(
    data: Union[pd.DataFrame, Dict[str, Any]],
    visualization_type: str,
    filepath: str,
    title: str = "Titanic Data Analysis",
    color_scheme: str = "viridis",
    annotations: List[Dict[str, Any]] = None,
    **kwargs
) -> str:
    """
    Generate a visualization based on the data and type.
    
    Args:
        data: The data to visualize
        visualization_type: The type of visualization to generate
        filepath: The path to save the visualization to
        title: The title of the visualization
        color_scheme: The color scheme to use for the visualization
        annotations: List of annotations to add to the visualization
        **kwargs: Additional keyword arguments for the visualization
        
    Returns:
        The path to the saved visualization
    """
    # Convert dict to DataFrame if necessary
    if isinstance(data, dict):
        data = pd.DataFrame(data)
    
    # Set up the figure
    plt.figure(figsize=(12, 7))
    
    # Set the style
    sns.set_style("whitegrid")
    
    # Set the color palette
    sns.set_palette(color_scheme)
    
    # Generate the visualization based on the type
    if visualization_type == "bar":
        create_bar_chart(data, title, **kwargs)
    elif visualization_type == "histogram":
        create_histogram(data, title, **kwargs)
    elif visualization_type == "scatter":
        create_scatter_plot(data, title, **kwargs)
    elif visualization_type == "pie":
        create_pie_chart(data, title, **kwargs)
    elif visualization_type == "line":
        create_line_chart(data, title, **kwargs)
    elif visualization_type == "heatmap":
        create_heatmap(data, title, **kwargs)
    elif visualization_type == "box":
        create_box_plot(data, title, **kwargs)
    elif visualization_type == "grouped_bar":
        create_grouped_bar_chart(data, title, **kwargs)
    elif visualization_type == "violin":
        create_violin_plot(data, title, **kwargs)
    elif visualization_type == "count":
        create_count_plot(data, title, **kwargs)
    elif visualization_type == "kde":
        create_kde(data, title, **kwargs)
    else:
        # Default to bar chart
        create_bar_chart(data, title, **kwargs)
    
    # Add annotations if provided
    if annotations:
        for annotation in annotations:
            plt.annotate(
                annotation.get("text", ""),
                xy=(annotation.get("x", 0), annotation.get("y", 0)),
                xytext=annotation.get("xytext", (0, 10)),
                textcoords=annotation.get("textcoords", "offset points"),
                ha=annotation.get("ha", "center"),
                va=annotation.get("va", "bottom"),
                fontsize=annotation.get("fontsize", 12),
                color=annotation.get("color", "black"),
                arrowprops=annotation.get("arrowprops", dict(arrowstyle="->", color="black"))
            )
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close()
    
    return filepath


def create_bar_chart(
    data: pd.DataFrame,
    title: str,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    hue_col: Optional[str] = None,
    **kwargs
) -> None:
    """
    Create a bar chart.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        x_col: The column to use for the x-axis
        y_col: The column to use for the y-axis
        hue_col: The column to use for the hue
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine x and y columns if not provided
    if x_col is None:
        x_col = data.columns[0]
    if y_col is None:
        y_col = data.columns[1] if len(data.columns) > 1 else None
    
    # Create the bar chart
    if hue_col:
        ax = sns.barplot(x=x_col, y=y_col, hue=hue_col, data=data)
    else:
        ax = sns.barplot(x=x_col, y=y_col, data=data)
    
    # Set the title and labels
    plt.title(title, fontsize=16)
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    
    # Rotate x-axis labels if there are many categories
    if len(data[x_col].unique()) > 3:
        plt.xticks(rotation=45, ha="right")
    
    # Add value labels on top of bars
    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.1f}",
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha="center",
            va="bottom",
            fontsize=10,
            color="black",
            xytext=(0, 5),
            textcoords="offset points"
        )


def create_histogram(
    data: pd.DataFrame,
    title: str,
    x_col: Optional[str] = None,
    hue_col: Optional[str] = None,
    bins: int = 20,
    **kwargs
) -> None:
    """
    Create a histogram.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        x_col: The column to use for the x-axis
        hue_col: The column to use for the hue
        bins: The number of bins to use
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine x column if not provided
    if x_col is None:
        # If 'age' is in the columns, use it
        if 'age' in data.columns:
            x_col = 'age'
        # Otherwise use the first numeric column
        else:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                x_col = numeric_cols[0]
            else:
                x_col = data.columns[0]
    
    # Create the histogram
    if hue_col:
        # If hue is 'survived', convert to string for better legend
        if hue_col == 'survived':
            data = data.copy()
            data[hue_col] = data[hue_col].map({True: 'Survived', False: 'Did not survive'})
        
        sns.histplot(data=data, x=x_col, hue=hue_col, bins=bins, kde=True, multiple="dodge")
    else:
        sns.histplot(data=data, x=x_col, bins=bins, kde=True)
    
    # Set the title and labels
    plt.title(title, fontsize=16)
    plt.xlabel(x_col.capitalize(), fontsize=12)
    plt.ylabel("Count", fontsize=12)


def create_scatter_plot(
    data: pd.DataFrame,
    title: str,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    hue_col: Optional[str] = None,
    size_col: Optional[str] = None,
    **kwargs
) -> None:
    """
    Create a scatter plot.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        x_col: The column to use for the x-axis
        y_col: The column to use for the y-axis
        hue_col: The column to use for the hue
        size_col: The column to use for the point size
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine x and y columns if not provided
    if x_col is None:
        # If 'age' is in the columns, use it
        if 'age' in data.columns:
            x_col = 'age'
        # Otherwise use the first numeric column
        else:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                x_col = numeric_cols[0]
            else:
                x_col = data.columns[0]
    
    if y_col is None:
        # If 'fare' is in the columns, use it
        if 'fare' in data.columns:
            y_col = 'fare'
        # Otherwise use the second numeric column
        else:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                y_col = numeric_cols[1]
            else:
                y_col = data.columns[1] if len(data.columns) > 1 else x_col
    
    # Create the scatter plot
    if hue_col:
        # If hue is 'survived', convert to string for better legend
        if hue_col == 'survived':
            data = data.copy()
            data[hue_col] = data[hue_col].map({True: 'Survived', False: 'Did not survive'})
        
        if size_col:
            sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue_col, size=size_col, alpha=0.7)
        else:
            sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue_col, alpha=0.7)
    else:
        if size_col:
            sns.scatterplot(data=data, x=x_col, y=y_col, size=size_col, alpha=0.7)
        else:
            sns.scatterplot(data=data, x=x_col, y=y_col, alpha=0.7)
    
    # Set the title and labels
    plt.title(title, fontsize=16)
    plt.xlabel(x_col.capitalize(), fontsize=12)
    plt.ylabel(y_col.capitalize(), fontsize=12)


def create_pie_chart(
    data: pd.DataFrame,
    title: str,
    label_col: Optional[str] = None,
    value_col: Optional[str] = None,
    **kwargs
) -> None:
    """
    Create a pie chart.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        label_col: The column to use for the labels
        value_col: The column to use for the values
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine label and value columns if not provided
    if label_col is None:
        label_col = data.columns[0]
    if value_col is None:
        value_col = data.columns[1] if len(data.columns) > 1 else None
    
    # If value_col is None, count the occurrences of each label
    if value_col is None:
        values = data[label_col].value_counts()
        labels = values.index
    else:
        values = data[value_col]
        labels = data[label_col]
    
    # Create the pie chart
    plt.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        shadow=False,
        explode=[0.05] * len(values),
        textprops={'fontsize': 12}
    )
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    
    # Set the title
    plt.title(title, fontsize=16)


def create_line_chart(
    data: pd.DataFrame,
    title: str,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    hue_col: Optional[str] = None,
    **kwargs
) -> None:
    """
    Create a line chart.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        x_col: The column to use for the x-axis
        y_col: The column to use for the y-axis
        hue_col: The column to use for the hue
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine x and y columns if not provided
    if x_col is None:
        x_col = data.columns[0]
    if y_col is None:
        y_col = data.columns[1] if len(data.columns) > 1 else None
    
    # Create the line chart
    if hue_col:
        sns.lineplot(data=data, x=x_col, y=y_col, hue=hue_col, marker='o')
    else:
        sns.lineplot(data=data, x=x_col, y=y_col, marker='o')
    
    # Set the title and labels
    plt.title(title, fontsize=16)
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    
    # Rotate x-axis labels if there are many categories
    if len(data[x_col].unique()) > 3:
        plt.xticks(rotation=45, ha="right")


def create_heatmap(
    data: pd.DataFrame,
    title: str,
    **kwargs
) -> None:
    """
    Create a heatmap.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        **kwargs: Additional keyword arguments for the visualization
    """
    # Create the heatmap
    sns.heatmap(data, annot=True, cmap="YlGnBu", fmt=".1f", linewidths=.5)
    
    # Set the title
    plt.title(title, fontsize=16)


def create_box_plot(
    data: pd.DataFrame,
    title: str,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    hue_col: Optional[str] = None,
    **kwargs
) -> None:
    """
    Create a box plot.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        x_col: The column to use for the x-axis
        y_col: The column to use for the y-axis
        hue_col: The column to use for the hue
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine x and y columns if not provided
    if x_col is None and y_col is None:
        # If 'survived' is in the columns, use it as x
        if 'survived' in data.columns:
            x_col = 'survived'
            # If 'fare' is in the columns, use it as y
            if 'fare' in data.columns:
                y_col = 'fare'
            # Otherwise use the first numeric column as y
            else:
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    y_col = numeric_cols[0]
                else:
                    y_col = data.columns[0]
        else:
            x_col = data.columns[0]
            y_col = data.columns[1] if len(data.columns) > 1 else None
    
    # If x_col is 'survived', convert to string for better labels
    if x_col == 'survived':
        data = data.copy()
        data[x_col] = data[x_col].map({True: 'Survived', False: 'Did not survive'})
    
    # Create the box plot
    if hue_col:
        sns.boxplot(data=data, x=x_col, y=y_col, hue=hue_col)
    else:
        sns.boxplot(data=data, x=x_col, y=y_col)
    
    # Set the title and labels
    plt.title(title, fontsize=16)
    if x_col:
        plt.xlabel(x_col.capitalize(), fontsize=12)
    if y_col:
        plt.ylabel(y_col.capitalize(), fontsize=12)


def create_grouped_bar_chart(
    data: pd.DataFrame,
    title: str,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    hue_col: Optional[str] = None,
    **kwargs
) -> None:
    """
    Create a grouped bar chart.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        x_col: The column to use for the x-axis
        y_col: The column to use for the y-axis
        hue_col: The column to use for the hue
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine x and y columns if not provided
    if x_col is None:
        x_col = data.columns[0]
    if y_col is None:
        y_col = data.columns[1] if len(data.columns) > 1 else None
    if hue_col is None and len(data.columns) > 2:
        hue_col = data.columns[2]
    
    # Create the grouped bar chart
    ax = sns.catplot(
        data=data, 
        x=x_col, 
        y=y_col, 
        hue=hue_col, 
        kind="bar",
        height=6, 
        aspect=1.5,
        palette=kwargs.get("palette", "viridis")
    )
    
    # Set the title and labels
    ax.fig.suptitle(title, fontsize=16)
    ax.set_xlabels(x_col, fontsize=12)
    ax.set_ylabels(y_col, fontsize=12)
    
    # Rotate x-axis labels if there are many categories
    if len(data[x_col].unique()) > 3:
        plt.xticks(rotation=45, ha="right")


def create_violin_plot(
    data: pd.DataFrame,
    title: str,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    hue_col: Optional[str] = None,
    **kwargs
) -> None:
    """
    Create a violin plot.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        x_col: The column to use for the x-axis
        y_col: The column to use for the y-axis
        hue_col: The column to use for the hue
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine x and y columns if not provided
    if x_col is None:
        # If 'survived' is in the columns, use it
        if 'survived' in data.columns:
            x_col = 'survived'
        else:
            categorical_cols = data.select_dtypes(include=['object', 'category', 'bool']).columns
            if len(categorical_cols) > 0:
                x_col = categorical_cols[0]
            else:
                x_col = data.columns[0]
    
    if y_col is None:
        # If 'fare' is in the columns and the title contains 'fare', use it
        if 'fare' in data.columns and 'fare' in title.lower():
            y_col = 'fare'
        # If 'age' is in the columns, use it
        elif 'age' in data.columns:
            y_col = 'age'
        else:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                y_col = numeric_cols[0]
            else:
                y_col = data.columns[1] if len(data.columns) > 1 else data.columns[0]
    
    # If x_col is 'survived', convert to string for better legend
    if x_col == 'survived':
        data = data.copy()
        data[x_col] = data[x_col].map({True: 'Survived', False: 'Did not survive'})
    
    # Create the violin plot
    if hue_col:
        sns.violinplot(data=data, x=x_col, y=y_col, hue=hue_col, split=True, inner="quart", palette="viridis")
    else:
        sns.violinplot(data=data, x=x_col, y=y_col, inner="quart", palette="viridis")
    
    # Set the title and labels
    plt.title(title, fontsize=16)
    plt.xlabel(x_col.capitalize(), fontsize=12)
    plt.ylabel(y_col.capitalize(), fontsize=12)
    
    # Add a grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)


def create_count_plot(
    data: pd.DataFrame,
    title: str,
    x_col: Optional[str] = None,
    hue_col: Optional[str] = None,
    **kwargs
) -> None:
    """
    Create a count plot.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        x_col: The column to use for the x-axis
        hue_col: The column to use for the hue
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine x column if not provided
    if x_col is None:
        # If 'survived' is in the columns, use it
        if 'survived' in data.columns:
            x_col = 'survived'
        else:
            categorical_cols = data.select_dtypes(include=['object', 'category', 'bool']).columns
            if len(categorical_cols) > 0:
                x_col = categorical_cols[0]
            else:
                x_col = data.columns[0]
    
    # Create the count plot
    if hue_col:
        # If hue is 'survived', convert to string for better legend
        if hue_col == 'survived':
            data = data.copy()
            data[hue_col] = data[hue_col].map({True: 'Survived', False: 'Did not survive'})
        
        ax = sns.countplot(
            data=data, 
            x=x_col, 
            hue=hue_col,
            palette=kwargs.get("palette", "viridis")
        )
    else:
        ax = sns.countplot(
            data=data, 
            x=x_col,
            palette=kwargs.get("palette", "viridis")
        )
    
    # Set the title and labels
    plt.title(title, fontsize=16)
    plt.xlabel(x_col.capitalize(), fontsize=12)
    plt.ylabel("Count", fontsize=12)
    
    # Add value labels on top of bars
    for p in ax.patches:
        ax.annotate(
            f"{int(p.get_height())}",
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha="center",
            va="bottom",
            fontsize=10,
            color="black",
            xytext=(0, 5),
            textcoords="offset points"
        )


def create_kde(
    data: pd.DataFrame,
    title: str,
    x_col: Optional[str] = None,
    hue_col: Optional[str] = None,
    fill: bool = True,
    **kwargs
) -> None:
    """
    Create a KDE (Kernel Density Estimation) plot.
    
    Args:
        data: The data to visualize
        title: The title of the visualization
        x_col: The column to use for the x-axis
        hue_col: The column to use for the hue
        fill: Whether to fill the area under the KDE curve
        **kwargs: Additional keyword arguments for the visualization
    """
    # Determine x column if not provided
    if x_col is None:
        # If 'fare' is in the columns, use it
        if 'fare' in data.columns:
            x_col = 'fare'
        # Otherwise use the first numeric column
        else:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                x_col = numeric_cols[0]
            else:
                x_col = data.columns[0]
    
    # Create the KDE plot
    if hue_col:
        # If hue is 'survived', convert to string for better legend
        if hue_col == 'survived':
            data = data.copy()
            data[hue_col] = data[hue_col].map({True: 'Survived', False: 'Did not survive'})
        
        sns.kdeplot(data=data, x=x_col, hue=hue_col, fill=fill, common_norm=False, palette="viridis")
    else:
        sns.kdeplot(data=data, x=x_col, fill=fill, color="royalblue")
    
    # Set the title and labels
    plt.title(title, fontsize=16)
    plt.xlabel(x_col.capitalize(), fontsize=12)
    plt.ylabel("Density", fontsize=12)
    
    # Add a grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)
