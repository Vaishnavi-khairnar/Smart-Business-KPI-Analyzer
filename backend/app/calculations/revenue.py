from typing import Dict, Any, List
from datetime import datetime
from .base import BaseCalculation
from app.models.sale import Sale


class RevenueCalculation(BaseCalculation):
    """
    Calculates total revenue for a given period.
    Works with DB ORM objects (NOT pandas).
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

            sales: List[Sale] = data["sales"]

            if not sales:
                raise ValueError("No sales data available for the selected period")

            # -------------------------------------------------
            # Calculate revenue
            # -------------------------------------------------
            total_revenue = sum(
                sale.amount for sale in sales if sale.amount is not None
            )

            transaction_count = len(sales)
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
        Validate that sales data exists and is non-empty.
        """
        return "sales" in data and isinstance(data["sales"], list)

    def get_required_data_fields(self) -> list:
        """
        Required data keys for this KPI.
        """
        return ["sales"]
