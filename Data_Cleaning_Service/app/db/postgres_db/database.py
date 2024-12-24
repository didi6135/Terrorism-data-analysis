import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from psycopg2 import connect, sql
from psycopg2.errors import DuplicateDatabase
from Data_Cleaning_Service.app.db.postgres_db.models import Base
from Data_Cleaning_Service.app.utils.logger import log
from dotenv import load_dotenv

load_dotenv(verbose=True)

POSTGRES_URL = os.getenv("POSTGRES_URI")
POSTGRES_DB = os.getenv("POSTGRES_DB", "terrorism_data_analysis")  # Default DB name
engine = create_engine(POSTGRES_URL)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database():
    """Create the database if it does not exist."""
    try:
        # Extract connection parameters
        db_url_parts = POSTGRES_URL.rsplit("/", 1)
        base_url = db_url_parts[0]
        db_name = POSTGRES_DB

        log(f"Checking if database '{db_name}' exists...")

        # Connect to the base PostgreSQL instance
        with connect(dsn=base_url) as conn:
            conn.set_isolation_level(0)  # Disable transactions for this connection
            with conn.cursor() as cur:
                try:
                    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                    log(f"Database '{db_name}' created successfully.")
                except DuplicateDatabase:
                    log(f"Database '{db_name}' already exists. Skipping creation.")
    except Exception as e:
        log(f"Error creating database '{db_name}': {e}", level="error")




def create_tables():
    """Create all tables in the database."""
    try:
        log("Creating tables in the database...")
        Base.metadata.create_all(bind=engine)
        log("Tables created successfully.")
    except Exception as e:
        log(f"Error creating tables: {e}", level="error")

if __name__ == "__main__":
    create_database()
    create_tables()
