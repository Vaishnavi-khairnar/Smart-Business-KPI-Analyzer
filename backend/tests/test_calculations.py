import pytest
import pandas as pd
from datetime import datetime, timedelta
from app.calculations.revenue import RevenueCalculation
from app.calculations.profit import ProfitCalculation
from app.calculations.cac import CACCalculation
from app.calculations.retention import RetentionCalculation

class TestRevenueCalculation:
       """Test cases for RevenueCalculation."""
       
       def setup_method(self):
           """Set up test data before each test."""
           self.calculation = RevenueCalculation()
           
           # Sample sales data
           self.sales_data = pd.DataFrame({
               'date': [
                   datetime(2023, 1, 1),
                   datetime(2023, 1, 15),
                   datetime(2023, 2, 1),
                   datetime(2023, 2, 15)
               ],
               'amount': [100, 200, 150, 250],
               'product_id': ['PROD001', 'PROD002', 'PROD001', 'PROD003']
           })
           
           self.data = {'sales': self.sales_data}
       
       def test_calculate_revenue_for_january(self):
           """Test revenue calculation for January 2023."""
           period_start = datetime(2023, 1, 1)
           period_end = datetime(2023, 1, 31)
           
           result = self.calculation.calculate(self.data, period_start, period_end)
           
           assert result['value'] == 300.0  # 100 + 200
           assert result['transaction_count'] == 2
           assert result['average_transaction'] == 150.0  # 300 / 2
       
       def test_calculate_revenue_for_february(self):
           """Test revenue calculation for February 2023."""
           period_start = datetime(2023, 2, 1)
           period_end = datetime(2023, 2, 28)
           
           result = self.calculation.calculate(self.data, period_start, period_end)
           
           assert result['value'] == 400.0  # 150 + 250
           assert result['transaction_count'] == 2
           assert result['average_transaction'] == 200.0  # 400 / 2
       
       def test_calculate_revenue_with_no_data(self):
           """Test revenue calculation with no matching data."""
           period_start = datetime(2023, 3, 1)
           period_end = datetime(2023, 3, 31)
           
           result = self.calculation.calculate(self.data, period_start, period_end)
           
           assert result['value'] == 0.0
           assert result['transaction_count'] == 0
           assert result['average_transaction'] == 0.0
       
       def test_validate_data_with_valid_data(self):
           """Test data validation with valid data."""
           assert self.calculation.validate_data(self.data) == True
       
       def test_validate_data_with_missing_sales(self):
           """Test data validation with missing sales data."""
           assert self.calculation.validate_data({}) == False
       
       def test_validate_data_with_missing_columns(self):
           """Test data validation with missing required columns."""
           invalid_data = {'sales': pd.DataFrame({'invalid_column': [1, 2, 3]})}
           assert self.calculation.validate_data(invalid_data) == False

class TestProfitCalculation:
       """Test cases for ProfitCalculation."""
       
       def setup_method(self):
           """Set up test data before each test."""
           self.calculation = ProfitCalculation()
           
           # Sample sales data
           self.sales_data = pd.DataFrame({
               'date': [
                   datetime(2023, 1, 1),
                   datetime(2023, 1, 15),
                   datetime(2023, 2, 1),
                   datetime(2023, 2, 15)
               ],
               'amount': [100, 200, 150, 250]
           })
           
           # Sample cost data
           self.cost_data = pd.DataFrame({
               'date': [
                   datetime(2023, 1, 5),
                   datetime(2023, 1, 20),
                   datetime(2023, 2, 5),
                   datetime(2023, 2, 20)
               ],
               'amount': [50, 75, 60, 90]
           })
           
           self.data = {
               'sales': self.sales_data,
               'costs': self.cost_data
           }
       
       def test_calculate_profit_for_january(self):
           """Test profit calculation for January 2023."""
           period_start = datetime(2023, 1, 1)
           period_end = datetime(2023, 1, 31)
           
           result = self.calculation.calculate(self.data, period_start, period_end)
           
           assert result['revenue'] == 300.0  # 100 + 200
           assert result['costs'] == 125.0  # 50 + 75
           assert result['value'] == 175.0  # 300 - 125
           assert result['profit_margin'] == (175.0 / 300.0) * 100
       
       def test_calculate_profit_with_no_costs(self):
           """Test profit calculation with no costs in the period."""
           period_start = datetime(2023, 3, 1)
           period_end = datetime(2023, 3, 31)
           
           result = self.calculation.calculate(self.data, period_start, period_end)
           
           assert result['revenue'] == 0.0
           assert result['costs'] == 0.0
           assert result['value'] == 0.0
           assert result['profit_margin'] == 0.0

