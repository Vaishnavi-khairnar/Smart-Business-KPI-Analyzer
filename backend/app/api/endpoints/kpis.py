from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.kpi import KPI, KPICreate, KPIUpdate, KPIWithValues
from app.schemas.kpi import KPIResponse, KPIListResponse, ErrorResponse
from datetime import datetime 
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