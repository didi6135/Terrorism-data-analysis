from data_cleaning.app.models import Coordinate
from data_cleaning.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_coordinate(latitude, longitude):
    """
    Insert new coordinates or retrieve existing ones.
    """
    filters = {"latitude": latitude, "longitude": longitude}
    entity = Coordinate(latitude=latitude, longitude=longitude)
    return PostgresCRUD.get_or_insert(Coordinate, filters, entity)
