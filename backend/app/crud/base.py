from typing import Any, Dict, Generic, List, Type, TypeVar, Union
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from app.core.database import Base
from pydantic import BaseModel
   
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
   
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
       def __init__(self, model: Type[ModelType]):
           self.model = model
       
       def get(self, db: Session, id: Any) -> ModelType:
           """
           Get a single record by ID.
           """
           return db.query(self.model).filter(self.model.id == id).first()
       
       def get_multi(
           self, db: Session, skip: int = 0, limit: int = 100
       ) -> List[ModelType]:
           """
           Get multiple records with pagination.
           """
           return db.query(self.model).offset(skip).limit(limit).all()
       
       def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
           """
           Create a new record.
           """
           try:
               obj_data = obj_in.dict()
               db_obj = self.model(**obj_data)
               db.add(db_obj)
               db.commit()
               db.refresh(db_obj)
               return db_obj
           except IntegrityError as e:
               db.rollback()
               raise HTTPException(
                   status_code=400,
                   detail=f"Integrity error: {str(e)}"
               )
       
       def update(
           self,
           db: Session,
           *,
           db_obj: ModelType,
           obj_in: Union[UpdateSchemaType, Dict[str, Any]]
       ) -> ModelType:
           """
           Update an existing record.
           """
           try:
               if isinstance(obj_in, dict):
                   update_data = obj_in
               else:
                   update_data = obj_in.dict(exclude_unset=True)
               
               for field, value in update_data.items():
                   setattr(db_obj, field, value)
               
               db.add(db_obj)
               db.commit()
               db.refresh(db_obj)
               return db_obj
           except IntegrityError as e:
               db.rollback()
               raise HTTPException(
                   status_code=400,
                   detail=f"Integrity error: {str(e)}"
               )
       
       def remove(self, db: Session, *, id: int) -> ModelType:
           """
           Delete a record by ID.
           """
           try:
               obj = db.query(self.model).get(id)
               if obj:
                   db.delete(obj)
                   db.commit()
               return obj
           except IntegrityError as e:
               db.rollback()
               raise HTTPException(
                   status_code=400,
                   detail=f"Integrity error: {str(e)}"
               )