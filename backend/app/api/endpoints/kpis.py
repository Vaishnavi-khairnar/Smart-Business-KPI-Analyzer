from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field
from pydantic_settings import BaseSettings
from app.schemas.responses import KPIResponse, KPIListResponse
from app.services.kpi_calculator import KPICalculator
from app.services.data_processor import DataProcessor
from app.utils.error_handling import ErrorHandler, KPIError
import pandas as pd

router = APIRouter()
# Temporary in-memory storage (will be replaced with database in Day 04)
kpi_storage = {}
kpi_id_counter = 1

@router.get("/", response_model=KPIListResponse)
async def get_all_kpis():
       """
       Retrieve all available KPIs.
       """
       try:
           kpis = list(kpi_storage.values())
           return KPIListResponse(
               message="KPIs retrieved successfully",
               data=kpis,
               count=len(kpis)
           )
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

@router.get("/{kpi_id}", response_model=KPIResponse)
async def get_kpi(kpi_id: int):
       """
       Retrieve a specific KPI by ID.
       """
       try:
           if kpi_id not in kpi_storage:
               raise HTTPException(status_code=404, detail="KPI not found")
           
           kpi = kpi_storage[kpi_id]
           return KPIResponse(
               message="KPI retrieved successfully",
               data=kpi
           )
       except HTTPException:
           raise
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=KPIResponse)
async def create_kpi(kpi: KPICreate):
       """
       Create a new KPI.
       """
       global kpi_id_counter
       
       try:
           # Create a new KPI with generated ID and timestamps
           new_kpi = KPI(
               id=kpi_id_counter,
               name=kpi.name,
               description=kpi.description,
               unit=kpi.unit,
               formula=kpi.formula,
               created_at=datetime.now(),
               updated_at=datetime.now()
           )
           
           # Store the KPI
           kpi_storage[kpi_id_counter] = new_kpi
           kpi_id_counter += 1
           
           return KPIResponse(
               message="KPI created successfully",
               data=new_kpi
           )
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

@router.put("/{kpi_id}", response_model=KPIResponse)
async def update_kpi(kpi_id: int, kpi_update: KPIUpdate):
       """
       Update an existing KPI.
       """
       try:
           if kpi_id not in kpi_storage:
               raise HTTPException(status_code=404, detail="KPI not found")
           
           # Get the existing KPI
           existing_kpi = kpi_storage[kpi_id]
           
           # Update fields if provided
           update_data = kpi_update.dict(exclude_unset=True)
           for field, value in update_data.items():
               setattr(existing_kpi, field, value)
           
           # Update the timestamp
           existing_kpi.updated_at = datetime.now()
           
           return KPIResponse(
               message="KPI updated successfully",
               data=existing_kpi
           )
       except HTTPException:
           raise
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{kpi_id}", response_model=KPIResponse)
async def delete_kpi(kpi_id: int):
       """
       Delete a KPI.
       """
       try:
           if kpi_id not in kpi_storage:
               raise HTTPException(status_code=404, detail="KPI not found")
           
           # Remove the KPI
           deleted_kpi = kpi_storage.pop(kpi_id)
           
           return KPIResponse(
               message="KPI deleted successfully",
               data=deleted_kpi
           )
       except HTTPException:
           raise
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))
       
       class KPICalculationRequest(BaseModel):
            kpi_type: str = Field(..., description="Type of KPI to calculate")
            period_start: datetime = Field(..., description="Start date for calculation period")
            period_end: datetime = Field(..., description="End date for calculation period")
       
       class Config:
           schema_extra = {
               "example": {
                   "kpi_type": "revenue",
                   "period_start": "2023-01-01T00:00:00",
                   "period_end": "2023-01-31T23:59:59"
               }
           }

class AllKPICalculationRequest(BaseModel):
       period_start: datetime = Field(..., description="Start date for calculation period")
       period_end: datetime = Field(..., description="End date for calculation period")
       
       class Config:
           schema_extra = {
               "example": {
                   "period_start": "2023-01-01T00:00:00",
                   "period_end": "2023-01-31T23:59:59"
               }
           }

class DataUploadRequest(BaseModel):
       data_type: str = Field(..., description="Type of data (sales, costs, marketing, customers)")
       data_format: str = Field(..., description="Format of data (csv, excel, json)")
       data: str = Field(..., description="Data content")
       
       class Config:
           schema_extra = {
               "example": {
                   "data_type": "sales",
                   "data_format": "csv",
                   "data": "date,amount,product_id\n2023-01-01,100.00,PROD001"
               }
           }

   # Add these endpoint functions after the existing CRUD endpoints
