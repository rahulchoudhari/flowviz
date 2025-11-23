# FlowViz - FMGC Data Analytics Platform

A professional-grade Streamlit application for visualizing and analyzing FMGC (Fast-Moving Consumer Goods) industry data with machine learning-powered insights.

## 🌟 Features

### 1. **Secure Login System**
- User authentication with password hashing
- Demo credentials available for quick testing
- Session management

### 2. **Interactive Home Page**
- Feature showcase carousel highlighting app capabilities
- Professional dashboard layout
- Easy navigation to all features

### 3. **Smart Data Visualization**
- Support for CSV and Excel file uploads
- ML-powered automatic visualization recommendations
- Multiple chart types:
  - Time series analysis
  - Correlation heatmaps
  - Distribution plots
  - Category-based analysis
  - Top N rankings
- Professional-grade, interactive Plotly charts

### 4. **Month-over-Month Comparison**
- Compare current vs. previous month data
- Automatic metric calculation and change detection
- Visual comparison charts
- Percentage change indicators

### 5. **Data Export & Download**
- Download all visualizations as HTML files
- Export processed data as CSV or Excel
- Comparison reports with detailed metrics

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/rahulchoudhari/flowviz.git
cd flowviz
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the application**
Open your browser and navigate to `http://localhost:8501`

## 🔐 Login Credentials

For testing purposes, use these demo credentials:
- **Username:** demo
- **Password:** demo123

Or use admin account:
- **Username:** admin
- **Password:** admin123

## 📊 Usage Guide

### Data Visualization

1. **Login** to the application
2. Navigate to **"Data Visualization"** from the sidebar
3. **Upload** your CSV or Excel file
4. The ML algorithm will automatically:
   - Analyze your data structure
   - Recommend optimal visualizations
   - Generate professional charts
5. **Download** individual charts or the entire dataset

### Month Comparison

1. Navigate to **"Month Comparison"** from the sidebar
2. Upload **current month** data in the left column
3. Upload **previous month** data in the right column
4. View automated comparison charts and metrics
5. Download comparison summary reports

## 📁 Data Format

Your data files should contain:
- At least one numeric column for analysis
- Optional: Date columns for time series analysis
- Optional: Categorical columns for grouping
- Headers in the first row

### Example CSV Format:
```csv
Date,Product,Sales,Units,Revenue
2024-01-01,Product A,1000,50,50000
2024-01-02,Product B,1500,75,75000
```

## 🤖 ML-Powered Features

The application uses machine learning to:
- **Identify data types** automatically
- **Recommend optimal visualizations** based on data characteristics
- **Detect patterns** and correlations
- **Prioritize insights** by importance
- **Select relevant columns** for analysis

## 🎨 Professional Design

- Clean, modern interface
- Responsive layout for all screen sizes
- Color-coded metrics and indicators
- Interactive Plotly charts with zoom and pan
- Gradient styling for visual appeal
- Consistent branding throughout

## 🛠️ Technology Stack

- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **Scikit-learn** - Machine learning algorithms
- **NumPy** - Numerical computations
- **OpenPyXL** - Excel file handling

## 📦 Project Structure

```
flowviz/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
└── .gitignore           # Git ignore rules
```

## 🔒 Security Notes

- Passwords are hashed using SHA-256
- Session state management for secure access
- No sensitive data is stored in plain text
- For production use, implement a proper database for user management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🎯 Future Enhancements

- [ ] Database integration for user management
- [ ] Advanced ML models for predictions
- [ ] Real-time data streaming
- [ ] Multi-language support
- [ ] Custom dashboard builder
- [ ] API integration for external data sources
- [ ] Advanced filtering and querying
- [ ] Scheduled reports and alerts

---

Built with ❤️ using Streamlit