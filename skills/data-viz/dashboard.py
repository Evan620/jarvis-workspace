#!/usr/bin/env python3
"""
Streamlit Dashboard for Quick Data Exploration
Usage: streamlit run dashboard.py -- data.csv
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys


@st.cache_data
def load_data(filepath):
    """Load data from file"""
    filepath = Path(filepath)

    if filepath.suffix == '.csv':
        df = pd.read_csv(filepath)
    elif filepath.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(filepath)
    elif filepath.suffix == '.json':
        df = pd.read_json(filepath)
    else:
        st.error(f"Unsupported file format: {filepath.suffix}")
        return None

    return df


def main():
    st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")

    st.title("📊 Data Visualization Dashboard")
    st.sidebar.title("Controls")

    # Get data file from command line args
    if len(sys.argv) < 2:
        st.error("Please provide a data file: streamlit run dashboard.py -- data.csv")
        sys.exit(1)

    data_file = sys.argv[1]

    # Load data
    with st.spinner("Loading data..."):
        df = load_data(data_file)

    if df is None:
        sys.exit(1)

    st.success(f"Loaded {len(df)} rows from {data_file}")
    st.sidebar.markdown(f"**File:** {data_file}")
    st.sidebar.markdown(f"**Rows:** {len(df)}")
    st.sidebar.markdown(f"**Columns:** {len(df.columns)}")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Charts", "📊 Statistics", "🔍 Data View", "📤 Export"])

    # Charts Tab
    with tab1:
        st.subheader("Create Visualizations")

        col1, col2 = st.columns(2)

        with col1:
            chart_type = st.selectbox("Chart Type",
                                     ["Line", "Bar", "Scatter", "Histogram", "Pie", "Box"])
            x_col = st.selectbox("X-axis", df.columns, key="x_axis")

        with col2:
            y_col = st.selectbox("Y-axis", df.columns, key="y_axis")
            color_col = st.selectbox("Color (optional)", [None] + list(df.columns))

        # Chart creation
        if chart_type == "Line":
            fig = px.line(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} over {x_col}")
        elif chart_type == "Bar":
            fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} by {x_col}")
        elif chart_type == "Scatter":
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                           title=f"{y_col} vs {x_col}",
                           hover_data=df.columns.tolist())
        elif chart_type == "Histogram":
            fig = px.histogram(df, x=y_col, color=color_col, title=f"Distribution of {y_col}")
        elif chart_type == "Pie":
            fig = px.pie(df, names=x_col, values=y_col, title=f"{y_col} by {x_col}")
        elif chart_type == "Box":
            if color_col:
                fig = px.box(df, x=x_col, y=y_col, color=color_col,
                            title=f"Box plot of {y_col} by {x_col}")
            else:
                fig = px.box(df, x=x_col, y=y_col, title=f"Box plot of {y_col} by {x_col}")

        st.plotly_chart(fig, use_container_width=True)

    # Statistics Tab
    with tab2:
        st.subheader("Data Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Numeric Columns Summary**")
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.dataframe(df[numeric_cols].describe().T, use_container_width=True)
            else:
                st.info("No numeric columns found")

        with col2:
            st.write("**Column Information**")
            col_info = pd.DataFrame({
                'Name': df.columns,
                'Type': df.dtypes.astype(str),
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum(),
                'Unique Values': df.nunique()
            })
            st.dataframe(col_info, use_container_width=True)

        # Correlation matrix
        if len(numeric_cols) > 1:
            st.write("**Correlation Matrix**")
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                          color_continuous_scale='RdBu_r',
                          title="Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)

    # Data View Tab
    with tab3:
        st.subheader("Raw Data")

        # Search/Filter
        col1, col2 = st.columns(2)

        with col1:
            search_term = st.text_input("Search in all columns")

        with col2:
            filter_col = st.selectbox("Filter by column", [None] + list(df.columns))
            filter_value = st.text_input("Filter value")

        # Apply filters
        filtered_df = df.copy()

        if search_term:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            filtered_df = filtered_df[mask]

        if filter_col and filter_value:
            filtered_df = filtered_df[filtered_df[filter_col].astype(str).str.contains(filter_value, case=False)]

        st.info(f"Showing {len(filtered_df)} of {len(df)} rows")

        st.dataframe(filtered_df, use_container_width=True, height=400)

    # Export Tab
    with tab4:
        st.subheader("Export Data")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Export Filtered Data**")
            export_format = st.selectbox("Format", ["CSV", "Excel", "JSON"])
            if st.button("Download"):
                if export_format == "CSV":
                    csv = filtered_df.to_csv(index=False)
                    st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")
                elif export_format == "Excel":
                    buffer = pd.ExcelWriter("temp.xlsx", engine='openpyxl')
                    filtered_df.to_excel(buffer, index=False)
                    st.download_button("Download Excel", buffer, "filtered_data.xlsx",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                elif export_format == "JSON":
                    json_data = filtered_df.to_json(orient='records')
                    st.download_button("Download JSON", json_data, "filtered_data.json", "application/json")

        with col2:
            st.write("**Current Chart as Image**")
            if st.button("Save Chart"):
                st.info("Use your browser's save function to save the chart")


if __name__ == '__main__':
    main()
