from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.business_unit import BusinessUnitResponse
from app.crud.business_unit import get_active_business_units

router = APIRouter(prefix="/business-units", tags=["Business Units"])


@router.get("/", response_model=List[BusinessUnitResponse])
def list_business_units(db: Session = Depends(get_db)):
    return get_active_business_units(db)