class TestCACCalculation:
       """Test cases for CACCalculation."""
       
       def setup_method(self):
           """Set up test data before each test."""
           self.calculation = CACCalculation()
           
           # Sample marketing data
           self.marketing_data = pd.DataFrame({
               'date': [
                   datetime(2023, 1, 1),
                   datetime(2023, 1, 15),
                   datetime(2023, 2, 1),
                   datetime(2023, 2, 15)
               ],
               'amount': [500, 750, 600, 900]
           })
           
           # Sample customer data
           self.customer_data = pd.DataFrame({
               'customer_id': [1, 2, 3, 4, 5],
               'signup_date': [
                   datetime(2023, 1, 5),
                   datetime(2023, 1, 10),
                   datetime(2023, 1, 20),
                   datetime(2023, 2, 5),
                   datetime(2023, 2, 25)
               ]
           })
           
           self.data = {
               'marketing': self.marketing_data,
               'customers': self.customer_data
           }
       
       def test_calculate_cac_for_january(self):
           """Test CAC calculation for January 2023."""
           period_start = datetime(2023, 1, 1)
           period_end = datetime(2023, 1, 31)
           
           result = self.calculation.calculate(self.data, period_start, period_end)
           
           assert result['marketing_spend'] == 1250.0  # 500 + 750
           assert result['new_customers'] == 3  # Customers 1, 2, 3
           assert result['value'] == 1250.0 / 3  # Marketing spend / new customers
       
       def test_calculate_cac_with_no_new_customers(self):
           """Test CAC calculation with no new customers."""
           period_start = datetime(2023, 3, 1)
           period_end = datetime(2023, 3, 31)
           
           result = self.calculation.calculate(self.data, period_start, period_end)
           
           assert result['marketing_spend'] == 0.0
           assert result['new_customers'] == 0
           assert result['value'] == 0.0  # Avoid division by zero

class TestRetentionCalculation:
       """Test cases for RetentionCalculation."""
       
       def setup_method(self):
           """Set up test data before each test."""
           self.calculation = RetentionCalculation()
           
           # Sample customer data
           self.customer_data = pd.DataFrame({
               'customer_id': [1, 2, 3, 4, 5],
               'signup_date': [
                   datetime(2022, 11, 1),  # Existing customer
                   datetime(2022, 12, 15), # Existing customer
                   datetime(2023, 1, 5),   # New customer in January
                   datetime(2023, 1, 20),  # New customer in January
                   datetime(2023, 2, 10)   # New customer in February
               ],
               'last_activity_date': [
                   datetime(2023, 1, 15),  # Active
                   datetime(2023, 1, 10),  # Active
                   datetime(2023, 1, 25),  # Active
                   datetime(2023, 2, 5),   # Active
                   datetime(2023, 2, 20)   # Active
               ]
           })
           
           self.data = {'customers': self.customer_data}
       
       def test_calculate_retention_for_january(self):
           """Test retention calculation for January 2023."""
           period_start = datetime(2023, 1, 1)
           period_end = datetime(2023, 1, 31)
           
           result = self.calculation.calculate(self.data, period_start, period_end)
           
           # 2 existing customers at start (customers 1, 2)
           # 2 new customers during period (customers 3, 4)
           # 4 active customers at end (customers 1, 2, 3, 4)
           # Retention rate = ((4 - 2) / 2) * 100 = 100%
           assert result['customers_start'] == 2
           assert result['new_customers'] == 2
           assert result['customers_end'] == 4
           assert result['value'] == ((4 - 2) / 2) * 100
       
       def test_calculate_retention_with_no_existing_customers(self):
           """Test retention calculation with no existing customers."""
           # Create data with only new customers
           new_customer_data = pd.DataFrame({
               'customer_id': [1, 2],
               'signup_date': [
                   datetime(2023, 3, 1),
                   datetime(2023, 3, 15)
               ],
               'last_activity_date': [
                   datetime(2023, 3, 10),
                   datetime(2023, 3, 20)
               ]
           })
           
           data = {'customers': new_customer_data}
           
           period_start = datetime(2023, 3, 1)
           period_end = datetime(2023, 3, 31)
           
           result = self.calculation.calculate(data, period_start, period_end)
           
           assert result['customers_start'] == 0
           assert result['new_customers'] == 2
           assert result['customers_end'] == 2
           assert result['value'] == 0  # No existing customers, retention rate is 0