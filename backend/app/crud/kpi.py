from typing import List
from sqlalchemy.orm import Session

from app.models.database import KPI, KPIValue
from app.schemas.kpi import KPICreate, KPIUpdate, KPIRead, KPIValueCreate

from .base import CRUDBase


class CRUDKPI(CRUDBase[KPI, KPICreate, KPIUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> KPI | None:
        """
        Get KPI by name.
        """
        return db.query(KPI).filter(KPI.name == name).first()


class CRUDKPIValue(CRUDBase[KPIValue, KPIValueCreate, dict]):
    def get_by_kpi_id(
        self,
        db: Session,
        kpi_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[KPIValue]:
        """
        Get KPI values by KPI ID with pagination.
        """
        return (
            db.query(KPIValue)
            .filter(KPIValue.kpi_id == kpi_id)
            .order_by(KPIValue.period_end.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_kpi(
        self,
        db: Session,
        *,
        obj_in: KPIValueCreate,
        kpi_id: int,
    ) -> KPIValue:
        """
        Create a new KPI value associated with a KPI.
        """
        obj_data = obj_in.dict()
        obj_data["kpi_id"] = kpi_id
        return super().create(db, obj_in=obj_data)


# Create CRUD instances
crud_kpi = CRUDKPI(KPI)
crud_kpi_value = CRUDKPIValue(KPIValue)
