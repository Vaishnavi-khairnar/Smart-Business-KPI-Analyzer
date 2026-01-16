from fastapi import FastAPI
from app.core.database import Base, engine

# Import all SQLAlchemy models to ensure they're registered
import app.models.user
import app.models.kpi_model
import app.models.kpi_value
import app.models.business_unit
import app.models.customer
import app.models.sale
import app.models.cost
import app.models.marketing_spend

from api.endpoints import auth, kpis, data

app = FastAPI(title="KPI Analyzer API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(kpis.router, prefix="/api/v1")
app.include_router(data.router, prefix="/api/v1")
