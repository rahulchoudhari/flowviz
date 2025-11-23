# FlowViz - Modular Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         app.py                                   │
│                   (Main Streamlit App)                           │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Login Page   │  │  Home Page   │  │ Sidebar Nav  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │ Data Visualization   │  │ Month Comparison     │            │
│  │       Page           │  │       Page           │            │
│  └──────────────────────┘  └──────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ imports
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    helpers/ (Modular Scripts)                    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  datetime_utils.py                                       │   │
│  │  • detect_datetime_format()                              │   │
│  │  • parse_datetime_column()                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ▲                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ml_analysis.py                                          │   │
│  │  • analyze_data_with_ml()                                │   │
│  │  • get_data_statistics()                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ▲                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  visualizations.py                                       │   │
│  │  • create_visualization()                                │   │
│  │  • create_time_series()                                  │   │
│  │  • create_heatmap()                                      │   │
│  │  • create_distribution()                                 │   │
│  │  • create_category_analysis()                            │   │
│  │  • create_top_n()                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  comparison.py                                           │   │
│  │  • calculate_comparison_summary()                        │   │
│  │  • calculate_overall_change()                            │   │
│  │  • calculate_average_difference()                        │   │
│  │  • create_comparison_chart()                             │   │
│  │  • calculate_metric_change()                             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Upload CSV/Excel
        │
        ▼
┌─────────────────┐
│  Data Loading   │
│   (app.py)      │
└─────────────────┘
        │
        ▼
┌─────────────────────────┐
│  ML Analysis            │
│  (ml_analysis.py)       │
│  - Analyze columns      │
│  - Detect date cols     │◄─────── datetime_utils.py
│  - Generate recs        │
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│  Create Visualizations  │
│  (visualizations.py)    │
│  - Time series          │
│  - Heatmaps            │
│  - Distributions        │
│  - Category analysis    │
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│  Display to User        │
│  (Streamlit UI)         │
└─────────────────────────┘
```

## Month Comparison Flow

```
User Uploads Current + Previous
        │
        ▼
┌──────────────────────────┐
│  Calculate Summary       │
│  (comparison.py)         │
│  - Find common columns   │
│  - Calculate changes     │
└──────────────────────────┘
        │
        ▼
┌──────────────────────────┐
│  Create Comparison       │
│  Charts                  │
│  (comparison.py)         │
└──────────────────────────┘
        │
        ▼
┌──────────────────────────┐
│  Display Results         │
│  (Streamlit UI)          │
└──────────────────────────┘
```

## Module Dependencies

```
app.py
  ├── helpers.datetime_utils
  ├── helpers.ml_analysis
  │     └── helpers.datetime_utils (internal)
  ├── helpers.visualizations
  │     └── helpers.datetime_utils (internal)
  └── helpers.comparison
```

## Key Benefits

### 🎯 Separation of Concerns
- **UI Layer** (app.py) - Handles user interaction
- **Analysis Layer** (ml_analysis.py) - Business logic
- **Visualization Layer** (visualizations.py) - Chart generation
- **Utility Layer** (datetime_utils.py, comparison.py) - Reusable functions

### 🔧 Easy Modification
To modify a feature, only edit its helper module:
- Change date parsing → Edit `datetime_utils.py`
- Add chart type → Edit `visualizations.py`
- New ML algorithm → Edit `ml_analysis.py`
- Comparison logic → Edit `comparison.py`

### ✅ Testability
Each module can be tested independently:
```python
# Test datetime_utils
def test_detect_format():
    series = pd.Series(['2025-01-01', '2025-01-02'])
    assert detect_datetime_format(series) == '%Y-%m-%d'

# Test ml_analysis
def test_recommendations():
    df = create_test_dataframe()
    recs = analyze_data_with_ml(df)
    assert len(recs) > 0
```

### 🚀 Scalability
Add new features without touching existing code:
```python
# New module: helpers/forecasting.py
def predict_next_month(df, metric):
    """Use ML to forecast next month's values"""
    # Implementation
    pass
```

## File Structure

```
flowviz/
├── app.py                 ← Main application (uses helpers)
├── helpers/               ← Modular helper scripts
│   ├── __init__.py       ← Package initialization
│   ├── datetime_utils.py ← Date/time utilities
│   ├── ml_analysis.py    ← ML analysis
│   ├── visualizations.py ← Chart creation
│   ├── comparison.py     ← Comparison logic
│   └── README.md         ← Helper documentation
├── requirements.txt
└── REFACTORING_SUMMARY.md
```

## Import Pattern

```python
# Clean imports at top of app.py
from helpers.datetime_utils import detect_datetime_format
from helpers.ml_analysis import analyze_data_with_ml, get_data_statistics
from helpers.visualizations import create_visualization
from helpers.comparison import (
    calculate_comparison_summary,
    calculate_overall_change,
    calculate_average_difference,
    create_comparison_chart,
    calculate_metric_change
)

# Use throughout the application
stats = get_data_statistics(df)
recommendations = analyze_data_with_ml(df)
fig = create_visualization(df, recommendations[0])
```
