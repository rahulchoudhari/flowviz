"""
Custom chart builder for FlowViz
Allows users to create custom visualizations by selecting columns and chart types
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def get_column_types(df: pd.DataFrame) -> dict:
    """
    Categorize columns by data type.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with categorized columns
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Try to detect date columns
    date_cols = []
    for col in categorical_cols:
        try:
            pd.to_datetime(df[col], errors='raise')
            date_cols.append(col)
        except:
            pass
    
    # Remove date columns from categorical
    categorical_cols = [col for col in categorical_cols if col not in date_cols]
    
    return {
        'numeric': numeric_cols,
        'categorical': categorical_cols,
        'date': date_cols
    }


def create_custom_line_chart(df: pd.DataFrame, x_col: str, y_cols: list, title: str = None) -> go.Figure:
    """Create custom line chart."""
    fig = go.Figure()
    
    for y_col in y_cols:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            name=y_col
        ))
    
    fig.update_layout(
        title=title or f'{", ".join(y_cols)} over {x_col}',
        xaxis_title=x_col,
        yaxis_title='Values',
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_custom_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, 
                            orientation: str = 'v', title: str = None) -> go.Figure:
    """Create custom bar chart."""
    # Aggregate if needed
    if df[x_col].dtype == 'object' or df[x_col].dtype.name == 'category':
        grouped = df.groupby(x_col)[y_col].sum().reset_index()
    else:
        grouped = df[[x_col, y_col]]
    
    if orientation == 'h':
        grouped = grouped.sort_values(y_col, ascending=True)
        fig = go.Figure(go.Bar(
            y=grouped[x_col],
            x=grouped[y_col],
            orientation='h',
            marker_color='#10b981'
        ))
    else:
        fig = go.Figure(go.Bar(
            x=grouped[x_col],
            y=grouped[y_col],
            marker_color='#06b6d4'
        ))
    
    fig.update_layout(
        title=title or f'{y_col} by {x_col}',
        xaxis_title=x_col if orientation == 'v' else y_col,
        yaxis_title=y_col if orientation == 'v' else x_col,
        template='plotly_white'
    )
    
    return fig


def create_custom_scatter(df: pd.DataFrame, x_col: str, y_col: str, 
                         color_col: str = None, size_col: str = None, 
                         title: str = None) -> go.Figure:
    """Create custom scatter plot."""
    if color_col:
        fig = px.scatter(
            df, x=x_col, y=y_col, color=color_col,
            size=size_col if size_col else None,
            title=title or f'{y_col} vs {x_col}',
            template='plotly_white'
        )
    else:
        fig = go.Figure(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(
                size=df[size_col] if size_col else 8,
                color='#8b5cf6'
            )
        ))
        
        fig.update_layout(
            title=title or f'{y_col} vs {x_col}',
            xaxis_title=x_col,
            yaxis_title=y_col,
            template='plotly_white'
        )
    
    return fig


def create_custom_pie_chart(df: pd.DataFrame, names_col: str, values_col: str, 
                            title: str = None) -> go.Figure:
    """Create custom pie chart."""
    grouped = df.groupby(names_col)[values_col].sum().reset_index()
    
    fig = go.Figure(go.Pie(
        labels=grouped[names_col],
        values=grouped[values_col],
        hole=0.3,
        textinfo='label+percent'
    ))
    
    fig.update_layout(
        title=title or f'{values_col} by {names_col}',
        template='plotly_white'
    )
    
    return fig


def create_custom_box_plot(df: pd.DataFrame, category_col: str, value_col: str,
                           title: str = None) -> go.Figure:
    """Create custom box plot."""
    fig = go.Figure()
    
    for category in df[category_col].unique():
        data = df[df[category_col] == category][value_col]
        fig.add_trace(go.Box(
            y=data,
            name=str(category)
        ))
    
    fig.update_layout(
        title=title or f'{value_col} distribution by {category_col}',
        yaxis_title=value_col,
        xaxis_title=category_col,
        template='plotly_white'
    )
    
    return fig


def create_custom_heatmap(df: pd.DataFrame, columns: list, title: str = None) -> go.Figure:
    """Create custom correlation heatmap."""
    corr_matrix = df[columns].corr()
    
    fig = go.Figure(go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu_r',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title=title or 'Correlation Heatmap',
        template='plotly_white',
        xaxis=dict(side='bottom')
    )
    
    return fig


def create_custom_area_chart(df: pd.DataFrame, x_col: str, y_cols: list, 
                             title: str = None) -> go.Figure:
    """Create custom area chart."""
    fig = go.Figure()
    
    for y_col in y_cols:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines',
            name=y_col,
            fill='tonexty' if len(fig.data) > 0 else 'tozeroy',
            stackgroup='one'
        ))
    
    fig.update_layout(
        title=title or f'Stacked Area: {", ".join(y_cols)}',
        xaxis_title=x_col,
        yaxis_title='Values',
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_custom_histogram(df: pd.DataFrame, column: str, bins: int = 30,
                            title: str = None) -> go.Figure:
    """Create custom histogram."""
    fig = go.Figure(go.Histogram(
        x=df[column],
        nbinsx=bins,
        marker_color='#10b981'
    ))
    
    fig.update_layout(
        title=title or f'Distribution of {column}',
        xaxis_title=column,
        yaxis_title='Frequency',
        template='plotly_white'
    )
    
    return fig
