# FlowViz Quick Reference Guide

## 🚀 Getting Started

### Installation
```bash
# Clone repository
git clone <repo-url>
cd flowviz

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Login
- **Username:** `demo`
- **Password:** `demo123`

---

## 📚 Helper Modules Reference

### 1. DateTime Utilities (`helpers/datetime_utils.py`)

#### `detect_datetime_format(series)`
Automatically detects datetime format in a pandas Series.

```python
from helpers.datetime_utils import detect_datetime_format

date_series = df['date_column']
format_str = detect_datetime_format(date_series)
# Returns: '%Y-%m-%d' or None
```

#### `parse_datetime_column(df, col, date_format=None)`
Parses a datetime column with optional format.

```python
from helpers.datetime_utils import parse_datetime_column

parsed_dates = parse_datetime_column(df, 'date_column', '%Y-%m-%d')
```

---

### 2. ML Analysis (`helpers/ml_analysis.py`)

#### `analyze_data_with_ml(df)`
Analyzes DataFrame and recommends visualizations.

```python
from helpers.ml_analysis import analyze_data_with_ml

recommendations = analyze_data_with_ml(df)
# Returns: [
#   {'type': 'time_series', 'x': 'date', 'y': ['value1', 'value2'], ...},
#   {'type': 'heatmap', 'columns': [...], ...},
#   ...
# ]
```

**Recommendation Types:**
- `time_series` - Line charts for date-based data
- `heatmap` - Correlation heatmaps
- `distribution` - Histograms
- `category_analysis` - Bar charts by category
- `top_n` - Top 10 horizontal bars

#### `get_data_statistics(df)`
Returns basic statistics about the DataFrame.

```python
from helpers.ml_analysis import get_data_statistics

stats = get_data_statistics(df)
# Returns: {
#   'total_rows': 1000,
#   'total_columns': 10,
#   'numeric_columns': 7,
#   'categorical_columns': 3
# }
```

---

### 3. Visualizations (`helpers/visualizations.py`)

#### `create_visualization(df, recommendation)`
Main function to create any chart type.

```python
from helpers.visualizations import create_visualization

fig = create_visualization(df, recommendation)
st.plotly_chart(fig)
```

#### Individual Chart Functions

**Time Series:**
```python
from helpers.visualizations import create_time_series

recommendation = {
    'type': 'time_series',
    'x': 'date',
    'y': ['metric1', 'metric2'],
    'title': 'Time Series Analysis',
    'date_format': '%Y-%m-%d'
}
fig = create_time_series(df, recommendation)
```

**Heatmap:**
```python
from helpers.visualizations import create_heatmap

recommendation = {
    'type': 'heatmap',
    'columns': ['col1', 'col2', 'col3'],
    'title': 'Correlation Heatmap'
}
fig = create_heatmap(df, recommendation)
```

**Distribution:**
```python
from helpers.visualizations import create_distribution

recommendation = {
    'type': 'distribution',
    'columns': ['metric1', 'metric2'],
    'title': 'Distribution Analysis'
}
fig = create_distribution(df, recommendation)
```

---

### 4. Comparison Analysis (`helpers/comparison.py`)

#### `calculate_comparison_summary(current_df, previous_df)`
Creates summary DataFrame with changes.

```python
from helpers.comparison import calculate_comparison_summary

common_cols, summary_df = calculate_comparison_summary(current_df, previous_df)
# Returns:
# common_cols: ['metric1', 'metric2', ...]
# summary_df: DataFrame with columns ['Metric', 'Previous Month', 'Current Month', 'Change (%)']
```

#### `calculate_overall_change(current_df, previous_df, common_numeric)`
Overall percentage change across all metrics.

```python
from helpers.comparison import calculate_overall_change

change_pct = calculate_overall_change(current_df, previous_df, common_cols)
# Returns: 15.5 (means 15.5% increase)
```

#### `create_comparison_chart(current_df, previous_df, column)`
Creates bar chart comparing two periods.

```python
from helpers.comparison import create_comparison_chart

fig = create_comparison_chart(current_df, previous_df, 'sales')
st.plotly_chart(fig)
```

---

## 🎨 Styling Guide

### Metric Cards
```python
st.markdown(f"""
    <div class='metric-card'>
        <h3>{value}</h3>
        <p>{label}</p>
    </div>
""", unsafe_allow_html=True)
```

### Feature Cards
```python
st.markdown("""
    <div class='feature-card'>
        <h3>Title</h3>
        <p>Description</p>
    </div>
""", unsafe_allow_html=True)
```

---

## 🔧 Common Patterns

### Loading Data
```python
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
```

### Complete Analysis Workflow
```python
from helpers import *

