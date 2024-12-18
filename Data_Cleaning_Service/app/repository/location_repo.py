from Data_Cleaning_Service.app.models import Location
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_location(city_id, coordinate_id):
    """
    Insert a new location or retrieve an existing one.
    """
    filters = {"city_id": city_id, "coordinate_id": coordinate_id}
    entity = Location(city_id=city_id, coordinate_id=coordinate_id)
    return PostgresCRUD.get_or_insert(Location, filters, entity)
