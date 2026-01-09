from typing import Dict,Any
from datetime import datetime 
import pandas as pd
from.base import BaseCalculation

class ProfitCalculation(BaseCalculation):
       """
       Calculates profit (revenue minus costs) for a given period.
       """
       
       def __init__(self):
           super().__init__(
               name="Profit",
               description="Profit calculated as revenue minus costs",
               unit="currency"
           )
       
       def calculate(self, data: Dict[str, pd.DataFrame], 
                   period_start: datetime, 
                   period_end: datetime) -> Dict[str, Any]:
           """
           Calculate profit from sales and cost data.
           
           Args:
               data: Dictionary containing 'sales' and 'costs' DataFrames
               period_start: Start date for calculation period
               period_end: End date for calculation period
               
           Returns:
               Dictionary containing profit value and extra_data
           """
           try:
               if 'sales' not in data or 'costs' not in data:
                   raise ValueError("Both sales and cost data are required for profit calculation")
               
               sales_df = data['sales'].copy()
               costs_df = data['costs'].copy()
               
               # Convert date columns to datetime
               if 'date' in sales_df.columns:
                   sales_df['date'] = pd.to_datetime(sales_df['date'])
               else:
                   raise ValueError("Sales data must contain a 'date' column")
               
               if 'date' in costs_df.columns:
                   costs_df['date'] = pd.to_datetime(costs_df['date'])
               else:
                   raise ValueError("Cost data must contain a 'date' column")
               
               # Filter data for the specified period
               period_sales = sales_df[
                   (sales_df['date'] >= period_start) & 
                   (sales_df['date'] <= period_end)
               ]
               
               period_costs = costs_df[
                   (costs_df['date'] >= period_start) & 
                   (costs_df['date'] <= period_end)
               ]
               
               # Check if amount columns exist
               if 'amount' not in period_sales.columns:
                   raise ValueError("Sales data must contain an 'amount' column")
               
               if 'amount' not in period_costs.columns:
                   raise ValueError("Cost data must contain an 'amount' column")
               
               # Calculate totals
               total_revenue = period_sales['amount'].sum()
               total_costs = period_costs['amount'].sum()
               profit = total_revenue - total_costs
               
               # Calculate profit margin
               profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
               
               return {
                   'value': float(profit),
                   'revenue': float(total_revenue),
                   'costs': float(total_costs),
                   'profit_margin': float(profit_margin),
                   'period_start': period_start.isoformat(),
                   'period_end': period_end.isoformat(),
                   'currency': self._get_currency(sales_df, costs_df)
               }
               
           except Exception as e:
               raise ValueError(f"Error calculating profit: {str(e)}")
       
       def validate_data(self, data: Dict[str, pd.DataFrame]) -> bool:
           """
           Validate that sales and cost data are present and have required columns.
           """
           if 'sales' not in data or 'costs' not in data:
               return False
           
           sales_df = data['sales']
           costs_df = data['costs']
           required_columns = ['date', 'amount']
           
           return (all(col in sales_df.columns for col in required_columns) and
                   all(col in costs_df.columns for col in required_columns))
       
       def get_required_data_fields(self) -> Dict[str, list]:
           """
           Get the required data fields for profit calculation.
           """
           return {
               'sales': ['date', 'amount'],
               'costs': ['date', 'amount']
           }
       
       def _get_currency(self, sales_df: pd.DataFrame, costs_df: pd.DataFrame) -> str:
           """
           Extract currency from data if available.
           """
           if 'currency' in sales_df.columns and len(sales_df) > 0:
               return sales_df['currency'].iloc[0]
           elif 'currency' in costs_df.columns and len(costs_df) > 0:
               return costs_df['currency'].iloc[0]
           return 'USD'  # Default currency