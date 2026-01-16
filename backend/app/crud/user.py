from sqlalchemy.orm import Session
from app.models.user import User
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, dict, dict]):

    def get_by_username(self, db: Session, *, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, *, email: str):
        return db.query(User).filter(User.email == email).first()

    # ✅ OVERRIDE CREATE (CRITICAL FIX)
    def create(self, db: Session, *, obj_in):
        """
        Create a user.
        Supports dict, Pydantic v1, and Pydantic v2 inputs.
        """

        if hasattr(obj_in, "model_dump"):        # Pydantic v2
            obj_data = obj_in.model_dump()
        elif hasattr(obj_in, "dict"):            # Pydantic v1
            obj_data = obj_in.dict()
        else:                                    # already dict
            obj_data = obj_in

        db_obj = User(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_user = CRUDUser(User)
