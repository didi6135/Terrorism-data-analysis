from Data_Cleaning_Service.app.models import Region
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_region(name):
    """
    Insert a new region or retrieve an existing one.
    """
    filters = {"name": name}
    entity = Region(name=name)
    return PostgresCRUD.get_or_insert(Region, filters, entity)