from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import kpis, data 
from app.api import dashboard
from app.database import engine, Base
from app.api.endpoints import auth
from app.api.api_v1.api import api_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPI Analyzer API",
    description="API for KPI analytics and business intelligence",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_V1_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_V1_PREFIX)
app.include_router(kpis.router, prefix=API_V1_PREFIX)
app.include_router(data.router, prefix=API_V1_PREFIX)
app.include_router(dashboard.router, prefix=API_V1_PREFIX)
app.include_router(api_router, prefix=API_V1_PREFIX)

@app.get("/")
def root():
    return {"message": "KPI Analyzer API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}