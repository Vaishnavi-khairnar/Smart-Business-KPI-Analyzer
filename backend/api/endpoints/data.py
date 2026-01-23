from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from io import StringIO
from datetime import datetime
   
from app.core.database import get_db
from app.crud import crud_sales_data, crud_cost_data, crud_marketing_data, crud_customer_data
from app.schemas.data import (
       DataUploadResponse, SalesDataCreate, CostDataCreate, 
       MarketingDataCreate, CustomerDataCreate
   )
from app.services.data_processor import DataProcessor
from app.utils.error_handling import ErrorHandler, KPIError
   
router = APIRouter(prefix="/data", tags=["Data"])
   
@router.post("/upload/sales", response_model=DataUploadResponse)
async def upload_sales_data(
       file: UploadFile = File(...), db: Session = Depends(get_db)
   ):
       """
       Upload sales data from CSV file.
       """
       try:
           # Read file content
           contents = await file.read()
           
           # Process CSV data
           processor = DataProcessor()
           df = processor.process_csv_data(contents.decode("utf-8"), "sales")
           
           # Convert DataFrame to list of dictionaries
           sales_data = df.to_dict(orient="records")
           
           # Create records in database
           created_count = 0
           errors = []
           
           for data in sales_data:
               try:
                   sales_create = SalesDataCreate(**data)
                   crud_sales_data.create(db, obj_in=sales_create)
                   created_count += 1
               except Exception as e:
                   errors.append(f"Error processing record: {str(e)}")
           
           return DataUploadResponse(
               message=f"Uploaded {created_count} sales records successfully",
               records_processed=created_count,
               errors=errors if errors else None
           )
           
       except Exception as e:
           raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
   
@router.post("/upload/costs", response_model=DataUploadResponse)
async def upload_cost_data(
       file: UploadFile = File(...), db: Session = Depends(get_db)
   ):
       """
       Upload cost data from CSV file.
       """
       try:
           # Read file content
           contents = await file.read()
           
           # Process CSV data
           processor = DataProcessor()
           df = processor.process_csv_data(contents.decode("utf-8"), "costs")
           
           # Convert DataFrame to list of dictionaries
           cost_data = df.to_dict(orient="records")
           
           # Create records in database
           created_count = 0
           errors = []
           
           for data in cost_data:
               try:
                   cost_create = CostDataCreate(**data)
                   crud_cost_data.create(db, obj_in=cost_create)
                   created_count += 1
               except Exception as e:
                   errors.append(f"Error processing record: {str(e)}")
           
           return DataUploadResponse(
               message=f"Uploaded {created_count} cost records successfully",
               records_processed=created_count,
               errors=errors if errors else None
           )
           
       except Exception as e:
           raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
   
@router.post("/upload/marketing", response_model=DataUploadResponse)
async def upload_marketing_data(
       file: UploadFile = File(...), db: Session = Depends(get_db)
   ):
       """
       Upload marketing data from CSV file.
       """
       try:
           # Read file content
           contents = await file.read()
           
           # Process CSV data
           processor = DataProcessor()
           df = processor.process_csv_data(contents.decode("utf-8"), "marketing")
           
           # Convert DataFrame to list of dictionaries
           marketing_data = df.to_dict(orient="records")
           
           # Create records in database
           created_count = 0
           errors = []
           
           for data in marketing_data:
               try:
                   marketing_create = MarketingDataCreate(**data)
                   crud_marketing_data.create(db, obj_in=marketing_create)
                   created_count += 1
               except Exception as e:
                   errors.append(f"Error processing record: {str(e)}")
           
           return DataUploadResponse(
               message=f"Uploaded {created_count} marketing records successfully",
               records_processed=created_count,
               errors=errors if errors else None
           )
           
       except Exception as e:
           raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
   
@router.post("/upload/customers", response_model=DataUploadResponse)
async def upload_customer_data(
       file: UploadFile = File(...), db: Session = Depends(get_db)
   ):
       """
       Upload customer data from CSV file.
       """
       try:
           # Read file content
           contents = await file.read()
           
           # Process CSV data
           processor = DataProcessor()
           df = processor.process_csv_data(contents.decode("utf-8"), "customers")
           
           # Convert DataFrame to list of dictionaries
           customer_data = df.to_dict(orient="records")
           
           # Create records in database
           created_count = 0
           errors = []
           
           for data in customer_data:
               try:
                   customer_create = CustomerDataCreate(**data)
                   crud_customer_data.create(db, obj_in=customer_create)
                   created_count += 1
               except Exception as e:
                   errors.append(f"Error processing record: {str(e)}")
           
           return DataUploadResponse(
               message=f"Uploaded {created_count} customer records successfully",
               records_processed=created_count,
               errors=errors if errors else None
           )
           
       except Exception as e:
           raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")