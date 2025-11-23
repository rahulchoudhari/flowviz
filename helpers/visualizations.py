"""
Visualization creation functions for FlowViz
Creates different types of charts based on recommendations
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .datetime_utils import parse_datetime_column


def create_visualization(df: pd.DataFrame, recommendation: dict):
    """
    Create visualization based on ML recommendation.
    
    Args:
        df: DataFrame containing the data
        recommendation: Dictionary with visualization parameters
        
    Returns:
        Plotly figure object
    """
    fig = None
    
    if recommendation['type'] == 'time_series':
        fig = create_time_series(df, recommendation)
    
    elif recommendation['type'] == 'heatmap':
        fig = create_heatmap(df, recommendation)
    
    elif recommendation['type'] == 'distribution':
        fig = create_distribution(df, recommendation)
    
    elif recommendation['type'] == 'category_analysis':
        fig = create_category_analysis(df, recommendation)
    
    elif recommendation['type'] == 'top_n':
        fig = create_top_n(df, recommendation)
    
    return fig


def create_time_series(df: pd.DataFrame, recommendation: dict):
    """Create time series line chart."""
    df_copy = df.copy()
    date_format = recommendation.get('date_format')
    
    df_copy[recommendation['x']] = parse_datetime_column(
        df_copy, 
        recommendation['x'], 
        date_format
    )
    df_sorted = df_copy.sort_values(recommendation['x'])
    
    fig = go.Figure()
    for y_col in recommendation['y']:
        if y_col in df_sorted.columns:
            fig.add_trace(go.Scatter(
                x=df_sorted[recommendation['x']],
                y=df_sorted[y_col],
                mode='lines+markers',
                name=y_col
            ))
    
    fig.update_layout(
        title=recommendation['title'],
        xaxis_title=recommendation['x'],
        yaxis_title='Values',
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def create_heatmap(df: pd.DataFrame, recommendation: dict):
    """Create correlation heatmap."""
    corr_matrix = df[recommendation['columns']].corr()
    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        color_continuous_scale='RdBu_r',
        aspect='auto',
        title=recommendation['title']
    )
    return fig


def create_distribution(df: pd.DataFrame, recommendation: dict):
    """Create distribution histogram."""
    fig = go.Figure()
    for col in recommendation['columns']:
        fig.add_trace(go.Histogram(
            x=df[col],
            name=col,
            opacity=0.7
        ))
    
    fig.update_layout(
        title=recommendation['title'],
        xaxis_title='Value',
        yaxis_title='Frequency',
        barmode='overlay',
        template='plotly_white'
    )
    
    return fig


def create_category_analysis(df: pd.DataFrame, recommendation: dict):
    """Create category analysis bar chart."""
    grouped = df.groupby(recommendation['category'])[recommendation['values']].mean().reset_index()
    
    fig = go.Figure()
    for val_col in recommendation['values']:
        if val_col in grouped.columns:
            fig.add_trace(go.Bar(
                x=grouped[recommendation['category']],
                y=grouped[val_col],
                name=val_col
            ))
    
    fig.update_layout(
        title=recommendation['title'],
        xaxis_title=recommendation['category'],
        yaxis_title='Average Value',
        template='plotly_white'
    )
    
    return fig


def create_top_n(df: pd.DataFrame, recommendation: dict):
    """Create top N horizontal bar chart."""
    top_data = df.nlargest(10, recommendation['value'])[[recommendation['category'], recommendation['value']]]
    
    fig = px.bar(
        top_data,
        x=recommendation['value'],
        y=recommendation['category'],
        orientation='h',
        title=recommendation['title'],
        template='plotly_white'
    )
    
    return fig
