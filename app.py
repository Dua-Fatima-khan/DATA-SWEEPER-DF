# Imports
import streamlit as st
import pandas as pd
import numpy as np

# Set App Config
st.set_page_config(page_title="SweepIt! 💡", layout="wide", page_icon="🧹")

# App Title & Subtitle
st.title("SweepIt! 💡")
st.markdown("### Your Smart Data Cleaning Companion 🚀")
st.markdown("---")

# About the App
st.markdown("""
### 🌟 **Welcome to SweepIt!**  
Tired of messy, unorganized data? Say hello to **SweepIt!** – your ultimate tool for **cleaning, transforming, and optimizing** datasets in seconds! Whether you're a data pro or just starting out, SweepIt! makes data cleaning **fast, easy, and fun**.  

---

### ✨ **What Makes SweepIt Special?**  
SweepIt! is packed with powerful features to turn your messy data into a masterpiece:  

✅ **Remove Duplicates** – Say goodbye to repetitive rows with a single click!  
✅ **Handle Missing Values** – Fill, drop, or analyze null values effortlessly.  
✅ **Format Data** – Standardize text, dates, and numbers for consistency.  
✅ **Detect Outliers** – Spot and handle anomalies with precision.  
✅ **Visual Insights** – Explore your data with stunning charts and summaries.  
✅ **Export Cleaned Data** – Save your polished dataset in CSV, Excel, or JSON.  

---

### 🎯 **Who Is This For?**  
SweepIt! is perfect for:  
- **Data Analysts** who want to save time on data prep.  
- **Researchers** who need clean, reliable data for analysis.  
- **Students** learning the ropes of data science.  
- **Developers** who want to integrate clean data into their apps.  

---

### 🚀 **How It Works**  
1. **Upload Your Dataset** – Bring in your messy CSV or Excel file.  
2. **Choose Cleaning Options** – Customize how you want your data cleaned.  
3. **Visualize & Analyze** – Explore your data with interactive charts.  
4. **Download Clean Data** – Get your polished dataset ready for action!  

---

### Ready to Clean Your Data? Let’s Get Started! 🧹✨  
""")

# File Upload Section
uploaded_files = st.file_uploader("📤 **Upload Your Dataset** (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)


if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(f"📌 **{uploaded_file.name}** ({uploaded_file.size / 1024:.2f} KB)")

        try:
            # Read the uploaded file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl')  # Excel support

            # Remove unnamed columns (e.g., Unnamed: 0, Unnamed: 1, etc.)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            # Display Data Preview
            st.write("🔍 **Original Data Preview:**")
            st.dataframe(df.head())

            # Cleaning Options
            st.subheader("🧹 Data Cleaning Options")

            # Remove Duplicates
            remove_duplicates = st.checkbox("🗑 Remove Duplicates")

            # Handle Missing Values
            missing_value_option = st.radio("⚠️ Handle Missing Values:",
                                            ["Do Nothing", "Drop Rows", "Fill with Mean", "Fill with Median"])

            # Choose Specific Columns
            st.subheader("🔧 Set Columns to Convert")
            columns = st.multiselect(f"Choose columns for {uploaded_file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Apply Cleaning
            if st.button("✨ Clean Data"):
                if remove_duplicates:
                    df = df.drop_duplicates()
                    st.success("✅ Duplicates Removed!")

                if missing_value_option == "Drop Rows":
                    df = df.dropna()
                    st.success("✅ Missing Values Dropped!")
                elif missing_value_option == "Fill with Mean":
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled with Mean!")
                elif missing_value_option == "Fill with Median":
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
                    st.success("✅ Missing Values Filled with Median!")

                # Display Cleaned Data Preview
                st.write("🎯 **Cleaned Data Preview:**")
                st.dataframe(df.head())

            # Data Visualization
            st.subheader("📊 Data Visualization")
            vis_type = st.selectbox("Select Visualization Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])

            if vis_type == "Bar Chart":
                st.bar_chart(df)
            elif vis_type == "Line Chart":
                st.line_chart(df)
            elif vis_type == "Scatter Plot":
                if len(df.columns) >= 2:
                    x_axis = st.selectbox("Select X-axis", df.columns)
                    y_axis = st.selectbox("Select Y-axis", df.columns)
                    st.scatter_chart(df[[x_axis, y_axis]])
                else:
                    st.warning("⚠️ Not enough columns for a scatter plot.")
            elif vis_type == "Histogram":
                column = st.selectbox("Select Column for Histogram", df.columns)
                st.bar_chart(df[column].value_counts())

            # Download Cleaned Data (Moved to the End)
            st.subheader("📥 Download Cleaned Data")
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')

            csv = convert_df(df)
            st.download_button("📥 Download Cleaned Data", csv, "cleaned_data.csv", "text/csv")

        except Exception as e:
            st.error(f"⚠️ Error reading file: {e}")