from Data_Cleaning_Service.app.models import Event
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_new_event(event):
    return PostgresCRUD.insert(event, Event)
