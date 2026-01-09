from app.core.database import engine, Base
from app.models import *  # Import all models
   
def init_db():
       """
       Initialize database with all tables.
       """
       Base.metadata.create_all(bind=engine)
   
def drop_db():
       """
       Drop all database tables.
       """
       Base.metadata.drop_all(bind=engine)
   
def reset_db():
       """
       Reset database by dropping and recreating all tables.
       """
       drop_db()
       init_db()