from Data_Cleaning_Service.app.db.postgres_db.models import Coordinate
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_coordinate(latitude, longitude):

    filters = {"latitude": latitude, "longitude": longitude}
    entity = Coordinate(latitude=latitude, longitude=longitude)
    return PostgresCRUD.get_or_insert(Coordinate, filters, entity)
