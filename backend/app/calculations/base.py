from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd

class BaseCalculation(ABC):
       """
       Base class for all KPI calculations.
       Provides common functionality and enforces consistent interface.
       """
       
       def __init__(self, name: str, description: str, unit: str):
           self.name = name
           self.description = description
           self.unit = unit
       
       @abstractmethod
       def calculate(self, data: Dict[str, pd.DataFrame], 
                   period_start: datetime, 
                   period_end: datetime) -> Dict[str, Any]:
           """
           Calculate the KPI value.
           
           Args:
               data: Dictionary containing DataFrames with required data
               period_start: Start date for calculation period
               period_end: End date for calculation period
               
           Returns:
               Dictionary containing the KPI value and extra_data
           """
           pass
       
       def validate_data(self, data: Dict[str, pd.DataFrame]) -> bool:
           """
           Validate that required data is present and in correct format.
           
           Args:
               data: Dictionary containing DataFrames to validate
               
           Returns:
               True if data is valid, False otherwise
           """
           # Override in subclasses for specific validation
           return True
       
       def get_required_data_fields(self) -> Dict[str, list]:
           """
           Get the required data fields for this calculation.
           
           Returns:
               Dictionary mapping data types to required field names
           """
           # Override in subclasses to specify required fields
           return {}