from .kpis import router as kpis_router
from .data import router as data_router
from fastapi import APIRouter

   
api_router = APIRouter()
api_router.include_router(kpis_router, prefix="/kpis", tags=["KPIs"])
api_router.include_router(data_router, prefix="/data", tags=["Data Upload"])