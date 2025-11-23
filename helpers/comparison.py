"""
Comparison analysis functions for FlowViz
Handles month-over-month data comparison
"""

import pandas as pd
import numpy as np
import plotly.express as px


def calculate_comparison_summary(current_df: pd.DataFrame, previous_df: pd.DataFrame) -> tuple[list, pd.DataFrame]:
    """
    Calculate comparison summary between current and previous data.
    
    Args:
        current_df: Current month DataFrame
        previous_df: Previous month DataFrame
        
    Returns:
        Tuple of (common_numeric_columns, summary_dataframe)
    """
    # Find common numeric columns
    current_numeric = set(current_df.select_dtypes(include=[np.number]).columns)
    previous_numeric = set(previous_df.select_dtypes(include=[np.number]).columns)
    common_numeric = list(current_numeric.intersection(previous_numeric))
    
    if not common_numeric:
        return [], pd.DataFrame()
    
    # Create summary dataframe
    summary = pd.DataFrame({
        'Metric': common_numeric,
        'Previous Month': [previous_df[col].sum() for col in common_numeric],
        'Current Month': [current_df[col].sum() for col in common_numeric],
    })
    summary['Change (%)'] = (
        (summary['Current Month'] - summary['Previous Month']) / 
        summary['Previous Month'] * 100
    ).round(2)
    
    return common_numeric, summary


def calculate_overall_change(current_df: pd.DataFrame, previous_df: pd.DataFrame, common_numeric: list) -> float:
    """
    Calculate overall percentage change across all metrics.
    
    Args:
        current_df: Current month DataFrame
        previous_df: Previous month DataFrame
        common_numeric: List of common numeric columns
        
    Returns:
        Overall change percentage
    """
    current_total = current_df[common_numeric].sum().sum()
    previous_total = previous_df[common_numeric].sum().sum()
    
    if previous_total != 0:
        return ((current_total - previous_total) / previous_total * 100)
    return 0


def calculate_average_difference(current_df: pd.DataFrame, previous_df: pd.DataFrame, common_numeric: list) -> float:
    """
    Calculate average difference across all metrics.
    
    Args:
        current_df: Current month DataFrame
        previous_df: Previous month DataFrame
        common_numeric: List of common numeric columns
        
    Returns:
        Average difference value
    """
    avg_change = (
        current_df[common_numeric].mean().mean() - 
        previous_df[common_numeric].mean().mean()
    )
    return avg_change


def create_comparison_chart(current_df: pd.DataFrame, previous_df: pd.DataFrame, column: str):
    """
    Create a comparison bar chart for a specific column.
    
    Args:
        current_df: Current month DataFrame
        previous_df: Previous month DataFrame
        column: Column name to compare
        
    Returns:
        Plotly figure object
    """
    comparison_data = pd.DataFrame({
        'Period': ['Previous Month', 'Current Month'],
        column: [previous_df[column].sum(), current_df[column].sum()]
    })
    
    fig = px.bar(
        comparison_data,
        x='Period',
        y=column,
        title=f'{column} - Month over Month',
        template='plotly_white',
        color='Period',
        color_discrete_sequence=['#764ba2', '#667eea']
    )
    
    return fig


def calculate_metric_change(current_df: pd.DataFrame, previous_df: pd.DataFrame, column: str) -> float:
    """
    Calculate percentage change for a specific metric.
    
    Args:
        current_df: Current month DataFrame
        previous_df: Previous month DataFrame
        column: Column name to calculate change for
        
    Returns:
        Percentage change
    """
    current_sum = current_df[column].sum()
    previous_sum = previous_df[column].sum()
    
    if previous_sum != 0:
        return ((current_sum - previous_sum) / previous_sum * 100)
    return 0
