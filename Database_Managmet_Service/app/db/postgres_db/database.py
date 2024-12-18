import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Data_Cleaning_Service.app.models import Base
from Data_Cleaning_Service.app.utils.logger import log

from dotenv import load_dotenv

load_dotenv(verbose=True)

POSTGRES_URL = os.getenv('POSTGRES_URI')
engine = create_engine(POSTGRES_URL)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all tables in the database."""
    try:
        log('drop all tables')
        Base.metadata.drop_all(engine)

        log("Creating tables in the database...")
        Base.metadata.create_all(bind=engine)
        log("Tables created successfully.")
    except Exception as e:
        log(f"Error creating tables: {e}", level="error")

if __name__ == "__main__":
    create_tables()
