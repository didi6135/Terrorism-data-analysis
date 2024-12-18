from data_cleaning.app.models import EventType
from data_cleaning.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_event_type(name, details=None):
    """
    Insert a new event type or retrieve an existing one.
    """
    filters = {"name": name}
    entity = EventType(name=name, details=details)
    return PostgresCRUD.get_or_insert(EventType, filters, entity)
