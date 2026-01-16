from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import crud_kpi
from app.schemas.kpi import (
    KPICreate,
    KPIUpdate,
    KPIRead,
    KPICalculationRequest,
    AllKPICalculationRequest,
)
from app.schemas.responses import KPIResponse, KPIListResponse
from app.services.kpi_calculator import KPICalculator
from app.utils.error_handling import KPIError

router = APIRouter(prefix="/kpis", tags=["KPIs"])


# =====================================================
# GET KPI TYPES  (⚠ MUST BE FIRST)
# =====================================================
@router.get("/types")
async def get_kpi_types():
    """
    Returns available KPI types
    """
    return {
        "message": "KPI types retrieved successfully",
        "data": [
            "Financial",
            "Operational",
            "HR",
            "Sales",
            "Customer",
        ],
    }


# =====================================================
# GET ALL KPIs
# =====================================================
@router.get("/", response_model=KPIListResponse)
async def get_all_kpis(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    try:
        kpis = crud_kpi.get_multi(db, skip=skip, limit=limit)

        return KPIListResponse(
            message="KPIs retrieved successfully",
            data=[KPIRead.model_validate(kpi) for kpi in kpis],
            count=len(kpis),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# GET SINGLE KPI
# =====================================================
@router.get("/{kpi_id}", response_model=KPIResponse)
async def get_kpi(kpi_id: int, db: Session = Depends(get_db)):
    kpi = crud_kpi.get(db, id=kpi_id)

    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")

    return KPIResponse(
        message="KPI retrieved successfully",
        data=KPIRead.model_validate(kpi),
    )


# =====================================================
# CREATE KPI
# =====================================================
@router.post("/", response_model=KPIResponse)
async def create_kpi(
    kpi: KPICreate,
    db: Session = Depends(get_db),
):
    try:
        created_kpi = crud_kpi.create(db, obj_in=kpi)

        return KPIResponse(
            message="KPI created successfully",
            data=KPIRead.model_validate(created_kpi),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =====================================================
# UPDATE KPI
# =====================================================
@router.put("/{kpi_id}", response_model=KPIResponse)
async def update_kpi(
    kpi_id: int,
    kpi_update: KPIUpdate,
    db: Session = Depends(get_db),
):
    kpi = crud_kpi.get(db, id=kpi_id)

    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")

    try:
        updated_kpi = crud_kpi.update(db, db_obj=kpi, obj_in=kpi_update)

        return KPIResponse(
            message="KPI updated successfully",
            data=KPIRead.model_validate(updated_kpi),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =====================================================
# DELETE KPI
# =====================================================
@router.delete("/{kpi_id}", response_model=KPIResponse)
async def delete_kpi(kpi_id: int, db: Session = Depends(get_db)):
    kpi = crud_kpi.get(db, id=kpi_id)

    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")

    crud_kpi.remove(db, id=kpi_id)

    return KPIResponse(
        message="KPI deleted successfully",
        data={"id": kpi_id},
    )


# =====================================================
# CALCULATE SINGLE KPI
# =====================================================
@router.post("/calculate", response_model=KPIResponse)
async def calculate_kpi(
    request: KPICalculationRequest,
    db: Session = Depends(get_db),
):
    try:
        calculator = KPICalculator()

        result = calculator.calculate_kpi(
            kpi_type=request.kpi_type,
            db=db,
            period_start=request.period_start,
            period_end=request.period_end,
        )

        return KPIResponse(
            message="KPI calculated successfully",
            data=result,
        )

    except KPIError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# CALCULATE ALL KPIs
# =====================================================
@router.post("/calculate-all", response_model=KPIResponse)
async def calculate_all_kpis(
    request: AllKPICalculationRequest,
    db: Session = Depends(get_db),
):
    try:
        calculator = KPICalculator()

        result = calculator.calculate_all_kpis(
            db=db,
            period_start=request.period_start,
            period_end=request.period_end,
        )

        return KPIResponse(
            message="All KPIs calculated successfully",
            data=result,
        )

    except KPIError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
