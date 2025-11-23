import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
import hashlib

# Page configuration
st.set_page_config(
    page_title="FlowViz - FMGC Data Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .carousel-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'data' not in st.session_state:
    st.session_state.data = None
if 'previous_data' not in st.session_state:
    st.session_state.previous_data = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# User credentials (in production, use a database)
USERS = {
    'admin': hashlib.sha256('admin123'.encode()).hexdigest(),
    'demo': hashlib.sha256('demo123'.encode()).hexdigest(),
}

def verify_login(username, password):
    """Verify user credentials"""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return username in USERS and USERS[username] == hashed_password

def login_page():
    """Display login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>📊 FlowViz</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>FMGC Data Analytics Platform</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("Login", use_container_width=True):
                    if verify_login(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.page = 'home'
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("📌 Demo credentials: username='demo', password='demo123'")

def home_page():
    """Display home page with carousel"""
    st.title("🏠 Welcome to FlowViz Dashboard")
    st.markdown(f"Hello, **{st.session_state.username}**! 👋")
    
    # Carousel-like feature showcase
    st.markdown("---")
    st.header("✨ What FlowViz Can Do")
    
    # Create carousel items
    carousel_items = [
        {
            "title": "📊 Smart Data Visualization",
            "description": "Upload your CSV or Excel files and let our ML algorithms automatically identify the best visualizations for your data.",
            "icon": "📊"
        },
        {
            "title": "📈 Comparative Analysis",
            "description": "Compare current data with previous month's data to identify trends, patterns, and anomalies.",
            "icon": "📈"
        },
        {
            "title": "💾 Export & Download",
            "description": "Download all visualizations and analyzed data in high-quality formats for presentations and reports.",
            "icon": "💾"
        },
        {
            "title": "🤖 ML-Powered Insights",
            "description": "Leverage machine learning to discover hidden patterns and get actionable insights from your FMGC data.",
            "icon": "🤖"
        }
    ]
    
    # Display carousel items in a grid
    cols = st.columns(2)
    for idx, item in enumerate(carousel_items):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class='carousel-item'>
                    <h2>{item['icon']} {item['title']}</h2>
                    <p style='font-size: 16px;'>{item['description']}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features Section
    st.header("🎯 Key Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='feature-card'>
                <h3 style='text-align: center;'>🔒</h3>
                <h4 style='text-align: center;'>Secure Login</h4>
                <p>Protected access to your data</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='feature-card'>
                <h3 style='text-align: center;'>📁</h3>
                <h4 style='text-align: center;'>File Upload</h4>
                <p>Support for CSV and Excel files</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='feature-card'>
                <h3 style='text-align: center;'>🔍</h3>
                <h4 style='text-align: center;'>Auto-Analysis</h4>
                <p>ML-driven data insights</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='feature-card'>
                <h3 style='text-align: center;'>📊</h3>
                <h4 style='text-align: center;'>Pro Visuals</h4>
                <p>Professional-grade charts</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Use the sidebar to navigate to Data Visualization or Comparison Analysis")

def analyze_data_with_ml(df):
    """Use ML to determine best visualizations for the data"""
    recommendations = []
    
    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Date columns detection
    date_cols = []
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                pd.to_datetime(df[col])
                date_cols.append(col)
            except (ValueError, TypeError):
                pass
    
    # Recommendation 1: Time series if date column exists
    if date_cols and numeric_cols:
        recommendations.append({
            'type': 'time_series',
            'x': date_cols[0],
            'y': numeric_cols[:3],  # Top 3 numeric columns
            'title': f'Time Series Analysis',
            'priority': 1
        })
    
    # Recommendation 2: Correlation heatmap for numeric data
    if len(numeric_cols) >= 2:
        recommendations.append({
            'type': 'heatmap',
            'columns': numeric_cols[:10],  # Max 10 columns for readability
            'title': 'Correlation Heatmap',
            'priority': 2
        })
    
    # Recommendation 3: Distribution plots for numeric columns
    if numeric_cols:
        # Use variance to identify most interesting columns
        variances = df[numeric_cols].var().sort_values(ascending=False)
        top_cols = variances.head(3).index.tolist()
        recommendations.append({
            'type': 'distribution',
            'columns': top_cols,
            'title': 'Distribution Analysis',
            'priority': 3
        })
    
    # Recommendation 4: Category analysis
    if categorical_cols and numeric_cols:
        # Find categorical column with reasonable number of unique values
        for cat_col in categorical_cols:
            if 2 <= df[cat_col].nunique() <= 20:
                recommendations.append({
                    'type': 'category_analysis',
                    'category': cat_col,
                    'values': numeric_cols[:2],
                    'title': f'Analysis by {cat_col}',
                    'priority': 4
                })
                break
    
    # Recommendation 5: Top N analysis
    if categorical_cols and numeric_cols:
        recommendations.append({
            'type': 'top_n',
            'category': categorical_cols[0],
            'value': numeric_cols[0],
            'title': f'Top 10 by {numeric_cols[0]}',
            'priority': 5
        })
    
    return sorted(recommendations, key=lambda x: x['priority'])

def create_visualization(df, recommendation):
    """Create visualization based on ML recommendation"""
    fig = None
    
    if recommendation['type'] == 'time_series':
        df_copy = df.copy()
        df_copy[recommendation['x']] = pd.to_datetime(df_copy[recommendation['x']])
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
    
    elif recommendation['type'] == 'heatmap':
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
    
    elif recommendation['type'] == 'distribution':
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
    
    elif recommendation['type'] == 'category_analysis':
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
    
    elif recommendation['type'] == 'top_n':
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

def data_visualization_page():
    """Data visualization page"""
    st.title("📊 Data Visualization")
    
    # File uploader
    st.header("📁 Upload Your Data")
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your FMGC industry data file"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.session_state.data = df
            
            # Display data overview
            st.success(f"✅ File loaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Show data preview
            with st.expander("🔍 Data Preview", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Basic statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>{df.shape[0]}</h3>
                        <p>Total Rows</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>{df.shape[1]}</h3>
                        <p>Total Columns</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>{numeric_cols}</h3>
                        <p>Numeric Columns</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                categorical_cols = len(df.select_dtypes(include=['object']).columns)
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>{categorical_cols}</h3>
                        <p>Categorical Columns</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ML-based visualization recommendations
            st.header("🤖 ML-Recommended Visualizations")
            st.info("Our machine learning algorithm has analyzed your data and recommends the following visualizations:")
            
            recommendations = analyze_data_with_ml(df)
            
            if recommendations:
                for idx, rec in enumerate(recommendations):
                    with st.container():
                        st.subheader(f"📈 Visualization {idx + 1}: {rec['title']}")
                        
                        fig = create_visualization(df, rec)
                        
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Download button
                            col_a, col_b, col_c = st.columns([3, 1, 3])
                            with col_b:
                                # Convert figure to HTML
                                buffer = io.StringIO()
                                fig.write_html(buffer)
                                html_bytes = buffer.getvalue().encode()
                                
                                st.download_button(
                                    label="💾 Download Chart",
                                    data=html_bytes,
                                    file_name=f"visualization_{idx+1}.html",
                                    mime="text/html",
                                    use_container_width=True
                                )
                        
                        st.markdown("---")
            
            # Download processed data
            st.header("💾 Download Data")
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="processed_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Create Excel file in memory
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Data')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📥 Download as Excel",
                    data=excel_data,
                    file_name="processed_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    else:
        st.info("👆 Please upload a CSV or Excel file to begin visualization")

def comparison_page():
    """Data comparison page for previous month analysis"""
    st.title("📊 Month-over-Month Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📅 Current Month Data")
        current_file = st.file_uploader(
            "Upload current month data",
            type=['csv', 'xlsx', 'xls'],
            key="current"
        )
    
    with col2:
        st.header("📅 Previous Month Data")
        previous_file = st.file_uploader(
            "Upload previous month data",
            type=['csv', 'xlsx', 'xls'],
            key="previous"
        )
    
    if current_file and previous_file:
        try:
            # Read files
            if current_file.name.endswith('.csv'):
                current_df = pd.read_csv(current_file)
            else:
                current_df = pd.read_excel(current_file)
            
            if previous_file.name.endswith('.csv'):
                previous_df = pd.read_csv(previous_file)
            else:
                previous_df = pd.read_excel(previous_file)
            
            st.success("✅ Both files loaded successfully!")
            
            # Find common numeric columns
            current_numeric = set(current_df.select_dtypes(include=[np.number]).columns)
            previous_numeric = set(previous_df.select_dtypes(include=[np.number]).columns)
            common_numeric = list(current_numeric.intersection(previous_numeric))
            
            if common_numeric:
                st.markdown("---")
                st.header("📈 Comparative Analysis")
                
                # Summary comparison
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    current_total = current_df[common_numeric].sum().sum()
                    previous_total = previous_df[common_numeric].sum().sum()
                    change = ((current_total - previous_total) / previous_total * 100) if previous_total != 0 else 0
                    
                    st.markdown(f"""
                        <div class='metric-card'>
                            <h3>{change:+.2f}%</h3>
                            <p>Overall Change</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class='metric-card'>
                            <h3>{len(common_numeric)}</h3>
                            <p>Metrics Compared</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    avg_change = current_df[common_numeric].mean().mean() - previous_df[common_numeric].mean().mean()
                    st.markdown(f"""
                        <div class='metric-card'>
                            <h3>{avg_change:+.2f}</h3>
                            <p>Avg Difference</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Detailed comparisons for each metric
                for col in common_numeric[:5]:  # Show top 5 metrics
                    st.subheader(f"📊 {col} Comparison")
                    
                    # Create comparison chart
                    comparison_data = pd.DataFrame({
                        'Period': ['Previous Month', 'Current Month'],
                        col: [previous_df[col].sum(), current_df[col].sum()]
                    })
                    
                    fig = px.bar(
                        comparison_data,
                        x='Period',
                        y=col,
                        title=f'{col} - Month over Month',
                        template='plotly_white',
                        color='Period',
                        color_discrete_sequence=['#764ba2', '#667eea']
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Calculate and show change
                    change = ((current_df[col].sum() - previous_df[col].sum()) / previous_df[col].sum() * 100) if previous_df[col].sum() != 0 else 0
                    
                    if change > 0:
                        st.success(f"📈 Increase of {change:.2f}%")
                    elif change < 0:
                        st.error(f"📉 Decrease of {abs(change):.2f}%")
                    else:
                        st.info("➡️ No change")
                    
                    # Download button for this comparison
                    col_a, col_b, col_c = st.columns([3, 1, 3])
                    with col_b:
                        buffer = io.StringIO()
                        fig.write_html(buffer)
                        html_bytes = buffer.getvalue().encode()
                        
                        st.download_button(
                            label="💾 Download",
                            data=html_bytes,
                            file_name=f"comparison_{col}.html",
                            mime="text/html",
                            use_container_width=True,
                            key=f"download_{col}"
                        )
                    
                    st.markdown("---")
                
                # Download comparison summary
                st.header("💾 Download Comparison Report")
                
                # Create summary dataframe
                summary = pd.DataFrame({
                    'Metric': common_numeric,
                    'Previous Month': [previous_df[col].sum() for col in common_numeric],
                    'Current Month': [current_df[col].sum() for col in common_numeric],
                })
                summary['Change (%)'] = ((summary['Current Month'] - summary['Previous Month']) / summary['Previous Month'] * 100).round(2)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    csv = summary.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Summary (CSV)",
                        data=csv,
                        file_name="comparison_summary.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        summary.to_excel(writer, index=False, sheet_name='Comparison')
                    excel_data = output.getvalue()
                    
                    st.download_button(
                        label="📥 Download Summary (Excel)",
                        data=excel_data,
                        file_name="comparison_summary.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            
            else:
                st.warning("⚠️ No common numeric columns found between the two datasets")
        
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
    
    else:
        st.info("👆 Please upload both current and previous month data files to begin comparison")

def main():
    """Main application logic"""
    
    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.title("🧭 Navigation")
            st.markdown("---")
            
            # User info
            st.markdown(f"👤 **User:** {st.session_state.username}")
            st.markdown("---")
            
            # Navigation menu
            menu_options = {
                "🏠 Home": "home",
                "📊 Data Visualization": "visualization",
                "📈 Month Comparison": "comparison"
            }
            
            for label, page in menu_options.items():
                if st.button(label, use_container_width=True):
                    st.session_state.page = page
                    st.rerun()
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ''
                st.session_state.page = 'login'
                st.session_state.data = None
                st.session_state.previous_data = None
                st.rerun()
            
            st.markdown("---")
            st.markdown("### ℹ️ About")
            st.markdown("FlowViz v1.0")
            st.markdown("FMGC Data Analytics Platform")
        
        # Display selected page
        if st.session_state.page == 'home':
            home_page()
        elif st.session_state.page == 'visualization':
            data_visualization_page()
        elif st.session_state.page == 'comparison':
            comparison_page()

if __name__ == "__main__":
    main()
