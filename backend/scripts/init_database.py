import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
   
from app.core.init_db import init_db
   
if __name__ == "__main__":
       print("Initializing database...")
       init_db()
       print("Database initialized successfully!")