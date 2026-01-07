from typing import Dict, Any, Optional
import traceback
from datetime import datetime

class KPIError(Exception):
       """Custom exception for KPI calculation errors."""
       def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
           super().__init__(message)
           self.error_code = error_code
           self.details = details or {}

class ErrorHandler:
       """
       Utility class for handling errors in KPI calculations.
       """
       
       @staticmethod
       def handle_calculation_error(error: Exception, kpi_name: str) -> Dict[str, Any]:
           """
           Handle errors during KPI calculations.
           
           Args:
               error: The exception that occurred
               kpi_name: Name of the KPI being calculated
               
           Returns:
               Dictionary containing error information
           """
           error_info = {
               'error': True,
               'kpi_name': kpi_name,
               'message': str(error),
               'timestamp': datetime.now().isoformat(),
               'error_type': type(error).__name__
           }
           
           # Add specific error details based on error type
           if isinstance(error, ValueError):
               error_info['error_code'] = 'VALIDATION_ERROR'
               error_info['suggestion'] = 'Check that input data is in the correct format'
           
           elif isinstance(error, KeyError):
               error_info['error_code'] = 'MISSING_DATA'
               error_info['suggestion'] = 'Ensure all required data is provided'
               error_info['missing_key'] = str(error).strip("'")
           
           else:
               error_info['error_code'] = 'CALCULATION_ERROR'
               error_info['suggestion'] = 'Check calculation logic and input data'
           
           # Add traceback for debugging (in production, you might want to log this instead)
           error_info['traceback'] = traceback.format_exc()
           
           return error_info
       
       @staticmethod
       def create_error_response(message: str, error_code: str = None, 
                             details: Dict[str, Any] = None) -> Dict[str, Any]:
           """
           Create a standardized error response.
           
           Args:
               message: Error message
               error_code: Error code for categorization
               details: Additional error details
               
           Returns:
               Standardized error response dictionary
           """
           return {
               'success': False,
               'error': True,
               'message': message,
               'error_code': error_code or 'UNKNOWN_ERROR',
               'details': details or {},
               'timestamp': datetime.now().isoformat()
           }
       
       @staticmethod
       def create_success_response(data: Any, message: str = "Operation successful") -> Dict[str, Any]:
           """
           Create a standardized success response.
           
           Args:
               data: Response data
               message: Success message
               
           Returns:
               Standardized success response dictionary
           """
           return {
               'success': True,
               'error': False,
               'message': message,
               'data': data,
               'timestamp': datetime.now().isoformat()
           }