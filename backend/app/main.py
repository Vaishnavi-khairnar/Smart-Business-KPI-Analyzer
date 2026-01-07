from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import kpis
from app.core.config import settings

app = FastAPI(
       title="Smart Business KPI Analyzer API",
       description="API for calculating and analyzing business KPIs",
       version="1.0.0",
   )

   # Configure CORS
app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:8501"],  # Streamlit default port
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )

   # Include API routers
app.include_router(kpis.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
       """
       Root endpoint to check if the API is running.
       """
       return {"message": "Smart Business KPI Analyzer API is running"}

@app.get("/health", tags=["Health"])
async def health_check():
       """
       Health check endpoint for monitoring.
       """
       return {"status": "healthy", "service": "KPI Analyzer API"}