from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import api_router
from app.core.init_db import init_db
from app.core.database import SessionLocal
from app.crud.user import crud_user
from app.schemas.user import UserCreate
from app.utils.auth import get_password_hash

app = FastAPI(
    title="Smart Business KPI Analyzer API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """
    1️⃣ Create database tables
    2️⃣ Create default admin user
    """

    # =====================================================
    # STEP 1: Create tables
    # =====================================================
    init_db()
    print("Database initialized successfully!")

    # =====================================================
    # STEP 2: Create default admin user
    # =====================================================
    db = SessionLocal()
    try:
        admin_user = crud_user.get_by_username(db, username="admin")

        if not admin_user:
            admin_data = UserCreate(
                username="admin",
                email="admin@example.com",
                password="Admin@12345",  # ✅ >= 8 chars, bcrypt-safe
            )

            crud_user.create(
                db=db,
                obj_in={
                    "username": admin_data.username,
                    "email": admin_data.email,
                    "hashed_password": get_password_hash(admin_data.password),
                    "is_active": True,
                    "is_superuser": True,
                },
            )

            print("✅ Default admin user created")
        else:
            print("ℹ️ Admin user already exists")

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
    finally:
        db.close()
