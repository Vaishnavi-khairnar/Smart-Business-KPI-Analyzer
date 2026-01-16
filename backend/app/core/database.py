from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# =====================================================
# DATABASE ENGINE
# =====================================================
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

print("🚨 DATABASE URL:", engine.url)

# =====================================================
# SESSION
# =====================================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# =====================================================
# BASE (DECLARE ONLY ONCE)
# =====================================================
Base = declarative_base()

# =====================================================
# DEPENDENCY
# =====================================================
def get_db():
    """
    FastAPI dependency to get a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()