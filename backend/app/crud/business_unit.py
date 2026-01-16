from sqlalchemy.orm import Session
from app.models.business_unit import BusinessUnit


def get_active_business_units(db: Session):
    return (
        db.query(BusinessUnit)
        .filter(BusinessUnit.is_active == True)
        .order_by(BusinessUnit.name)
        .all()
    )
