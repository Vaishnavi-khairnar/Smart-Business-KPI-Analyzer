import pytest
from sqlalchemy.orm import Session

# Import all SQLAlchemy models to ensure they're registered with the Base
import app.models.user
import app.models.kpi_model
import app.models.kpi_value
import app.models.business_unit
import app.models.customer
import app.models.sale
import app.models.cost
import app.models.marketing_spend

from app.core.database import SessionLocal, engine, Base

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
