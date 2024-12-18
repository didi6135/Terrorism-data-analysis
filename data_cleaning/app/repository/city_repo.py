from data_cleaning.app.models import City
from data_cleaning.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_city(name, country_id, city: City):
    """
    Insert a new city or retrieve an existing one.
    """
    filters = {"name": name, "country_id": country_id}
    return PostgresCRUD.get_or_insert(City, filters, city)
