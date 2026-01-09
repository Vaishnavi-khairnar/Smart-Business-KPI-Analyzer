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
    Supports both file-based (DataFrame) and DB-based (list) data.
    """

    def __init__(self):
        self.validator = DataValidator()
        self.error_handler = ErrorHandler()

    # =====================================================
    # FILE-BASED DATA PROCESSING
    # =====================================================
    def process_csv_data(self, csv_content: str, data_type: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(StringIO(csv_content))
            df = self.validator.clean_data(df, data_type)
            return df
        except Exception as e:
            raise KPIError(
                f"Failed to process CSV data: {str(e)}",
                "DATA_PROCESSING_ERROR",
            )

    def process_excel_data(
        self,
        excel_content: bytes,
        sheet_name: Optional[str] = None,
        data_type: str = "unknown",
    ) -> pd.DataFrame:
        try:
            df = pd.read_excel(BytesIO(excel_content), sheet_name=sheet_name)
            df = self.validator.clean_data(df, data_type)
            return df
        except Exception as e:
            raise KPIError(
                f"Failed to process Excel data: {str(e)}",
                "DATA_PROCESSING_ERROR",
            )

    def process_json_data(self, json_content: str, data_type: str) -> pd.DataFrame:
        try:
            json_data = json.loads(json_content)

            if isinstance(json_data, list):
                df = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                df = pd.DataFrame([json_data])
            else:
                raise ValueError("JSON data must be a list or dictionary")

            df = self.validator.clean_data(df, data_type)
            return df

        except Exception as e:
            raise KPIError(
                f"Failed to process JSON data: {str(e)}",
                "DATA_PROCESSING_ERROR",
            )

    # =====================================================
    # KPI DATA VALIDATION (DB-BASED)
    # =====================================================
    def validate_data_for_kpi(
        self,
        data: Dict[str, Any],
        required_fields: List[str],
    ) -> None:
        """
        Validate DB-based data (lists / dicts) for KPI calculations.

        Args:
            data: Dictionary containing lists or nested dicts of lists
            required_fields: List of required data keys

        Raises:
            KPIError: If validation fails
        """
        try:
            for field in required_fields:
                if field not in data:
                    raise KPIError(
                        f"Missing required data: {field}",
                        "MISSING_DATA",
                    )

                value = data[field]

                # Case 1: List (sales, costs, marketing)
                if isinstance(value, list):
                    if len(value) == 0:
                        raise KPIError(
                            f"No data available for: {field}",
                            "EMPTY_DATA",
                        )

                # Case 2: Dict of lists (customers.start / customers.all)
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, list) and len(sub_value) == 0:
                            raise KPIError(
                                f"No data available for: {field}.{sub_key}",
                                "EMPTY_DATA",
                            )

                else:
                    raise KPIError(
                        f"Unsupported data type for {field}: {type(value)}",
                        "INVALID_DATA_TYPE",
                    )

        except KPIError:
            raise
        except Exception as e:
            raise KPIError(
                f"Unexpected error during data validation: {str(e)}",
                "UNKNOWN_ERROR",
            )
