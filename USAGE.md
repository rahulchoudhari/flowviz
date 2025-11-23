# FlowViz Usage Guide

This guide will help you get started with FlowViz for Industry Data analysis.

## Quick Start

### Step 1: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Step 2: Login

Use one of these credentials to login:

**Demo Account:**
- Username: `demo`
- Password: `demo123`

**Admin Account:**
- Username: `admin`
- Password: `admin123`

## Features Guide

### 1. Home Page

After logging in, you'll see the home page with:
- Feature carousel showcasing app capabilities
- Key features overview
- Navigation options in the sidebar

### 2. Data Visualization

#### Uploading Data

1. Click on **"📊 Data Visualization"** in the sidebar
2. Click **"Browse files"** or drag and drop your CSV/Excel file
3. The app will automatically load and analyze your data

#### Sample Data

Two sample files are included:
- `sample_data.csv` - Current month Industry Data
- `sample_data_previous.csv` - Previous month data for comparison

#### What You'll See

- **Data Preview**: First 10 rows of your data
- **Basic Statistics**: Row count, column count, data types
- **ML-Recommended Visualizations**: 
  - Time Series Analysis (if date column exists)
  - Correlation Heatmaps
  - Distribution Plots
  - Category Analysis
  - Top N Rankings

#### Downloading Visualizations

Each chart has a **"💾 Download Chart"** button that saves the visualization as an interactive HTML file.

#### Downloading Data

At the bottom of the page, you can:
- Download processed data as CSV
- Download processed data as Excel

### 3. Month-over-Month Comparison

#### Comparing Data

1. Click on **"📈 Month Comparison"** in the sidebar
2. Upload **current month** data in the left column
3. Upload **previous month** data in the right column
4. The app will automatically generate comparison charts

#### What You'll See

- **Overall Change**: Percentage change across all metrics
- **Metrics Compared**: Number of common metrics found
- **Average Difference**: Mean change in values
- **Detailed Comparisons**: Individual charts for each metric
- **Change Indicators**: Visual indicators showing increases/decreases

#### Downloading Reports

- Download comparison summary as CSV
- Download comparison summary as Excel

## Understanding ML Recommendations

The app uses machine learning to analyze your data and recommend visualizations:

### Time Series Analysis
- **When**: Your data contains date columns
- **Shows**: Trends over time for numeric metrics
- **Best for**: Identifying seasonal patterns, growth trends

### Correlation Heatmap
- **When**: Multiple numeric columns exist
- **Shows**: Relationships between different metrics
- **Best for**: Finding which metrics move together

### Distribution Analysis
- **When**: Numeric columns are present
- **Shows**: How values are spread across a range
- **Best for**: Understanding data variability and outliers

### Category Analysis
- **When**: Both categorical and numeric columns exist
- **Shows**: Average values grouped by categories
- **Best for**: Comparing performance across segments

### Top N Rankings
- **When**: Categorical and numeric columns exist
- **Shows**: Top 10 items by a metric
- **Best for**: Identifying best/worst performers

## Data Format Requirements

### Optimal Data Structure

Your CSV or Excel file should have:

1. **Column Headers**: First row should contain column names
2. **Date Columns**: Use format: YYYY-MM-DD (e.g., 2024-01-15)
3. **Numeric Columns**: Sales, revenue, quantities, etc.
4. **Categorical Columns**: Product names, regions, categories

### Example Structure

```csv
Date,Product,Category,Sales,Units_Sold,Revenue,Region
2024-01-01,Product A,Beverages,1250,85,106250,North
2024-01-02,Product B,Snacks,980,65,63700,South
```

### Supported File Types

- **.csv** - Comma-separated values
- **.xlsx** - Excel 2007+ format
- **.xls** - Excel 97-2003 format

## Tips for Best Results

### Data Preparation

1. **Clean Your Data**: Remove empty rows and columns
2. **Consistent Formatting**: Use the same date format throughout
3. **Proper Headers**: Use descriptive column names
4. **Numeric Values**: Ensure numbers don't contain text or special characters
5. **Reasonable Size**: Keep files under 50MB for best performance

