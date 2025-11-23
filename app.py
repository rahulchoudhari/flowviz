import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
import hashlib

# Import modular helpers
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
from helpers.ceo_dashboard import (
    create_kpi_cards,
    create_revenue_trend,
    create_regional_performance,
    create_product_mix,
    create_efficiency_metrics,
    create_promotion_impact,
    create_top_products
)
from helpers.custom_charts import (
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

# Page configuration
st.set_page_config(
    page_title="FlowViz - Industry Data Analytics",
    page_icon="logo/flowviz_logo.png",
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
        # Display logo
        col_logo1, col_logo2, col_logo3 = st.columns([1, 1, 1])
        with col_logo2:
            st.image("logo/flowviz_logo.png", width=150)
        
        st.markdown("<h1 style='text-align: center;'>FlowViz</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Industry Data Analytics Platform</h3>", unsafe_allow_html=True)
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
    """Display industrial data intelligence home page"""
    
    # Display logo at the top
    col_logo1, col_logo2, col_logo3 = st.columns([2, 1, 2])
    with col_logo2:
        st.image("logo/flowviz_logo.png", width=200)
    
    # Modern dark-themed CSS with Tailwind-inspired styling
    st.markdown("""
    <style>
        .flow-gradient {
            background: linear-gradient(90deg, #10b981 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
        }
        .hero-section {
            background-image: radial-gradient(circle at 50% 10%, rgba(20, 184, 166, 0.15) 0%, rgba(248, 249, 250, 1) 70%);
            padding: 80px 20px;
            border-radius: 20px;
            text-align: center;
            margin: 20px 0;
        }
        .data-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            padding: 30px;
            border-radius: 15px;
            border: 2px solid #e5e7eb;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            height: 100%;
        }
        .data-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(6, 182, 212, 0.3);
            border-color: #06b6d4;
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            display: block;
        }
        .use-case-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            border-radius: 20px;
            margin: 40px 0;
        }
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 20px;
            color: #1f2937;
        }
        .hero-subtitle {
            font-size: 1.5rem;
            color: #6b7280;
            margin-bottom: 30px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        .cta-button {
            background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
            color: white;
            padding: 15px 40px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1.1rem;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .cta-button:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 15px -3px rgba(6, 182, 212, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">
            Turn <span class="flow-gradient">Industrial Data Flow</span><br>
            into <span style="color: #10b981;">Actionable Intelligence</span>
        </h1>
        <p class="hero-subtitle">
            FlowViz is your central hub for manufacturing, supply chain, and resource utilization analysis—built for real-time operational excellence.
        </p>
        <p style="font-size: 1.2rem; color: #374151; margin-top: 20px;">
            👋 Welcome back, <strong>{st.session_state.username}</strong>!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Analytical Features Section
    st.markdown("<h2 style='text-align: center; font-size: 2.5rem; margin: 60px 0 40px 0; color: #1f2937;'>⚡ Key Analytical Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="data-card">
            <span class="feature-icon">📊</span>
            <h3 style="color: #10b981; margin-bottom: 15px;">Overall Equipment Efficiency (OEE)</h3>
            <p style="color: #6b7280; font-size: 0.95rem;">
                Automated calculation of Availability, Performance, and Quality using production logs and shift data.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="data-card">
            <span class="feature-icon">⚡</span>
            <h3 style="color: #06b6d4; margin-bottom: 15px;">Utility & Resource Consumption</h3>
            <p style="color: #6b7280; font-size: 0.95rem;">
                Visualize kWh, water, and manpower per unit of output to identify waste and drive sustainability.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="data-card">
            <span class="feature-icon">⚠️</span>
            <h3 style="color: #eab308; margin-bottom: 15px;">Real-Time Anomaly Alerts</h3>
            <p style="color: #6b7280; font-size: 0.95rem;">
                Receive instant notifications for unexpected deviations in production metrics or utility spikes.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="data-card">
            <span class="feature-icon">🔮</span>
            <h3 style="color: #8b5cf6; margin-bottom: 15px;">Predictive Maintenance</h3>
            <p style="color: #6b7280; font-size: 0.95rem;">
                Leverage historical data to predict machine failures and optimize maintenance schedules.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Use Cases Section
    st.markdown("""
    <div class="use-case-section">
        <h2 style="font-size: 2.5rem; margin-bottom: 30px; text-align: center;">
            🏭 Empowering Decisions Across the Factory Floor
        </h2>
        <p style="font-size: 1.2rem; margin-bottom: 40px; text-align: center; opacity: 0.95;">
            FlowViz integrates seamlessly with ERP, MES, and sensor data to provide a unified view of your entire operation, from raw materials to final shipment.
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px;">
            <div style="padding: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 10px;">
                <h3 style="margin-bottom: 10px;">✅ Manufacturing</h3>
                <p style="opacity: 0.9;">Reduce bottlenecks and increase throughput efficiency.</p>
            </div>
            <div style="padding: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 10px;">
                <h3 style="margin-bottom: 10px;">✅ Utility Management</h3>
                <p style="opacity: 0.9;">Pinpoint processes with the highest energy and water footprint.</p>
            </div>
            <div style="padding: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 10px;">
                <h3 style="margin-bottom: 10px;">✅ Quality Control</h3>
                <p style="opacity: 0.9;">Correlate production inputs with finished product quality metrics.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Start Guide
    st.markdown("<h2 style='text-align: center; font-size: 2rem; margin: 60px 0 30px 0; color: #1f2937;'>🚀 Quick Start</h2>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 3rem; margin-bottom: 15px;">1️⃣</div>
            <h3 style="color: #10b981; margin-bottom: 10px;">Upload Data</h3>
            <p style="color: #6b7280;">Navigate to Data Visualization and upload your CSV or Excel files</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 3rem; margin-bottom: 15px;">2️⃣</div>
            <h3 style="color: #06b6d4; margin-bottom: 10px;">Analyze</h3>
            <p style="color: #6b7280;">Let AI recommend the best visualizations for your data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_c:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 3rem; margin-bottom: 15px;">3️⃣</div>
            <h3 style="color: #8b5cf6; margin-bottom: 10px;">Export</h3>
            <p style="color: #6b7280;">Download insights and share with your team</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 Use the sidebar to navigate to Data Visualization or Month Comparison")


def data_visualization_page():
    """Data visualization page"""
    st.title("📊 Data Visualization")
    
    # File uploader
    st.header("📁 Upload Your Data")
    
    # Option to choose between sample data or upload
    data_source = st.radio(
        "Select Data Source:",
        ["📂 Use Sample Data", "💻 Upload from Local Machine"],
        horizontal=True
    )
    
    uploaded_file = None
    
    if data_source == "📂 Use Sample Data":
        sample_files = {
            "August 2025": "SampleData/Aug.csv",
            "September 2025": "SampleData/Sep.csv",
            "October 2025": "SampleData/Oct.csv"
        }
        
        selected_sample = st.selectbox(
            "Choose Sample Dataset:",
            list(sample_files.keys())
        )
        
        if st.button("Load Sample Data", type="primary"):
            try:
                df = pd.read_csv(sample_files[selected_sample])
                st.session_state.data = df
                st.success(f"✅ Sample data '{selected_sample}' loaded successfully!")
                uploaded_file = "sample"  # Flag to trigger processing
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
    else:
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your industry data file"
        )
    
    # Process uploaded file or use session state data
    if uploaded_file is not None:
        try:
            # Only read file if it's not the sample flag
            if uploaded_file != "sample":
                # Read the file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.data = df
                st.success(f"✅ File loaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Use data from session state (either just loaded or from sample)
            df = st.session_state.data
            
            # Display data overview
            if uploaded_file != "sample":
                st.success(f"✅ File loaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Show data preview
            with st.expander("🔍 Data Preview", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Basic statistics using helper
            stats = get_data_statistics(df)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>{stats['total_rows']}</h3>
                        <p>Total Rows</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>{stats['total_columns']}</h3>
                        <p>Total Columns</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>{stats['numeric_columns']}</h3>
                        <p>Numeric Columns</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>{stats['categorical_columns']}</h3>
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
    elif st.session_state.data is not None:
        # Data was loaded in a previous interaction (sample data)
        df = st.session_state.data
        st.info(f"📊 Currently viewing data with {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Show the same analysis for persisted data
        with st.expander("🔍 Data Preview", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Continue with analysis...
        stats = get_data_statistics(df)
        recommendations = analyze_data_with_ml(df)
        
        # Display recommendations
        if recommendations:
            st.header("🤖 ML-Recommended Visualizations")
            for idx, rec in enumerate(recommendations):
                with st.container():
                    st.subheader(f"📈 Visualization {idx + 1}: {rec['title']}")
                    fig = create_visualization(df, rec)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        col_a, col_b, col_c = st.columns([3, 1, 3])
                        with col_b:
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
    else:
        st.info("👆 Please select a data source and load data to begin visualization")

def comparison_page():
    """Data comparison page for previous month analysis"""
    st.title("📊 Month-over-Month Comparison")
    
    # Option to choose between sample data or upload
    comp_data_source = st.radio(
        "Select Data Source:",
        ["📂 Use Sample Data", "💻 Upload from Local Machine"],
        horizontal=True,
        key="comparison_source"
    )
    
    current_file = None
    previous_file = None
    current_df = None
    previous_df = None
    
    if comp_data_source == "📂 Use Sample Data":
        st.info("📌 Compare August vs September, or September vs October")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("📅 Previous Month")
            prev_sample = st.selectbox(
                "Select previous month:",
                ["August 2025", "September 2025"],
                key="prev_month"
            )
        
        with col2:
            st.header("📅 Current Month")
            curr_sample = st.selectbox(
                "Select current month:",
                ["September 2025", "October 2025"],
                key="curr_month"
            )
        
        if st.button("Load Sample Data for Comparison", type="primary"):
            try:
                sample_map = {
                    "August 2025": "SampleData/Aug.csv",
                    "September 2025": "SampleData/Sep.csv",
                    "October 2025": "SampleData/Oct.csv"
                }
                previous_df = pd.read_csv(sample_map[prev_sample])
                current_df = pd.read_csv(sample_map[curr_sample])
                current_file = "sample"
                previous_file = "sample"
                st.success(f"✅ Loaded {prev_sample} vs {curr_sample}")
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
    else:
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
            except Exception as e:
                st.error(f"Error processing files: {str(e)}")
    
    # Process comparison if data is loaded (either from sample or upload)
    if current_df is not None and previous_df is not None:
        try:
            
            # Find common numeric columns and create summary using helper
            common_numeric, summary = calculate_comparison_summary(current_df, previous_df)
            
            if common_numeric:
                st.markdown("---")
                st.header("📈 Comparative Analysis")
                
                # Summary comparison using helpers
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    change = calculate_overall_change(current_df, previous_df, common_numeric)
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
                    avg_change = calculate_average_difference(current_df, previous_df, common_numeric)
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
                    
                    # Create comparison chart using helper
                    fig = create_comparison_chart(current_df, previous_df, col)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Calculate and show change using helper
                    change = calculate_metric_change(current_df, previous_df, col)
                    
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


def about_page():
    """About page with app information and data privacy policy"""
    st.title("ℹ️ About FlowViz")
    
    # App Overview
    st.header("📱 Application Overview")
    st.markdown("""
    **FlowViz** is a comprehensive **Industry Data Analytics Platform** designed to help businesses 
    gain actionable insights from their operational data. Built with Python and Streamlit, FlowViz 
    provides powerful visualization and analysis tools without requiring any coding knowledge.
    
    ### 🎯 Key Features:
    - **📊 Data Visualization**: Interactive charts and graphs with multiple visualization types
    - **💼 CEO Dashboard**: Executive-level KPIs and business performance metrics
    - **🎨 Custom Chart Builder**: Create custom visualizations with drag-and-drop simplicity
    - **📈 Month Comparison**: Compare performance across different time periods
    - **🤖 ML Insights**: Automated recommendations based on data patterns
    - **📥 Sample Data**: Pre-loaded datasets for quick testing and exploration
    """)
    
    st.markdown("---")
    
    # Data Privacy & Security
    st.header("🔒 Data Privacy & Security")
    st.markdown("""
    ### Your Data is Safe and Private
    
    We take data privacy seriously. Here's what you need to know:
    
    ✅ **No Data Storage**: This application **does not store any of your data** on our servers or databases. 
    All data processing happens in your browser session only.
    
    ✅ **Session-Based Processing**: Your uploaded data exists only in your active session. When you logout 
    or close the browser, all data is immediately cleared from memory.
    
    ✅ **No Third-Party Sharing**: We do not share, sell, or transmit your data to any third parties.
    
    ✅ **Local Processing**: All computations and visualizations are performed locally within the application 
    runtime. No data leaves your session.
    
    ✅ **Secure Connection**: The application uses standard web security protocols to protect data in transit.
    
    ### 📊 Sole Purpose: Data Visualization
    
    FlowViz is designed with **one primary goal**: to help you **visualize and analyze your data**. 
    We provide the tools, you maintain full control of your information.
    """)
    
    st.markdown("---")
    
    # Usage Guidelines
    st.header("📖 How to Use FlowViz")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Getting Started
        1. **Login** with your credentials
        2. Navigate to **Data Visualization**
        3. **Upload your CSV file** or use sample data
        4. Explore different visualization options
        5. Access specialized dashboards as needed
        """)
    
    with col2:
        st.markdown("""
        ### 💡 Best Practices
        - Use CSV files with clear column headers
        - Ensure date columns are properly formatted
        - Include numeric columns for metrics
        - Use sample data to test features first
        - Download charts for reports/presentations
        """)
    
    st.markdown("---")
    
    # Technical Information
    st.header("⚙️ Technical Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Version**  
        FlowViz v1.0
        
        **Framework**  
        Streamlit
        """)
    
    with col2:
        st.markdown("""
        **Language**  
        Python 3.12
        
        **Libraries**  
        Pandas, Plotly, NumPy
        """)
    
    with col3:
        st.markdown("""
        **License**  
        Open Source
        
        **Platform**  
        Industry Data Analytics
        """)
    
    st.markdown("---")
    
    # Support & Contact
    st.header("📧 Support & Feedback")
    st.markdown("""
    Have questions or suggestions? We'd love to hear from you!
    
    - 📝 **Documentation**: Check the README and QUICKREF files in the repository
    - 🐛 **Report Issues**: Submit bug reports through the issue tracker
    - 💬 **Feature Requests**: Share your ideas for improvements
    - ⭐ **Star the Project**: Show your support on GitHub
    """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p><strong>FlowViz - Industry Data Analytics Platform</strong></p>
        <p>Empowering businesses with data-driven insights</p>
        <p>© 2025 FlowViz. Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


def ceo_dashboard_page():
    """CEO Dashboard with high-level business metrics"""
    st.title("📊 CEO Dashboard - Business Overview")
    
    if st.session_state.data is None:
        st.warning("⚠️ Please load data first from the Data Visualization page")
        return
    
    df = st.session_state.data
    
    # Calculate KPIs
    kpis = create_kpi_cards(df)
    
    # Display KPI Cards
    st.header("🎯 Key Performance Indicators")
    cols = st.columns(4)
    
    with cols[0]:
        if 'total_revenue' in kpis:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>${kpis['total_revenue']:,.0f}</h3>
                    <p>Total Revenue</p>
                </div>
            """, unsafe_allow_html=True)
    
    with cols[1]:
        if 'total_transactions' in kpis:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>{kpis['total_transactions']:,}</h3>
                    <p>Total Transactions</p>
                </div>
            """, unsafe_allow_html=True)
    
    with cols[2]:
        if 'avg_transaction' in kpis:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>${kpis['avg_transaction']:.2f}</h3>
                    <p>Avg Transaction Value</p>
                </div>
            """, unsafe_allow_html=True)
    
    with cols[3]:
        if 'revenue_per_hour' in kpis:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>${kpis['revenue_per_hour']:.2f}</h3>
                    <p>Revenue per Hour</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Revenue Trend
    fig = create_revenue_trend(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Two columns for regional and product mix
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_regional_performance(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_product_mix(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Efficiency metrics
    fig = create_efficiency_metrics(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Two columns for promotion impact and top products
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_promotion_impact(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_top_products(df, top_n=8)
        if fig:
            st.plotly_chart(fig, use_container_width=True)


def custom_charts_page():
    """Custom chart builder page"""
    st.title("🎨 Custom Chart Builder")
    
    if st.session_state.data is None:
        st.warning("⚠️ Please load data first from the Data Visualization page")
        return
    
    df = st.session_state.data
    
    st.info("📌 Create custom visualizations by selecting columns and chart types")
    
    # Get column types
    col_types = get_column_types(df)
    
    # Display available columns
    with st.expander("📋 Available Columns", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Numeric Columns:**")
            st.write(col_types['numeric'])
        with col2:
            st.markdown("**Categorical Columns:**")
            st.write(col_types['categorical'])
        with col3:
            st.markdown("**Date Columns:**")
            st.write(col_types['date'])
    
    st.markdown("---")
    
    # Chart type selector
    chart_type = st.selectbox(
        "📊 Select Chart Type:",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Box Plot", 
         "Correlation Heatmap", "Area Chart", "Histogram"]
    )
    
    st.markdown("---")
    
    # Dynamic form based on chart type
    if chart_type == "Line Chart":
        st.subheader("📈 Line Chart Configuration")
        x_col = st.selectbox("X-Axis (Date/Categorical):", 
                            col_types['date'] + col_types['categorical'] + col_types['numeric'])
        y_cols = st.multiselect("Y-Axis (Numeric - select one or more):", 
                               col_types['numeric'])
        title = st.text_input("Chart Title (optional):", "")
        
        if st.button("Generate Line Chart", type="primary") and y_cols:
            fig = create_custom_line_chart(df, x_col, y_cols, title or None)
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Bar Chart":
        st.subheader("📊 Bar Chart Configuration")
        x_col = st.selectbox("Category Column:", 
                            col_types['categorical'] + col_types['date'])
        y_col = st.selectbox("Value Column (Numeric):", col_types['numeric'])
        orientation = st.radio("Orientation:", ["Vertical", "Horizontal"])
        title = st.text_input("Chart Title (optional):", "")
        
        if st.button("Generate Bar Chart", type="primary"):
            orient = 'h' if orientation == "Horizontal" else 'v'
            fig = create_custom_bar_chart(df, x_col, y_col, orient, title or None)
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Scatter Plot":
        st.subheader("🔵 Scatter Plot Configuration")
        x_col = st.selectbox("X-Axis:", col_types['numeric'])
        y_col = st.selectbox("Y-Axis:", col_types['numeric'])
        color_col = st.selectbox("Color by (optional):", 
                                ["None"] + col_types['categorical'])
        size_col = st.selectbox("Size by (optional):", 
                               ["None"] + col_types['numeric'])
        title = st.text_input("Chart Title (optional):", "")
        
        if st.button("Generate Scatter Plot", type="primary"):
            color = None if color_col == "None" else color_col
            size = None if size_col == "None" else size_col
            fig = create_custom_scatter(df, x_col, y_col, color, size, title or None)
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Pie Chart":
        st.subheader("🥧 Pie Chart Configuration")
        names_col = st.selectbox("Category Column:", col_types['categorical'])
        values_col = st.selectbox("Value Column (Numeric):", col_types['numeric'])
        title = st.text_input("Chart Title (optional):", "")
        
        if st.button("Generate Pie Chart", type="primary"):
            fig = create_custom_pie_chart(df, names_col, values_col, title or None)
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Box Plot":
        st.subheader("📦 Box Plot Configuration")
        category_col = st.selectbox("Category Column:", col_types['categorical'])
        value_col = st.selectbox("Value Column (Numeric):", col_types['numeric'])
        title = st.text_input("Chart Title (optional):", "")
        
        if st.button("Generate Box Plot", type="primary"):
            fig = create_custom_box_plot(df, category_col, value_col, title or None)
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Correlation Heatmap":
        st.subheader("🔥 Correlation Heatmap Configuration")
        if len(col_types['numeric']) >= 2:
            selected_cols = st.multiselect("Select Numeric Columns (min 2):", 
                                          col_types['numeric'],
                                          default=col_types['numeric'][:5])
            title = st.text_input("Chart Title (optional):", "")
            
            if st.button("Generate Heatmap", type="primary") and len(selected_cols) >= 2:
                fig = create_custom_heatmap(df, selected_cols, title or None)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for correlation heatmap")
    
    elif chart_type == "Area Chart":
        st.subheader("📊 Area Chart Configuration")
        x_col = st.selectbox("X-Axis:", col_types['date'] + col_types['categorical'])
        y_cols = st.multiselect("Y-Axis (Numeric - select one or more):", 
                               col_types['numeric'])
        title = st.text_input("Chart Title (optional):", "")
        
        if st.button("Generate Area Chart", type="primary") and y_cols:
            fig = create_custom_area_chart(df, x_col, y_cols, title or None)
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Histogram":
        st.subheader("📊 Histogram Configuration")
        column = st.selectbox("Select Column:", col_types['numeric'])
        bins = st.slider("Number of Bins:", 10, 100, 30)
        title = st.text_input("Chart Title (optional):", "")
        
        if st.button("Generate Histogram", type="primary"):
            fig = create_custom_histogram(df, column, bins, title or None)
            st.plotly_chart(fig, use_container_width=True)


def main():
    """Main application logic"""
    
    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar navigation
        with st.sidebar:
            # Logo at top of sidebar
            st.image("logo/flowviz_logo.png", width=100)
            st.title("🧭 Navigation")
            st.markdown("---")
            
            # User info
            st.markdown(f"👤 **User:** {st.session_state.username}")
            st.markdown("---")
            
            # Navigation menu
            menu_options = {
                "🏠 Home": "home",
                "📊 Data Visualization": "visualization",
                "💼 CEO Dashboard": "ceo_dashboard",
                "🎨 Custom Charts": "custom_charts",
                "📈 Month Comparison": "comparison",
                "ℹ️ About": "about"
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
            st.markdown("Industry Data Analytics Platform")
        
        # Display selected page
        if st.session_state.page == 'home':
            home_page()
        elif st.session_state.page == 'visualization':
            data_visualization_page()
        elif st.session_state.page == 'ceo_dashboard':
            ceo_dashboard_page()
        elif st.session_state.page == 'custom_charts':
            custom_charts_page()
        elif st.session_state.page == 'comparison':
            comparison_page()
        elif st.session_state.page == 'about':
            about_page()

if __name__ == "__main__":
    main()
