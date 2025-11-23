"""
CEO Dashboard visualizations for FlowViz
High-level business metrics and KPIs
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def create_kpi_cards(df: pd.DataFrame) -> dict:
    """
    Calculate key business KPIs.
    
    Args:
        df: DataFrame with business data
        
    Returns:
        Dictionary of KPIs
    """
    kpis = {}
    
    # Revenue metrics
    if 'Sales_Amount' in df.columns:
        kpis['total_revenue'] = df['Sales_Amount'].sum()
        kpis['avg_transaction'] = df['Sales_Amount'].mean()
    
    # Volume metrics
    if 'Quantity_Sold' in df.columns:
        kpis['total_units'] = df['Quantity_Sold'].sum()
        kpis['avg_units_per_transaction'] = df['Quantity_Sold'].mean()
    
    # Efficiency metrics
    if 'Manpower_Hours' in df.columns and 'Sales_Amount' in df.columns:
        kpis['revenue_per_hour'] = df['Sales_Amount'].sum() / df['Manpower_Hours'].sum()
    
    if 'kWh_Used' in df.columns and 'Sales_Amount' in df.columns:
        kpis['revenue_per_kwh'] = df['Sales_Amount'].sum() / df['kWh_Used'].sum()
    
    # Transaction count
    kpis['total_transactions'] = len(df)
    
    return kpis


def create_revenue_trend(df: pd.DataFrame, date_col: str = 'Date') -> go.Figure:
    """Create revenue trend over time."""
    if date_col not in df.columns or 'Sales_Amount' not in df.columns:
        return None
    
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
    df_sorted = df_copy.sort_values(date_col)
    
    # Daily revenue
    daily_revenue = df_sorted.groupby(date_col)['Sales_Amount'].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_revenue[date_col],
        y=daily_revenue['Sales_Amount'],
        mode='lines+markers',
        name='Daily Revenue',
        line=dict(color='#10b981', width=3),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.1)'
    ))
    
    fig.update_layout(
        title='Revenue Trend',
        xaxis_title='Date',
        yaxis_title='Revenue ($)',
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_regional_performance(df: pd.DataFrame) -> go.Figure:
    """Create regional performance comparison."""
    if 'Region' not in df.columns or 'Sales_Amount' not in df.columns:
        return None
    
    regional_sales = df.groupby('Region')['Sales_Amount'].sum().reset_index()
    regional_sales = regional_sales.sort_values('Sales_Amount', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=regional_sales['Region'],
        x=regional_sales['Sales_Amount'],
        orientation='h',
        marker=dict(
            color=regional_sales['Sales_Amount'],
            colorscale='Viridis',
            showscale=True
        ),
        text=regional_sales['Sales_Amount'].apply(lambda x: f'${x:,.0f}'),
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Regional Sales Performance',
        xaxis_title='Total Sales ($)',
        yaxis_title='Region',
        template='plotly_white'
    )
    
    return fig


def create_product_mix(df: pd.DataFrame) -> go.Figure:
    """Create product category mix pie chart."""
    if 'Product_Category' not in df.columns or 'Sales_Amount' not in df.columns:
        return None
    
    category_sales = df.groupby('Product_Category')['Sales_Amount'].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=category_sales['Product_Category'],
        values=category_sales['Sales_Amount'],
        hole=0.4,
        marker=dict(colors=px.colors.qualitative.Set3),
        textinfo='label+percent',
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Revenue by Product Category',
        template='plotly_white'
    )
    
    return fig


def create_efficiency_metrics(df: pd.DataFrame) -> go.Figure:
    """Create resource efficiency visualization."""
    if 'Store_Type' not in df.columns:
        return None
    
    metrics = []
    store_types = df['Store_Type'].unique()
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Revenue per Hour', 'Revenue per kWh', 'Avg Transaction Value'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]]
    )
    
    if 'Manpower_Hours' in df.columns and 'Sales_Amount' in df.columns:
        efficiency = df.groupby('Store_Type').apply(
            lambda x: x['Sales_Amount'].sum() / x['Manpower_Hours'].sum()
        ).reset_index(name='Revenue_per_Hour')
        
        fig.add_trace(
            go.Bar(x=efficiency['Store_Type'], y=efficiency['Revenue_per_Hour'], 
                   marker_color='#10b981', name='$/Hour'),
            row=1, col=1
        )
    
    if 'kWh_Used' in df.columns and 'Sales_Amount' in df.columns:
        energy_eff = df.groupby('Store_Type').apply(
            lambda x: x['Sales_Amount'].sum() / x['kWh_Used'].sum()
        ).reset_index(name='Revenue_per_kWh')
        
        fig.add_trace(
            go.Bar(x=energy_eff['Store_Type'], y=energy_eff['Revenue_per_kWh'],
                   marker_color='#06b6d4', name='$/kWh'),
            row=1, col=2
        )
    
    if 'Sales_Amount' in df.columns:
        avg_transaction = df.groupby('Store_Type')['Sales_Amount'].mean().reset_index()
        
        fig.add_trace(
            go.Bar(x=avg_transaction['Store_Type'], y=avg_transaction['Sales_Amount'],
                   marker_color='#8b5cf6', name='Avg $'),
            row=1, col=3
        )
    
    fig.update_layout(
        title_text='Operational Efficiency by Store Type',
        showlegend=False,
        template='plotly_white',
        height=400
    )
    
    return fig


def create_promotion_impact(df: pd.DataFrame) -> go.Figure:
    """Analyze promotion impact on sales."""
    if 'Promotion_Flag' not in df.columns or 'Sales_Amount' not in df.columns:
        return None
    
    promo_sales = df.groupby('Promotion_Flag')['Sales_Amount'].agg(['sum', 'mean', 'count']).reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Total Sales', 'Average Transaction Value'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}]]
    )
    
    fig.add_trace(
        go.Bar(x=promo_sales['Promotion_Flag'], y=promo_sales['sum'],
               marker_color=['#ef4444', '#10b981'], name='Total Sales',
               text=promo_sales['sum'].apply(lambda x: f'${x:,.0f}'),
               textposition='auto'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=promo_sales['Promotion_Flag'], y=promo_sales['mean'],
               marker_color=['#f59e0b', '#06b6d4'], name='Avg Transaction',
               text=promo_sales['mean'].apply(lambda x: f'${x:.2f}'),
               textposition='auto'),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text='Promotion Impact Analysis',
        showlegend=False,
        template='plotly_white',
        height=400
    )
    
    return fig


def create_top_products(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Show top performing products."""
    if 'Product_Name' not in df.columns or 'Sales_Amount' not in df.columns:
        return None
    
    top_products = df.groupby('Product_Name')['Sales_Amount'].sum().nlargest(top_n).reset_index()
    top_products = top_products.sort_values('Sales_Amount', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_products['Product_Name'],
        x=top_products['Sales_Amount'],
        orientation='h',
        marker=dict(
            color=top_products['Sales_Amount'],
            colorscale='Blues',
            showscale=False
        ),
        text=top_products['Sales_Amount'].apply(lambda x: f'${x:,.0f}'),
        textposition='auto'
    ))
    
    fig.update_layout(
        title=f'Top {top_n} Products by Revenue',
        xaxis_title='Total Revenue ($)',
        yaxis_title='Product',
        template='plotly_white',
        height=500
    )
    
    return fig
