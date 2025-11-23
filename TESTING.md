# Testing Guide for FlowViz

## Quick Test

To verify the application works correctly, follow these steps:

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Start Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### 3. Test Login

- Username: `demo`
- Password: `demo123`

### 4. Test Data Visualization

1. Navigate to "📊 Data Visualization" in sidebar
2. Upload `sample_data.csv`
3. Verify you see:
   - Data preview table
   - 4 metric cards (30 rows, 8 columns, 4 numeric, 4 categorical)
   - 5 ML-recommended visualizations
4. Test download buttons for charts and data

### 5. Test Month Comparison

1. Navigate to "📈 Month Comparison"
2. Upload `sample_data.csv` as current month
3. Upload `sample_data_previous.csv` as previous month
4. Verify comparison charts and metrics appear
5. Test download buttons for reports

## Expected Behavior

### Login Page
- Clean, centered login form
- Demo credentials shown in info box
- Error message for invalid credentials

### Home Page
- Welcome message with username
- 4 gradient feature cards
- 4 key feature boxes
- Sidebar navigation

### Data Visualization
- File uploader with drag & drop
- Data preview in expandable section
- Colored metric cards
- 5 interactive Plotly charts:
  1. Time Series Analysis
  2. Correlation Heatmap
  3. Distribution Analysis
  4. Analysis by Product
  5. Top 10 by Sales
- Download buttons for each chart
- Download buttons for data (CSV/Excel)

### Month Comparison
- Two file upload sections (current/previous)
- Metric cards showing overall change
- Individual comparison charts for each metric
- Percentage change indicators
- Download buttons for summary reports

## Troubleshooting

### Port Already in Use
```bash
# Kill existing Streamlit process
pkill -f streamlit
# Or use different port
streamlit run app.py --server.port=8502
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### File Upload Issues
- Ensure file is CSV or Excel format
- Check file has headers in first row
- Verify file size is under 200MB

## Performance Notes

- Files up to 50MB: Fast loading (<5 seconds)
- Files 50-200MB: May take 10-30 seconds
- Large datasets (100K+ rows): Visualizations may take longer

## Browser Compatibility

Tested and working on:
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

## Security Testing

- ✅ CodeQL scan: No vulnerabilities found
- ✅ Password hashing: SHA-256
- ✅ Session management: Secure
- ✅ No data persistence: Session-only storage

## Known Limitations

1. User management is code-based (not database)
2. No data persistence between sessions
3. Single file upload at a time for visualization
4. Max file size: 200MB (Streamlit default)

