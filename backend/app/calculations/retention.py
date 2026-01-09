from typing import Dict, Any
from datetime import datetime, timedelta
import pandas as pd
from .base import BaseCalculation

class RetentionCalculation(BaseCalculation):
       """
       Calculates Customer Retention Rate for a given period.
       Retention Rate = ((Customers at End - New Customers) / Customers at Start) * 100
       """
       
       def __init__(self):
           super().__init__(
               name="Customer Retention Rate",
               description="Percentage of customers retained over a period",
               unit="percentage"
           )
       
       def calculate(self, data: Dict[str, pd.DataFrame], 
                   period_start: datetime, 
                   period_end: datetime) -> Dict[str, Any]:
           """
           Calculate retention rate from customer data.
           
           Args:
               data: Dictionary containing 'customers' DataFrame
               period_start: Start date for calculation period
               period_end: End date for calculation period
               
           Returns:
               Dictionary containing retention rate value and extra_data
           """
           try:
               if 'customers' not in data:
                   raise ValueError("Customer data is required for retention calculation")
               
               customers_df = data['customers'].copy()
               
               # Convert date columns to datetime
               if 'signup_date' in customers_df.columns:
                   customers_df['signup_date'] = pd.to_datetime(customers_df['signup_date'])
               else:
                   raise ValueError("Customer data must contain a 'signup_date' column")
               
               if 'last_activity_date' in customers_df.columns:
                   customers_df['last_activity_date'] = pd.to_datetime(customers_df['last_activity_date'])
               else:
                   # If no last activity date, use signup date as fallback
                   customers_df['last_activity_date'] = customers_df['signup_date']
               
               # Define active customer threshold (e.g., active if activity within last 90 days)
               activity_threshold = timedelta(days=90)
               
               # Customers at start of period (signed up before period start)
               customers_start = customers_df[customers_df['signup_date'] < period_start]
               
               # Filter for active customers at start
               active_customers_start = customers_start[
                   customers_start['last_activity_date'] >= (period_start - activity_threshold)
               ]
               
               # New customers during period
               new_customers = customers_df[
                   (customers_df['signup_date'] >= period_start) & 
                   (customers_df['signup_date'] <= period_end)
               ]
               
               # Customers at end of period (signed up before or during period)
               customers_end = customers_df[customers_df['signup_date'] <= period_end]
               
               # Filter for active customers at end
               active_customers_end = customers_end[
                   customers_end['last_activity_date'] >= (period_end - activity_threshold)
               ]
               
               # Count unique customers
               customers_start_count = active_customers_start['customer_id'].nunique() if 'customer_id' in active_customers_start.columns else len(active_customers_start)
               new_customers_count = new_customers['customer_id'].nunique() if 'customer_id' in new_customers.columns else len(new_customers)
               customers_end_count = active_customers_end['customer_id'].nunique() if 'customer_id' in active_customers_end.columns else len(active_customers_end)
               
               # Calculate retention rate
               if customers_start_count > 0:
                   retention_rate = ((customers_end_count - new_customers_count) / customers_start_count) * 100
               else:
                   retention_rate = 0  # No customers at start, can't calculate retention
               
               return {
                   'value': float(retention_rate),
                   'customers_start': int(customers_start_count),
                   'new_customers': int(new_customers_count),
                   'customers_end': int(customers_end_count),
                   'period_start': period_start.isoformat(),
                   'period_end': period_end.isoformat(),
                   'activity_threshold_days': activity_threshold.days
               }
               
           except Exception as e:
               raise ValueError(f"Error calculating retention rate: {str(e)}")
       
       def validate_data(self, data: Dict[str, pd.DataFrame]) -> bool:
           """
           Validate that customer data is present and has required columns.
           """
           if 'customers' not in data:
               return False
           
           customers_df = data['customers']
           required_columns = ['signup_date']
           
           return all(col in customers_df.columns for col in required_columns)
       
       def get_required_data_fields(self) -> Dict[str, list]:
           """
           Get the required data fields for retention calculation.
           """
           return {
               'customers': ['signup_date', 'customer_id', 'last_activity_date']
           }