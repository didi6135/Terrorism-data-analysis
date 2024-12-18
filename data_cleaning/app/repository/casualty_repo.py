from data_cleaning.app.models import Casualty
from data_cleaning.app.utils.generic_for_postgres import PostgresCRUD


def insert_new_casualty(casualty):
    """
    Insert a casualty entity.
    """
    return PostgresCRUD.insert(casualty, Casualty)
