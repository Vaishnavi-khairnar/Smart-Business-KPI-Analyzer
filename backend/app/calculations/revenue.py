from typing import Dict, Any
from datetime import datetime
import pandas as pd
from .base import BaseCalculation

class RevenueCalculation(BaseCalculation):
       """
       Calculates total revenue for a given period.
       """
       
       def __init__(self):
           super().__init__(
               name="Total Revenue",
               description="Total revenue generated in the given period",
               unit="currency"
           )
       
       def calculate(self, data: Dict[str, pd.DataFrame], 
                   period_start: datetime, 
                   period_end: datetime) -> Dict[str, Any]:
           """
           Calculate total revenue from sales data.
           
           Args:
               data: Dictionary containing 'sales' DataFrame
               period_start: Start date for calculation period
               period_end: End date for calculation period
               
           Returns:
               Dictionary containing revenue value and metadata
           """
           try:
               if 'sales' not in data:
                   raise ValueError("Sales data is required for revenue calculation")
               
               sales_df = data['sales'].copy()
               
               # Convert date column to datetime if it's not already
               if 'date' in sales_df.columns:
                   sales_df['date'] = pd.to_datetime(sales_df['date'])
               else:
                   raise ValueError("Sales data must contain a 'date' column")
               
               # Filter data for the specified period
               period_sales = sales_df[
                   (sales_df['date'] >= period_start) & 
                   (sales_df['date'] <= period_end)
               ]
               
               # Check if amount column exists
               if 'amount' not in period_sales.columns:
                   raise ValueError("Sales data must contain an 'amount' column")
               
               # Calculate total revenue
               total_revenue = period_sales['amount'].sum()
               
               # Calculate additional metrics
               transaction_count = len(period_sales)
               average_transaction = total_revenue / transaction_count if transaction_count > 0 else 0
               
               return {
                   'value': float(total_revenue),
                   'transaction_count': int(transaction_count),
                   'average_transaction': float(average_transaction),
                   'period_start': period_start.isoformat(),
                   'period_end': period_end.isoformat(),
                   'currency': self._get_currency(sales_df)
               }
               
           except Exception as e:
               raise ValueError(f"Error calculating revenue: {str(e)}")
       
       def validate_data(self, data: Dict[str, pd.DataFrame]) -> bool:
           """
           Validate that sales data is present and has required columns.
           """
           if 'sales' not in data:
               return False
           
           sales_df = data['sales']
           required_columns = ['date', 'amount']
           
           return all(col in sales_df.columns for col in required_columns)
       
       def get_required_data_fields(self) -> Dict[str, list]:
           """
           Get the required data fields for revenue calculation.
           """
           return {
               'sales': ['date', 'amount']
           }
       
       def _get_currency(self, sales_df: pd.DataFrame) -> str:
           """
           Extract currency from sales data if available.
           """
           if 'currency' in sales_df.columns:
               return sales_df['currency'].iloc[0] if len(sales_df) > 0 else 'USD'
           return 'USD'  # Default currency