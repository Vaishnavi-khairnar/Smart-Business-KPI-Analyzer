from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
   
class UserBase(BaseModel):
       username: str = Field(..., min_length=3, max_length=50)
       email: EmailStr = Field(...)
       is_active: bool = True
       is_superuser: bool = False
   
class UserCreate(UserBase):
       password: str = Field(..., min_length=8)
   
class UserUpdate(BaseModel):
       username: Optional[str] = Field(None, min_length=3, max_length=50)
       email: Optional[EmailStr] = Field(None)
       is_active: Optional[bool] = Field(None)
       is_superuser: Optional[bool] = Field(None)
   
class UserResponse(BaseModel):
       id: int
       username: str
       email: str
       is_active: bool
       is_superuser: bool
       created_at: datetime
       updated_at: datetime
   
class UserLogin(BaseModel):
       username: str
       password: str
   
class Token(BaseModel):
       access_token: str
       token_type: str = "bearer"
       expires_in: int