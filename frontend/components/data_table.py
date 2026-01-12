import streamlit as st
import pandas as pd
from typing import List, Dict, Any
   
def display_data_table(df: pd.DataFrame, title: str, use_container_width: bool = True):
       """Display a pandas DataFrame as an interactive table."""
       # Display title
       st.subheader(title)
       
       # Display the DataFrame
       st.dataframe(df, use_container_width=use_container_width)
       
       # Add summary statistics
       if use_container_width:
           with st.container():
               st.write("**Data Summary:**")
               col1, col2 = st.columns(2)
               
               with col1:
                   st.metric("Total Rows", len(df))
               with col2:
                   st.metric("Columns", len(df.columns))
               
               # Display data types
               st.write("**Data Types:**")
       for col in df.columns:
                       data_type = str(df[col].dtype)
                       st.write(f"- {col}: {data_type}")