@router.get("/available", response_model=KPIResponse)
async def get_available_kpis():
       """
       Get information about available KPI calculations.
       """
       try:
           calculator = KPICalculator()
           kpis = calculator.get_available_kpis()
           
           return KPIResponse(
               message="Available KPIs retrieved successfully",
               data=kpis
           )
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate", response_model=KPIResponse)
async def calculate_kpi(request: KPICalculationRequest):
       """
       Calculate a specific KPI.
       """
       try:
           calculator = KPICalculator()
           
           # For now, we'll use sample data
           # In Day 04, we'll replace this with data from the database
           sample_data = get_sample_data()
           
           result = calculator.calculate_kpi(
               request.kpi_type,
               sample_data,
               request.period_start,
               request.period_end
           )
           
           return KPIResponse(
               message="KPI calculated successfully",
               data=result
           )
       except KPIError as e:
           raise HTTPException(status_code=400, detail=str(e))
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate-all", response_model=KPIResponse)
async def calculate_all_kpis(request: AllKPICalculationRequest):
       """
       Calculate all available KPIs.
       """
       try:
           calculator = KPICalculator()
           
           # For now, we'll use sample data
           # In Day 04, we'll replace this with data from the database
           sample_data = get_sample_data()
           
           result = calculator.calculate_all_kpis(
               sample_data,
               request.period_start,
               request.period_end
           )
           
           return KPIResponse(
               message="All KPIs calculated successfully",
               data=result
           )
       except KPIError as e:
           raise HTTPException(status_code=400, detail=str(e))
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

   # Add this helper function at the end of the file
def get_sample_data() -> Dict[str, pd.DataFrame]:
       """
       Generate sample data for testing KPI calculations.
       This will be replaced with actual data from the database in Day 04.
       """
       import numpy as np
       from datetime import timedelta
       
       # Generate date range
       start_date = datetime(2023, 1, 1)
       end_date = datetime(2023, 12, 31)
       date_range = pd.date_range(start=start_date, end=end_date, freq='D')
       
       # Sample sales data
       sales_data = []
       for date in date_range:
           # Random number of transactions per day (1-10)
           num_transactions = np.random.randint(1, 11)
           for _ in range(num_transactions):
               sales_data.append({
                   'date': date,
                   'amount': np.random.uniform(10, 500),
                   'product_id': f'PROD{np.random.randint(1, 101):03d}'
               })
       
       sales_df = pd.DataFrame(sales_data)
       
       # Sample cost data
       cost_data = []
       for date in date_range:
           # Random costs per day (5-20)
           num_costs = np.random.randint(5, 21)
           for _ in range(num_costs):
               cost_data.append({
                   'date': date,
                   'amount': np.random.uniform(5, 200),
                   'cost_category': np.random.choice(['Operations', 'Marketing', 'Admin', 'R&D'])
               })
       
       costs_df = pd.DataFrame(cost_data)
       
       # Sample marketing data
       marketing_data = []
       for date in date_range:
           # Marketing campaigns (0-2 per day)
           if np.random.random() > 0.7:  # 30% chance of marketing activity
               num_campaigns = np.random.randint(1, 3)
               for _ in range(num_campaigns):
                   marketing_data.append({
                       'date': date,
                       'amount': np.random.uniform(100, 1000),
                       'campaign_type': np.random.choice(['Online', 'Print', 'TV', 'Radio'])
                   })
       
       marketing_df = pd.DataFrame(marketing_data)
       
       # Sample customer data
       customer_data = []
       customer_id = 1
       
       # Generate customers over time
       for date in date_range:
           # New customers (0-5 per day)
           new_customers = np.random.randint(0, 6)
           for _ in range(new_customers):
               signup_date = date
               # Last activity date (sometime between signup and now)
               last_activity = signup_date + timedelta(days=np.random.randint(0, 90))
               if last_activity > end_date:
                   last_activity = end_date
               
               customer_data.append({
                   'customer_id': customer_id,
                   'signup_date': signup_date,
                   'last_activity_date': last_activity
               })
               customer_id += 1
       
       customers_df = pd.DataFrame(customer_data)
       
       return {
           'sales': sales_df,
           'costs': costs_df,
           'marketing': marketing_df,
           'customers': customers_df
       }