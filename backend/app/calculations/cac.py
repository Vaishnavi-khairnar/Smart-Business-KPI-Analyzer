from typing import Dict, Any
from datetime import datetime 
import pandas as pd
from.base import BaseCalculation

class CACCalculation(BaseCalculation):
       """
       Calculates Customer Acquisition Cost (CAC) for a given period.
       CAC = Marketing Spend / New Customers
       """
       
       def __init__(self):
           super().__init__(
               name="Customer Acquisition Cost",
               description="Cost to acquire a new customer",
               unit="currency"
           )
       
       def calculate(self, data: Dict[str, pd.DataFrame], 
                   period_start: datetime, 
                   period_end: datetime) -> Dict[str, Any]:
           """
           Calculate CAC from marketing and customer data.
           
           Args:
               data: Dictionary containing 'marketing' and 'customers' DataFrames
               period_start: Start date for calculation period
               period_end: End date for calculation period
               
           Returns:
               Dictionary containing CAC value and extra_data
           """
           try:
               if 'marketing' not in data or 'customers' not in data:
                   raise ValueError("Both marketing and customer data are required for CAC calculation")
               
               marketing_df = data['marketing'].copy()
               customers_df = data['customers'].copy()
               
               # Convert date columns to datetime
               if 'date' in marketing_df.columns:
                   marketing_df['date'] = pd.to_datetime(marketing_df['date'])
               else:
                   raise ValueError("Marketing data must contain a 'date' column")
               
               if 'signup_date' in customers_df.columns:
                   customers_df['signup_date'] = pd.to_datetime(customers_df['signup_date'])
               else:
                   raise ValueError("Customer data must contain a 'signup_date' column")
               
               # Filter marketing data for the specified period
               period_marketing = marketing_df[
                   (marketing_df['date'] >= period_start) & 
                   (marketing_df['date'] <= period_end)
               ]
               
               # Filter customers who signed up in the specified period
               period_customers = customers_df[
                   (customers_df['signup_date'] >= period_start) & 
                   (customers_df['signup_date'] <= period_end)
               ]
               
               # Check if required columns exist
               if 'amount' not in period_marketing.columns:
                   raise ValueError("Marketing data must contain an 'amount' column")
               
               # Calculate totals
               total_marketing_spend = period_marketing['amount'].sum()
               
               # Count new customers (unique customers)
               if 'customer_id' in period_customers.columns:
                   new_customers = period_customers['customer_id'].nunique()
               else:
                   new_customers = len(period_customers)
               
               # Calculate CAC
               cac = total_marketing_spend / new_customers if new_customers > 0 else 0
               
               return {
                   'value': float(cac),
                   'marketing_spend': float(total_marketing_spend),
                   'new_customers': int(new_customers),
                   'period_start': period_start.isoformat(),
                   'period_end': period_end.isoformat(),
                   'currency': self._get_currency(marketing_df)
               }
               
           except Exception as e:
               raise ValueError(f"Error calculating CAC: {str(e)}")
       
       def validate_data(self, data: Dict[str, pd.DataFrame]) -> bool:
           """
           Validate that marketing and customer data are present and have required columns.
           """
           if 'marketing' not in data or 'customers' not in data:
               return False
           
           marketing_df = data['marketing']
           customers_df = data['customers']
           
           marketing_required = ['date', 'amount']
           customers_required = ['signup_date']
           
           return (all(col in marketing_df.columns for col in marketing_required) and
                   all(col in customers_df.columns for col in customers_required))
       
       def get_required_data_fields(self) -> Dict[str, list]:
           """
           Get the required data fields for CAC calculation.
           """
           return {
               'marketing': ['date', 'amount'],
               'customers': ['signup_date', 'customer_id']
           }
       
       def _get_currency(self, marketing_df: pd.DataFrame) -> str:
           """
           Extract currency from marketing data if available.
           """
           if 'currency' in marketing_df.columns and len(marketing_df) > 0:
               return marketing_df['currency'].iloc[0]
           return 'USD'  # Default currency