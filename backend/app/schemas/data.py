from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
   
class DataUploadResponse(BaseModel):
       success: bool = True
       message: str
       records_processed: int
       errors: Optional[list] = None
       timestamp: datetime = Field(default_factory=datetime.now)
   
class SalesDataCreate(BaseModel):
       date: datetime
       amount: float
       product_id: Optional[str] = None
       customer_id: Optional[int] = None
       region: Optional[str] = None
   
class CostDataCreate(BaseModel):
       date: datetime
       amount: float
       cost_category: Optional[str] = None
       department: Optional[str] = None
       description: Optional[str] = None
   
class MarketingDataCreate(BaseModel):
       date: datetime
       amount: float
       campaign_type: Optional[str] = None
       campaign_name: Optional[str] = None
       channel: Optional[str] = None
   
class CustomerDataCreate(BaseModel):
       customer_id: int
       name: Optional[str] = None
       email: Optional[str] = None
       signup_date: datetime
       last_activity_date: Optional[datetime] = None
       total_purchases: Optional[float] = 0.0
       total_value: Optional[float] = 0.0
       region: Optional[str] = None