# 1. Load data
df = pd.read_csv('data.csv')

# 2. Get statistics
stats = get_data_statistics(df)
st.write(f"Rows: {stats['total_rows']}, Columns: {stats['total_columns']}")

# 3. Analyze and get recommendations
recommendations = analyze_data_with_ml(df)

# 4. Create visualizations
for rec in recommendations:
    fig = create_visualization(df, rec)
    st.plotly_chart(fig, use_container_width=True)
```

### Month Comparison Workflow
```python
from helpers.comparison import *

# 1. Load both datasets
current_df = pd.read_csv('current.csv')
previous_df = pd.read_csv('previous.csv')

# 2. Calculate summary
common_cols, summary = calculate_comparison_summary(current_df, previous_df)

# 3. Show overall metrics
overall_change = calculate_overall_change(current_df, previous_df, common_cols)
st.metric("Overall Change", f"{overall_change:+.2f}%")

# 4. Create comparison charts
for col in common_cols[:5]:
    fig = create_comparison_chart(current_df, previous_df, col)
    st.plotly_chart(fig)
    
    change = calculate_metric_change(current_df, previous_df, col)
    st.write(f"Change: {change:+.2f}%")
```

---

## 🐛 Debugging Tips

### Check Module Imports
```bash
python -c "from helpers import *; print('✓ Success')"
```

### Test Individual Functions
```python
# test_helpers.py
import pandas as pd
from helpers.datetime_utils import detect_datetime_format

# Create test data
test_series = pd.Series(['2025-01-01', '2025-01-02', '2025-01-03'])

# Test function
format_str = detect_datetime_format(test_series)
print(f"Detected format: {format_str}")
assert format_str == '%Y-%m-%d', "Format detection failed!"
```

### Enable Streamlit Debug Mode
```bash
streamlit run app.py --server.runOnSave=true --logger.level=debug
```

---

## 📝 Adding New Features

### Step 1: Create Helper Module
```python
# helpers/new_feature.py
"""
New feature description
"""

def new_function(df, param1, param2):
    """
    Function description.
    
    Args:
        df: Input DataFrame
        param1: First parameter
        param2: Second parameter
        
    Returns:
        Result value
    """
    # Implementation
    result = df.groupby(param1)[param2].sum()
    return result
```

### Step 2: Add to `__init__.py`
```python
# helpers/__init__.py
from .new_feature import new_function

__all__ = [
    # ... existing exports
    'new_function'
]
```

### Step 3: Use in App
```python
# app.py
from helpers.new_feature import new_function

result = new_function(df, 'category', 'value')
st.write(result)
```

---

## 🎯 Best Practices

1. **Always use helpers for reusable logic**
   ```python
   # ❌ Bad
   df['date'] = pd.to_datetime(df['date'])
   
   # ✅ Good
   from helpers.datetime_utils import parse_datetime_column
   df['date'] = parse_datetime_column(df, 'date')
   ```

2. **Keep functions focused**
   - One function = one responsibility
   - Easy to test and maintain

3. **Add docstrings**
   ```python
   def my_function(param):
       """
       Brief description.
       
       Args:
           param: Parameter description
           
       Returns:
           Return value description
       """
       pass
   ```

4. **Handle errors gracefully**
   ```python
   try:
       result = risky_operation()
   except Exception as e:
       st.error(f"Error: {str(e)}")
       return None
   ```

---

## 📊 Sample Data Format

### For Visualization
```csv
date,sales,quantity,category
2025-01-01,1000,50,A
2025-01-02,1200,60,A
2025-01-03,900,45,B
```

### For Comparison
Both files should have same column structure:
```csv
# current_month.csv
metric1,metric2,metric3
100,200,300

# previous_month.csv
metric1,metric2,metric3
90,180,310
```

---

## 🆘 Troubleshooting

### Import Error
```bash
# Problem: ImportError: cannot import name 'X'
# Solution: Check if function is exported in __init__.py
cat helpers/__init__.py
```

### Module Not Found
```bash
# Problem: ModuleNotFoundError: No module named 'helpers'
# Solution: Make sure you're in the correct directory
pwd  # Should be /path/to/flowviz
ls helpers/  # Should show helper files
```

### Streamlit Won't Start
```bash
# Check if port is in use
lsof -i :8501

# Kill existing process
pkill -f streamlit

# Try different port
streamlit run app.py --server.port=8502
```

---

## 📞 Support

For issues or questions:
1. Check `helpers/README.md` for detailed documentation
2. Review `ARCHITECTURE.md` for system overview
3. See `REFACTORING_SUMMARY.md` for changes made