### Comparison Analysis

1. **Same Structure**: Both files should have the same columns
2. **Common Metrics**: At least some numeric columns should match
3. **Similar Timeframes**: Use data from consecutive months
4. **Consistent Categories**: Use the same category names in both files

### Performance Optimization

1. **File Size**: Smaller files load faster
2. **Column Count**: Focus on relevant columns (remove unnecessary ones)
3. **Row Count**: Large datasets (100K+ rows) may take longer to process
4. **Browser**: Use Chrome or Edge for best performance

## Troubleshooting

### File Upload Issues

**Problem**: File won't upload
- **Solution**: Check file format (CSV, XLSX, XLS only)
- **Solution**: Ensure file size is reasonable (<50MB)
- **Solution**: Try a different browser

**Problem**: Error reading file
- **Solution**: Check for special characters in data
- **Solution**: Ensure first row contains headers
- **Solution**: Verify date format is consistent

### Visualization Issues

**Problem**: No visualizations appear
- **Solution**: Ensure data has numeric columns
- **Solution**: Check that data isn't all empty or zero
- **Solution**: Verify column headers are present

**Problem**: Comparison charts show errors
- **Solution**: Ensure both files have matching column names
- **Solution**: Verify both files have numeric columns
- **Solution**: Check that column names are spelled identically

### Login Issues

**Problem**: Can't login
- **Solution**: Double-check username and password
- **Solution**: Ensure no extra spaces in credentials
- **Solution**: Try clearing browser cache
- **Solution**: Use the demo account (demo/demo123)

## Advanced Usage

### Custom Analysis

While the app provides automatic recommendations, you can:
1. Download the data after viewing initial insights
2. Perform custom analysis in Excel or other tools
3. Return to upload modified data for new visualizations

### Batch Processing

To analyze multiple datasets:
1. Upload and analyze first dataset
2. Download results
3. Use the sidebar to navigate back to visualization
4. Upload next dataset
5. Repeat as needed

### Report Generation

For professional reports:
1. Generate all visualizations for your data
2. Download each chart as HTML
3. Download data as Excel
4. Open HTML files in browser and take screenshots
5. Compile screenshots into presentation software

## Best Practices

### Data Security

- Don't upload sensitive customer information
- Remove personal identifiable information before upload
- Use the app in a secure network environment
- Logout after each session

### Data Quality

- Verify data accuracy before upload
- Use consistent units across all records
- Ensure date ranges are complete
- Check for duplicate entries

### Workflow

1. **Prepare Data**: Clean and format your data
2. **Upload**: Load data into FlowViz
3. **Analyze**: Review ML-recommended visualizations
4. **Compare**: Use comparison feature for trends
5. **Download**: Save charts and reports
6. **Present**: Share insights with stakeholders

## Keyboard Shortcuts

- **Ctrl/Cmd + R**: Refresh the page
- **F11**: Toggle fullscreen
- **Ctrl/Cmd + P**: Print (for saving visualizations)

## FAQ

**Q: Can I use this with non-Industry Data?**
A: Yes! While designed for Industry, it works with any tabular data.

**Q: How many files can I upload?**
A: One at a time for visualization, two for comparison.

**Q: Can I share visualizations?**
A: Yes, download as HTML and share the files.

**Q: Is my data stored?**
A: No, data is only in memory during your session.

**Q: Can multiple users access simultaneously?**
A: Yes, each user has their own session.

**Q: How do I add more users?**
A: Currently managed in code (app.py USERS dictionary).

## Support

For issues or questions:
1. Check this guide first
2. Review the main README.md
3. Open an issue on GitHub
4. Contact the development team

## Version Information

- **Current Version**: 1.0
- **Last Updated**: November 2024
- **Compatible With**: Python 3.8+, Streamlit 1.29+

---

Happy analyzing! 📊
