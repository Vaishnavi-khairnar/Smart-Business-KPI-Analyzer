from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.models.database import KPI, KPIValue
from app.schemas.kpi import KPICreate, KPIUpdate, KPIRead, KPIValueCreate

from .base import CRUDBase


class CRUDKPI(CRUDBase[KPI, KPICreate, KPIUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> KPI | None:
        """
        Get KPI by name.
        """
        return db.query(KPI).filter(KPI.name == name).first()
    
    def get_by_username(self, db: Session, *, username: str):
       """
       Get a user by username.
       """
       return db.query(self.model).filter(self.model.username == username).first()
   
    def create(self, db: Session, *, obj_in: dict):
       """
       Create a new user.
       """
       try:
           obj_data = obj_in.copy()
           
           # Hash password if provided
           if "password" in obj_data:
               from app.utils.auth import get_password_hash
               obj_data["hashed_password"] = get_password_hash(obj_data["password"])
               # Remove plain password from stored data
               del obj_data["password"]
           
           db_obj = self.model(**obj_data)
           db.add(db_obj)
           db.commit()
           db.refresh(db_obj)
           return db_obj
       except IntegrityError as e: # pyright: ignore[reportUndefinedVariable]
           db.rollback()
           raise HTTPException(
               status_code=400,
               detail=f"Integrity error: {str(e)}"
           )


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
