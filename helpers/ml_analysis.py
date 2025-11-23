"""
Machine Learning analysis functions for FlowViz
Analyzes data and recommends optimal visualizations
"""

import pandas as pd
import numpy as np
from .datetime_utils import detect_datetime_format, parse_datetime_column


def analyze_data_with_ml(df: pd.DataFrame) -> list[dict]:
    """
    Use ML to determine best visualizations for the data.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        List of visualization recommendations sorted by priority
    """
    recommendations = []
    
    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Date columns detection
    date_cols = []
    date_formats = {}
    for col in df.columns:
        if df[col].dtype == 'object':
            fmt = detect_datetime_format(df[col])
            if fmt:
                parsed = parse_datetime_column(df, col, fmt)
            else:
                parsed = parse_datetime_column(df, col)

            if parsed.notna().any():
                date_cols.append(col)
                date_formats[col] = fmt
    
    # Recommendation 1: Time series if date column exists
    if date_cols and numeric_cols:
        recommendations.append({
            'type': 'time_series',
            'x': date_cols[0],
            'y': numeric_cols[:3],  # Top 3 numeric columns
            'title': f'Time Series Analysis',
            'date_format': date_formats.get(date_cols[0]),
            'priority': 1
        })
    
    # Recommendation 2: Correlation heatmap for numeric data
    if len(numeric_cols) >= 2:
        recommendations.append({
            'type': 'heatmap',
            'columns': numeric_cols[:10],  # Max 10 columns for readability
            'title': 'Correlation Heatmap',
            'priority': 2
        })
    
    # Recommendation 3: Distribution plots for numeric columns
    if numeric_cols:
        # Use variance to identify most interesting columns
        variances = df[numeric_cols].var().sort_values(ascending=False)
        top_cols = variances.head(3).index.tolist()
        recommendations.append({
            'type': 'distribution',
            'columns': top_cols,
            'title': 'Distribution Analysis',
            'priority': 3
        })
    
    # Recommendation 4: Category analysis
    if categorical_cols and numeric_cols:
        # Find categorical column with reasonable number of unique values
        for cat_col in categorical_cols:
            if 2 <= df[cat_col].nunique() <= 20:
                recommendations.append({
                    'type': 'category_analysis',
                    'category': cat_col,
                    'values': numeric_cols[:2],
                    'title': f'Analysis by {cat_col}',
                    'priority': 4
                })
                break
    
    # Recommendation 5: Top N analysis
    if categorical_cols and numeric_cols:
        recommendations.append({
            'type': 'top_n',
            'category': categorical_cols[0],
            'value': numeric_cols[0],
            'title': f'Top 10 by {numeric_cols[0]}',
            'priority': 5
        })
    
    return sorted(recommendations, key=lambda x: x['priority'])


def get_data_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate basic statistics for the dataframe.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary containing statistics
    """
    numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
    categorical_cols = len(df.select_dtypes(include=['object']).columns)
    
    return {
        'total_rows': df.shape[0],
        'total_columns': df.shape[1],
        'numeric_columns': numeric_cols,
        'categorical_columns': categorical_cols
    }
