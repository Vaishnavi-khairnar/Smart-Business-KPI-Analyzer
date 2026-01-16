from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.database import KPI, KPIValue
from app.schemas.kpi import KPICreate, KPIUpdate, KPIValueCreate
from .base import CRUDBase


# =====================================================
# KPI CRUD
# =====================================================
class CRUDKPI(CRUDBase[KPI, KPICreate, KPIUpdate]):

    def get_by_name(self, db: Session, *, name: str) -> KPI | None:
        """
        Get KPI by name.
        """
        return db.query(KPI).filter(KPI.name == name).first()

    def create(self, db: Session, *, obj_in: KPICreate) -> KPI:
        """
        Create a new KPI.
        """
        try:
            # ✅ Convert Pydantic model → dict (Pydantic v2)
            obj_data = obj_in.model_dump()

            db_obj = self.model(**obj_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="KPI with this name already exists"
            )


# =====================================================
# KPI VALUE CRUD
# =====================================================
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
        obj_data = obj_in.model_dump()
        obj_data["kpi_id"] = kpi_id

        return super().create(db, obj_in=obj_data)


# =====================================================
# CRUD INSTANCES
# =====================================================
crud_kpi = CRUDKPI(KPI)
crud_kpi_value = CRUDKPIValue(KPIValue)
