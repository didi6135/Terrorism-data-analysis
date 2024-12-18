from data_cleaning.app.models import Event
from data_cleaning.app.utils.generic_for_postgres import PostgresCRUD


def insert_new_event(event):
    return PostgresCRUD.insert(event, Event)
