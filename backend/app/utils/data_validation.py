from typing import Dict, List, Any
import pandas as pd
from datetime import datetime

class DataValidationError(Exception):
       """Custom exception for data validation errors."""
       pass

class DataValidator:
       """
       Utility class for validating data before KPI calculations.
       """
       
       @staticmethod
       def validate_dataframe(df: pd.DataFrame, required_columns: List[str], 
                           data_type: str) -> None:
           """
           Validate that a DataFrame has required columns and is not empty.
           
           Args:
               df: DataFrame to validate
               required_columns: List of required column names
               data_type: Type of data being validated (for error messages)
               
           Raises:
               DataValidationError: If validation fails
           """
           if df.empty:
               raise DataValidationError(f"{data_type} data is empty")
           
           missing_columns = [col for col in required_columns if col not in df.columns]
           if missing_columns:
               raise DataValidationError(
                   f"{data_type} data is missing required columns: {missing_columns}"
               )
       
       @staticmethod
       def validate_date_range(data: Dict[str, pd.DataFrame], 
                           period_start: datetime, 
                           period_end: datetime) -> None:
           """
           Validate that data contains records within the specified date range.
           
           Args:
               data: Dictionary of DataFrames to validate
               period_start: Start date for calculation period
               period_end: End date for calculation period
               
           Raises:
               DataValidationError: If no data is found in the date range
           """
           data_in_range = False
           
           for data_type, df in data.items():
               # Try to find a date column
               date_columns = [col for col in df.columns if 'date' in col.lower()]
               
               if date_columns:
                   date_col = date_columns[0]
                   # Convert to datetime if not already
                   df[date_col] = pd.to_datetime(df[date_col])
                   
                   # Check if any records are in the date range
                   in_range = df[
                       (df[date_col] >= period_start) & 
                       (df[date_col] <= period_end)
                   ]
                   
                   if not in_range.empty:
                       data_in_range = True
                       break
           
           if not data_in_range:
               raise DataValidationError(
                   f"No data found in the specified date range: {period_start} to {period_end}"
               )
       
       @staticmethod
       def validate_numeric_columns(df: pd.DataFrame, 
                                 numeric_columns: List[str], 
                                 data_type: str) -> None:
           """
           Validate that specified columns contain numeric data.
           
           Args:
               df: DataFrame to validate
               numeric_columns: List of column names that should be numeric
               data_type: Type of data being validated (for error messages)
               
           Raises:
               DataValidationError: If columns contain non-numeric data
           """
           for col in numeric_columns:
               if col in df.columns:
                   # Try to convert to numeric
                   try:
                       pd.to_numeric(df[col], errors='raise')
                   except (ValueError, TypeError):
                       raise DataValidationError(
                           f"Column '{col}' in {data_type} data contains non-numeric values"
                       )
       
       @staticmethod
       def clean_data(df: pd.DataFrame, data_type: str) -> pd.DataFrame:
           """
           Clean data by handling missing values and duplicates.
           
           Args:
               df: DataFrame to clean
               data_type: Type of data being cleaned
               
           Returns:
               Cleaned DataFrame
           """
           # Make a copy to avoid modifying the original
           cleaned_df = df.copy()
           
           # Remove duplicate rows
           initial_count = len(cleaned_df)
           cleaned_df = cleaned_df.drop_duplicates()
           duplicates_removed = initial_count - len(cleaned_df)
           
           if duplicates_removed > 0:
               print(f"Removed {duplicates_removed} duplicate rows from {data_type} data")
           
           # Handle missing values based on data type
           if data_type == 'sales':
               # For sales data, remove rows with missing amount
               if 'amount' in cleaned_df.columns:
                   cleaned_df = cleaned_df.dropna(subset=['amount'])
           
           elif data_type == 'customers':
               # For customer data, remove rows with missing customer_id
               if 'customer_id' in cleaned_df.columns:
                   cleaned_df = cleaned_df.dropna(subset=['customer_id'])
           
           return cleaned_df