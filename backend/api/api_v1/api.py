from fastapi import APIRouter

from api.endpoints import auth, kpis, data, business_units

api_router = APIRouter()

# Auth routes → /api/v1/auth
api_router.include_router(auth.router)

# KPI routes → /api/v1/kpis
api_router.include_router(kpis.router)

# Data routes → /api/v1/data
api_router.include_router(data.router)

# Business units → /api/v1/business-units
api_router.include_router(business_units.router)
