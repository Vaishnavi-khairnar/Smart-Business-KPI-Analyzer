from typing import Dict, Any, List, Optional
import pandas as pd
from datetime import datetime
from app.calculations.base import BaseCalculation
from app.calculations.revenue import RevenueCalculation
from app.calculations.profit import ProfitCalculation
from app.calculations.cac import CACCalculation
from app.calculations.retention import RetentionCalculation
from app.services.data_processor import DataProcessor
from app.utils.error_handling import ErrorHandler, KPIError

class KPICalculator:
       """
       Service for calculating KPIs from processed data.
       """
       
       def __init__(self):
           self.data_processor = DataProcessor()
           self.error_handler = ErrorHandler()
           
           # Register available calculations
           self.calculations = {
               'revenue': RevenueCalculation(),
               'profit': ProfitCalculation(),
               'cac': CACCalculation(),
               'retention': RetentionCalculation()
           }
       
       def calculate_kpi(self, kpi_type: str, data: Dict[str, pd.DataFrame], 
                       period_start: datetime, period_end: datetime) -> Dict[str, Any]:
           """
           Calculate a specific KPI.
           
           Args:
               kpi_type: Type of KPI to calculate
               data: Dictionary of DataFrames by data type
               period_start: Start date for calculation period
               period_end: End date for calculation period
               
           Returns:
               Dictionary containing KPI value and metadata
               
           Raises:
               KPIError: If calculation fails
           """
           try:
               # Check if KPI type is supported
               if kpi_type not in self.calculations:
                   raise KPIError(f"Unsupported KPI type: {kpi_type}", "UNSUPPORTED_KPI")
               
               calculation = self.calculations[kpi_type]
               
               # Validate data for this KPI
               required_fields = calculation.get_required_data_fields()
               self.data_processor.validate_data_for_kpi(data, required_fields)
               
               # Calculate the KPI
               result = calculation.calculate(data, period_start, period_end)
               
               # Add metadata
               result['kpi_type'] = kpi_type
               result['kpi_name'] = calculation.name
               result['kpi_description'] = calculation.description
               result['kpi_unit'] = calculation.unit
               result['calculated_at'] = datetime.now().isoformat()
               
               return result
               
           except KPIError:
               raise
           except Exception as e:
               error_info = self.error_handler.handle_calculation_error(e, kpi_type)
               raise KPIError(error_info['message'], error_info['error_code'], error_info)
       
       def calculate_all_kpis(self, data: Dict[str, pd.DataFrame], 
                           period_start: datetime, period_end: datetime) -> Dict[str, Any]:
           """
           Calculate all available KPIs.
           
           Args:
               data: Dictionary of DataFrames by data type
               period_start: Start date for calculation period
               period_end: End date for calculation period
               
           Returns:
               Dictionary containing all KPI results
           """
           results = {}
           errors = {}
           
           for kpi_type in self.calculations:
               try:
                   result = self.calculate_kpi(kpi_type, data, period_start, period_end)
                   results[kpi_type] = result
               except KPIError as e:
                   errors[kpi_type] = {
                       'error': True,
                       'message': str(e),
                       'error_code': e.error_code
                   }
           
           return {
               'results': results,
               'errors': errors,
               'period_start': period_start.isoformat(),
               'period_end': period_end.isoformat(),
               'calculated_at': datetime.now().isoformat()
           }
       
       def get_available_kpis(self) -> List[Dict[str, str]]:
           """
           Get information about available KPI calculations.
           
           Returns:
               List of dictionaries with KPI information
           """
           kpis = []
           
           for kpi_type, calculation in self.calculations.items():
               kpis.append({
                   'type': kpi_type,
                   'name': calculation.name,
                   'description': calculation.description,
                   'unit': calculation.unit,
                   'required_data': calculation.get_required_data_fields()
               })
           
           return kpis