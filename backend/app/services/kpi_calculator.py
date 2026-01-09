from typing import Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.calculations.revenue import RevenueCalculation
from app.calculations.profit import ProfitCalculation
from app.calculations.cac import CACCalculation
from app.calculations.retention import RetentionCalculation
from app.services.data_processor import DataProcessor
from app.utils.error_handling import ErrorHandler, KPIError
from app.crud import (
    crud_kpi,
    crud_kpi_value,
    crud_sales_data,
    crud_cost_data,
    crud_marketing_data,
    crud_customer_data,
)


class KPICalculator:
    """
    Service for calculating KPIs from processed data.
    """

    def __init__(self):
        self.data_processor = DataProcessor()
        self.error_handler = ErrorHandler()

        self.calculations = {
            "revenue": RevenueCalculation(),
            "profit": ProfitCalculation(),
            "cac": CACCalculation(),
            "retention": RetentionCalculation(),
        }

    def calculate_kpi(
        self,
        kpi_type: str,
        db: Session,
        period_start: datetime,
        period_end: datetime,
    ) -> Dict[str, Any]:
        try:
            # --------------------------------------------------
            # Validate KPI type
            # --------------------------------------------------
            if kpi_type not in self.calculations:
                raise KPIError(
                    f"Unsupported KPI type: {kpi_type}",
                    "UNSUPPORTED_KPI",
                )

            calculation = self.calculations[kpi_type]
            required_fields = calculation.get_required_data_fields()
            data: Dict[str, Any] = {}

            # --------------------------------------------------
            # Fetch required data
            # --------------------------------------------------
            if "sales" in required_fields:
                data["sales"] = crud_sales_data.get_by_date_range(
                    db=db,
                    start_date=period_start,
                    end_date=period_end,
                )

            if "costs" in required_fields:
                data["costs"] = crud_cost_data.get_by_date_range(
                    db=db,
                    start_date=period_start,
                    end_date=period_end,
                )

            if "marketing" in required_fields:
                data["marketing"] = crud_marketing_data.get_by_date_range(
                    db=db,
                    start_date=period_start,
                    end_date=period_end,
                )

            if "customers" in required_fields:
                data["customers"] = {
                    "start": crud_customer_data.get_active_at_date(
                        db=db,
                        date=period_start,
                    ),
                    "all": crud_customer_data.get_by_date_range(
                        db=db,
                        start_date=period_start,
                        end_date=period_end,
                    ),
                }

            # --------------------------------------------------
            # Validate data
            # --------------------------------------------------
            self.data_processor.validate_data_for_kpi(
                data,
                required_fields,
            )

            # --------------------------------------------------
            # Calculate KPI
            # --------------------------------------------------
            result = calculation.calculate(
                data,
                period_start,
                period_end,
            )

            # --------------------------------------------------
            # Save KPI value to DB
            # --------------------------------------------------
            if "value" in result:
                kpi = crud_kpi.get_by_name(
                    db,
                    name=calculation.name,
                )

                if kpi:
                    from app.schemas.kpi import KPIValueCreate

                    kpi_value_create = KPIValueCreate(
                        kpi_id=kpi.id,                 # ✅ FIX
                        value=result["value"],
                        period_start=period_start,
                        period_end=period_end,
                        extra_data=result,
                    )

                    crud_kpi_value.create(
                        db=db,
                        obj_in=kpi_value_create,       # ✅ FIX
                    )

            # --------------------------------------------------
            # Enrich response
            # --------------------------------------------------
            result.update(
                {
                    "kpi_type": kpi_type,
                    "kpi_name": calculation.name,
                    "kpi_description": calculation.description,
                    "kpi_unit": calculation.unit,
                    "calculated_at": datetime.now().isoformat(),
                }
            )

            return result

        except KPIError:
            raise
        except Exception as e:
            error_info = self.error_handler.handle_calculation_error(
                e,
                kpi_type,
            )
            raise KPIError(
                error_info["message"],
                error_info["error_code"],
                error_info,
            )

    def calculate_all_kpis(
        self,
        db: Session,
        period_start: datetime,
        period_end: datetime,
    ) -> Dict[str, Any]:
        results = {}
        errors = {}

        for kpi_type in self.calculations:
            try:
                results[kpi_type] = self.calculate_kpi(
                    kpi_type,
                    db,
                    period_start,
                    period_end,
                )
            except KPIError as e:
                errors[kpi_type] = {
                    "error": True,
                    "message": str(e),
                    "error_code": e.error_code,
                }

        return {
            "results": results,
            "errors": errors,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "calculated_at": datetime.now().isoformat(),
        }
