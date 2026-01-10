from sqlite3 import dbapi2
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from app.core.database import get_db
from app.models.user import UserResponse
from app.services.auth import AuthService
from app.utils.error_handling import KPIError
   
   # Security scheme
security = HTTPBearer()
   
def get_current_user_token(token: str = Depends(security)):
       """
       Get the current user from a JWT token.
       """
       credentials_exception = HTTPException(
           status_code=status.HTTP_403_FORBIDDEN,
           detail="Could not validate credentials",
           headers={"WWW-Authenticate": "Bearer"},
       )
       
       try:
           # Verify token
           auth_service = AuthService()
           user = auth_service.get_current_user(token, dbapi2)
           
           if user is None:
               raise credentials_exception
           
           return user
       except JWTError:
           raise credentials_exception
       except KPIError as e:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail=str(e),
               headers={"WWW-Authenticate": "Bearer"},
           )
   
def get_current_active_user(
       current_user: UserResponse = Depends(get_current_user_token)
   ):
       """
       Get the current active user.
       """
       if not current_user.is_active:
           raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Inactive user"
           )
       
       return current_user