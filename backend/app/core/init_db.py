from app.core.database import engine, Base
from app.models import *  # Import all models
   
def init_db():
       """
       Initialize database with all tables.
       """
       Base.metadata.create_all(bind=engine)
   