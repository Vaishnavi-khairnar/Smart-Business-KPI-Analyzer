from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.schemas.auth import AuthResponse
from app.services.auth import AuthService
from app.utils.error_handling import KPIError
from app.utils.auth import create_access_token

# 🔐 OAuth2 scheme (standard)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# =====================================================
# REGISTER
# =====================================================
@router.post("/register", response_model=AuthResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService()
        user_response = auth_service.create_user(db, user)

        return {
            "message": "User registered successfully",
            "data": user_response.model_dump(),
        }

    except KPIError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# LOGIN
# =====================================================
@router.post("/login", response_model=AuthResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService()
        user_response = auth_service.authenticate_user(
            db, user.username, user.password
        )

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user_response.id)},
            expires_delta=access_token_expires,
        )

        return {
            "message": "Login successful",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": 1800,
                "user": user_response.model_dump(),
            },
        }

    except KPIError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# REFRESH TOKEN
# =====================================================
@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        auth_service = AuthService()
        user_response = auth_service.get_current_user(token, db)

        new_access_token = create_access_token(
            data={"sub": str(user_response.id)},
            expires_delta=timedelta(minutes=30),
        )

        return {
            "message": "Token refreshed successfully",
            "data": {
                "access_token": new_access_token,
                "token_type": "bearer",
                "expires_in": 1800,
                "user": user_response.model_dump(),
            },
        }

    except KPIError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# ME (CURRENT USER)
# =====================================================
@router.get("/me", response_model=AuthResponse)
async def me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        auth_service = AuthService()
        user_response = auth_service.get_current_user(token, db)

        return {
            "message": "User retrieved successfully",
            "data": user_response.model_dump(),
        }

    except KPIError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
