from Data_Cleaning_Service.app.db.postgres_db.models import Region
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_region(name):

    filters = {"name": name}
    entity = Region(name=name)
    return PostgresCRUD.get_or_insert(Region, filters, entity)