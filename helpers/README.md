# FlowViz Helper Modules

This directory contains modular helper scripts that separate functionality into maintainable, reusable components.

## Module Structure

### 📅 `datetime_utils.py`
**Purpose:** Date and time parsing utilities

**Functions:**
- `detect_datetime_format(series)` - Automatically detect datetime format in a pandas Series
- `parse_datetime_column(df, col, date_format)` - Parse datetime column with optional format specification

**Use Case:** Prevents pandas datetime parsing warnings by detecting format first

---

### 🤖 `ml_analysis.py`
**Purpose:** Machine learning-based data analysis and visualization recommendations

**Functions:**
- `analyze_data_with_ml(df)` - Analyzes DataFrame and recommends optimal visualizations
- `get_data_statistics(df)` - Calculates basic statistics (row count, column types, etc.)

**Use Case:** Automatically determines which charts to show based on data characteristics

---

### 📊 `visualizations.py`
**Purpose:** Chart creation functions for different visualization types

**Functions:**
- `create_visualization(df, recommendation)` - Main dispatcher for creating charts
- `create_time_series(df, recommendation)` - Time series line charts
- `create_heatmap(df, recommendation)` - Correlation heatmaps
- `create_distribution(df, recommendation)` - Distribution histograms
- `create_category_analysis(df, recommendation)` - Category-based bar charts
- `create_top_n(df, recommendation)` - Top N horizontal bar charts

**Use Case:** Modular chart generation - modify one chart type without affecting others

---

### 📈 `comparison.py`
**Purpose:** Month-over-month comparison analysis

**Functions:**
- `calculate_comparison_summary(current_df, previous_df)` - Creates comparison summary DataFrame
- `calculate_overall_change(current_df, previous_df, common_numeric)` - Overall percentage change
- `calculate_average_difference(current_df, previous_df, common_numeric)` - Average difference calculation
- `create_comparison_chart(current_df, previous_df, column)` - Comparison bar chart for specific metric
- `calculate_metric_change(current_df, previous_df, column)` - Percentage change for single metric

**Use Case:** All comparison logic in one place - easy to extend with new comparison types

---

## Benefits of Modular Structure

✅ **Maintainability:** Each feature has its own file - easier to find and fix bugs

✅ **Testability:** Individual functions can be tested in isolation

✅ **Reusability:** Functions can be imported and used in other projects

✅ **Collaboration:** Multiple developers can work on different modules simultaneously

✅ **Scalability:** Easy to add new features without modifying existing code

---

## Usage Example

```python
# In app.py or any other file
from helpers.ml_analysis import analyze_data_with_ml, get_data_statistics
from helpers.visualizations import create_visualization
from helpers.comparison import calculate_comparison_summary

# Get data statistics
stats = get_data_statistics(df)
print(f"Total rows: {stats['total_rows']}")

# Analyze data and get visualization recommendations
recommendations = analyze_data_with_ml(df)

# Create visualizations
for rec in recommendations:
    fig = create_visualization(df, rec)
    # Display figure...

# Compare two datasets
common_cols, summary = calculate_comparison_summary(current_df, previous_df)
```

---

## Adding New Features

To add a new feature:

1. Create a new helper file (e.g., `helpers/feature_name.py`)
2. Implement your functions with clear docstrings
3. Add exports to `helpers/__init__.py`
4. Import in `app.py` as needed

Example:
```python
# helpers/new_feature.py
def my_new_function(df):
    """
    Description of what this does.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Result of operation
    """
    # Implementation
    return result
```

---

## Best Practices

- Keep functions focused on a single responsibility
- Add type hints for parameters and return values
- Include comprehensive docstrings
- Handle errors gracefully with try-except blocks
- Write unit tests for each helper function
