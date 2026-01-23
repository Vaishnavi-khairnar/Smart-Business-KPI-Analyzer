from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.crud.user import crud_user
from app.schemas.user import UserCreate, UserRead
from app.utils.auth import (
    create_access_token,
    verify_password,
    get_password_hash,
    verify_token,
)
from app.utils.error_handling import ErrorHandler, KPIError
from app.core.config import settings


class AuthService:
    def __init__(self):
        self.error_handler = ErrorHandler()

    # =====================================================
    # AUTHENTICATE USER
    # =====================================================
    def authenticate_user(
        self, db: Session, username: str, password: str
    ) -> UserRead:
        try:
            # ✅ Try to find user by username first
            user = crud_user.get_by_username(db, username=username)
            
            # ✅ If not found, try by email (allows login with email)
            if not user:
                user = crud_user.get_by_email(db, email=username)

            if not user or not verify_password(password, user.hashed_password):
                raise KPIError(
                    "Invalid username or password",
                    "AUTHENTICATION_FAILED",
                )

            if not user.is_active:
                raise KPIError(
                    "User account is inactive",
                    "ACCOUNT_INACTIVE",
                )

            return UserRead.model_validate(user)

        except KPIError:
            raise
        except Exception as e:
            error_info = self.error_handler.handle_calculation_error(
                e, "authentication"
            )
            raise KPIError(
                error_info["message"],
                error_info["error_code"],
                error_info,
            )

    # =====================================================
    # CREATE USER
    # =====================================================
    def create_user(self, db: Session, user: UserCreate) -> UserRead:
        try:
            existing_user = crud_user.get_by_username(
                db, username=user.username
            )
            if existing_user:
                raise KPIError(
                    "Username already registered",
                    "USERNAME_EXISTS",
                )

            hashed_password = get_password_hash(user.password)

            db_user = crud_user.create(
                db=db,
                obj_in={
                    "username": user.username,
                    "email": user.email,
                    "hashed_password": hashed_password,
                    "is_active": True,
                    "is_superuser": False,
                },
            )

            return UserRead.model_validate(db_user)

        except KPIError:
            raise
        except Exception as e:
            error_info = self.error_handler.handle_calculation_error(
                e, "user_creation"
            )
            raise KPIError(
                error_info["message"],
                error_info["error_code"],
                error_info,
            )

    # =====================================================
    # GET CURRENT USER FROM TOKEN
    # =====================================================
    def get_current_user(self, token: str, db: Session) -> UserRead:
        try:
            payload = verify_token(token)
            if not payload or "sub" not in payload:
                raise KPIError("Invalid token", "INVALID_TOKEN")

            user_id = int(payload["sub"])

            user = crud_user.get(db, id=user_id)
            if not user:
                raise KPIError("User not found", "USER_NOT_FOUND")

            return UserRead.model_validate(user)

        except KPIError:
            raise
        except Exception as e:
            error_info = self.error_handler.handle_calculation_error(
                e, "token_verification"
            )
            raise KPIError(
                error_info["message"],
                error_info["error_code"],
                error_info,
            )
