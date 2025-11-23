"""
FlowViz Helper Modules
Modular utilities for industrial data analysis
"""

from .datetime_utils import detect_datetime_format
from .ml_analysis import analyze_data_with_ml
from .visualizations import create_visualization
from .comparison import create_comparison_chart, calculate_comparison_summary
from .ceo_dashboard import (
    create_kpi_cards,
    create_revenue_trend,
    create_regional_performance,
    create_product_mix,
    create_efficiency_metrics,
    create_promotion_impact,
    create_top_products
)
from .custom_charts import (
    get_column_types,
    create_custom_line_chart,
    create_custom_bar_chart,
    create_custom_scatter,
    create_custom_pie_chart,
    create_custom_box_plot,
    create_custom_heatmap,
    create_custom_area_chart,
    create_custom_histogram
)

__all__ = [
    'detect_datetime_format',
    'analyze_data_with_ml',
    'create_visualization',
    'create_comparison_chart',
    'calculate_comparison_summary',
    'create_kpi_cards',
    'create_revenue_trend',
    'create_regional_performance',
    'create_product_mix',
    'create_efficiency_metrics',
    'create_promotion_impact',
    'create_top_products',
    'get_column_types',
    'create_custom_line_chart',
    'create_custom_bar_chart',
    'create_custom_scatter',
    'create_custom_pie_chart',
    'create_custom_box_plot',
    'create_custom_heatmap',
    'create_custom_area_chart',
    'create_custom_histogram'
]
