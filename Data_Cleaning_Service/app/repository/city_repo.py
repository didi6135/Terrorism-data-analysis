from Data_Cleaning_Service.app.models import City
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_city(name, country_id, city: City):
    """
    Insert a new city or retrieve an existing one.
    """
    filters = {"name": name, "country_id": country_id}
    return PostgresCRUD.get_or_insert(City, filters, city)
