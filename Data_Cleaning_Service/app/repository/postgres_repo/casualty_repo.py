from Data_Cleaning_Service.app.db.postgres_db.models import Casualty
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_new_casualty(casualty):
    """
    Insert a casualty entity.
    """
    return PostgresCRUD.insert(casualty, Casualty)
