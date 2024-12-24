import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from psycopg2 import connect, sql
from psycopg2.errors import DuplicateDatabase
from sqlalchemy_utils import database_exists, create_database

from Data_Cleaning_Service.app.db.postgres_db.models import Base
from Data_Cleaning_Service.app.utils.logger import log
from dotenv import load_dotenv

load_dotenv(verbose=True)

POSTGRES_URL = os.getenv("POSTGRES_URI")
POSTGRES_DB = os.getenv("POSTGRES_DB", "terrorism_data_analysis")  # Default DB name
engine = create_engine(POSTGRES_URL)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    """Create the database if it does not exist."""
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            log("Database created successfully")
            create_tables()
            return
        log('Database already exists')
        return

    except Exception as e:
        log(f"Error creating database terrorism_data_analysis: {e}", level="error")




def create_tables():
    """Create all tables in the database."""
    try:
        log("Creating tables in the database...")
        Base.metadata.create_all(bind=engine)
        log("Tables created successfully.")
    except Exception as e:
        log(f"Error creating tables: {e}", level="error")


