from typing import Dict, Any
from datetime import datetime
import pandas as pd
from .base import BaseCalculation


class RevenueCalculation(BaseCalculation):
    """
    Calculates total revenue for a given period.
    Works with pandas DataFrames.
    """

    def __init__(self):
        super().__init__(
            name="Total Revenue",
            description="Total revenue generated in the given period",
            unit="currency",
        )

    def calculate(
        self,
        data: Dict[str, Any],
        period_start: datetime,
        period_end: datetime,
    ) -> Dict[str, Any]:
        try:
            # -------------------------------------------------
            # Validate input
            # -------------------------------------------------
            if "sales" not in data:
                raise ValueError("Sales data is required for revenue calculation")

            sales_df: pd.DataFrame = data["sales"]

            if sales_df.empty:
                return {
                    "value": 0.0,
                    "transaction_count": 0,
                    "average_transaction": 0.0,
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "currency": "USD",
                }

            # Filter sales data for the specified period
            period_sales = sales_df[
                (sales_df['date'] >= period_start) & (sales_df['date'] <= period_end)
            ]

            if period_sales.empty:
                return {
                    "value": 0.0,
                    "transaction_count": 0,
                    "average_transaction": 0.0,
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "currency": "USD",
                }

            # -------------------------------------------------
            # Calculate revenue
            # -------------------------------------------------
            total_revenue = period_sales['amount'].sum()
            transaction_count = len(period_sales)
            average_transaction = (
                total_revenue / transaction_count
                if transaction_count > 0
                else 0
            )

            return {
                "value": round(float(total_revenue), 2),
                "transaction_count": transaction_count,
                "average_transaction": round(float(average_transaction), 2),
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "currency": "USD",
            }

        except Exception as e:
            raise ValueError(f"Error calculating revenue: {str(e)}")

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate that sales data exists and is a non-empty DataFrame.
        """
        if "sales" not in data or not isinstance(data["sales"], pd.DataFrame):
            return False
        
        df = data["sales"]
        required_columns = {"date", "amount"}
        
        return not df.empty and required_columns.issubset(df.columns)


    def get_required_data_fields(self) -> list:
        """
        Required data keys for this KPI.
        """
        return ["sales"]
