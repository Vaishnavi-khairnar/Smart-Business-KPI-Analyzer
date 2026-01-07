from typing import Dict, Any, List, Optional
import pandas as pd
from datetime import datetime
from io import StringIO, BytesIO
import json
from app.utils.data_validation import DataValidator, DataValidationError
from app.utils.error_handling import ErrorHandler, KPIError

class DataProcessor:
       """
       Service for processing and validating data before KPI calculations.
       """
       
       def __init__(self):
           self.validator = DataValidator()
           self.error_handler = ErrorHandler()
       
       def process_csv_data(self, csv_content: str, data_type: str) -> pd.DataFrame:
           """
           Process CSV data and return a DataFrame.
           
           Args:
               csv_content: CSV content as string
               data_type: Type of data (sales, costs, marketing, customers)
               
           Returns:
               Processed DataFrame
               
           Raises:
               KPIError: If data processing fails
           """
           try:
               # Read CSV content
               df = pd.read_csv(StringIO(csv_content))
               
               # Clean the data
               df = self.validator.clean_data(df, data_type)
               
               return df
               
           except Exception as e:
               raise KPIError(f"Failed to process CSV data: {str(e)}", "DATA_PROCESSING_ERROR")
       
       def process_excel_data(self, excel_content: bytes, sheet_name: Optional[str] = None, 
                           data_type: str = "unknown") -> pd.DataFrame:
           """
           Process Excel data and return a DataFrame.
           
           Args:
               excel_content: Excel content as bytes
               sheet_name: Name of the sheet to read (if None, reads first sheet)
               data_type: Type of data (sales, costs, marketing, customers)
               
           Returns:
               Processed DataFrame
               
           Raises:
               KPIError: If data processing fails
           """
           try:
               # Read Excel content
               df = pd.read_excel(BytesIO(excel_content), sheet_name=sheet_name)
               
               # Clean the data
               df = self.validator.clean_data(df, data_type)
               
               return df
               
           except Exception as e:
               raise KPIError(f"Failed to process Excel data: {str(e)}", "DATA_PROCESSING_ERROR")
       
       def process_json_data(self, json_content: str, data_type: str) -> pd.DataFrame:
           """
           Process JSON data and return a DataFrame.
           
           Args:
               json_content: JSON content as string
               data_type: Type of data (sales, costs, marketing, customers)
               
           Returns:
               Processed DataFrame
               
           Raises:
               KPIError: If data processing fails
           """
           try:
               # Parse JSON content
               json_data = json.loads(json_content)
               
               # Convert to DataFrame
               if isinstance(json_data, list):
                   df = pd.DataFrame(json_data)
               elif isinstance(json_data, dict):
                   # If it's a single record, wrap in a list
                   df = pd.DataFrame([json_data])
               else:
                   raise ValueError("JSON data must be a list or dictionary")
               
               # Clean the data
               df = self.validator.clean_data(df, data_type)
               
               return df
               
           except Exception as e:
               raise KPIError(f"Failed to process JSON data: {str(e)}", "DATA_PROCESSING_ERROR")
       
       def validate_data_for_kpi(self, data: Dict[str, pd.DataFrame], 
                               required_fields: Dict[str, List[str]]) -> None:
           """
           Validate that data contains all required fields for KPI calculations.
           
           Args:
               data: Dictionary of DataFrames by data type
               required_fields: Dictionary mapping data types to required field lists
               
           Raises:
               KPIError: If validation fails
           """
           try:
               for data_type, fields in required_fields.items():
                   if data_type in data:
                       self.validator.validate_dataframe(
                           data[data_type], fields, data_type
                       )
                       self.validator.validate_numeric_columns(
                           data[data_type], 
                           [field for field in fields if 'amount' in field.lower()],
                           data_type
                       )
                   else:
                       raise DataValidationError(f"Missing required data type: {data_type}")
               
               # Validate that data exists in the date range
               # Note: We'll validate date ranges in the calculation methods
               # since different KPIs might have different date requirements
               
           except DataValidationError as e:
               raise KPIError(str(e), "DATA_VALIDATION_ERROR")
           except Exception as e:
               raise KPIError(f"Unexpected error during data validation: {str(e)}", "UNKNOWN_ERROR")