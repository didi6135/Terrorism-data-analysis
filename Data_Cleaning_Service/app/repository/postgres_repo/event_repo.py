from Data_Cleaning_Service.app.db.postgres_db.models import Event
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_new_event(event):
    return PostgresCRUD.insert(event, Event)
