import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# Set page config
st.set_page_config(
    page_title="Car Price Analysis",
    page_icon="🚗",
    layout="wide"
)

# Title and description
st.title("🚗 Car Price Analysis Dashboard")
st.markdown("""
This dashboard allows you to analyze car price data. Upload your CSV file and explore the data through interactive visualizations.
""")

# File upload with separator selection
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
separator = st.selectbox(
    "Select the separator used in your CSV file",
    options=[';', ',', '\t'],
    index=0
)

@st.cache_data
def load_data(uploaded_file, separator):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, sep=separator)
            return df
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return None
    return None

# Load and display data
if uploaded_file is not None:
    df = load_data(uploaded_file, separator)
    
    if df is not None:
        # Display basic information
        st.subheader("Dataset Overview")
        st.write(f"Number of rows: {len(df)}")
        st.write(f"Number of columns: {len(df.columns)}")
        
        # Display the dataframe
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Column selection for visualization
        st.subheader("Data Visualization")
        col1, col2 = st.columns(2)
        
        with col1:
            x_column = st.selectbox("Select X-axis column", df.columns)
        with col2:
            y_column = st.selectbox("Select Y-axis column", df.columns)
        
        # Determine plot type based on column types
        x_type = df[x_column].dtype
        y_type = df[y_column].dtype
        
        # Create appropriate plot based on data types
        if pd.api.types.is_numeric_dtype(x_type) and pd.api.types.is_numeric_dtype(y_type):
            fig = px.scatter(df, x=x_column, y=y_column, title=f"{y_column} vs {x_column}")
        elif pd.api.types.is_numeric_dtype(y_type):
            fig = px.bar(df, x=x_column, y=y_column, title=f"{y_column} by {x_column}")
        else:
            fig = px.histogram(df, x=x_column, title=f"Distribution of {x_column}")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional statistics
        st.subheader("Statistical Summary")
        st.write(df.describe())
else:
    st.info("Please upload a CSV file to begin analysis.") 