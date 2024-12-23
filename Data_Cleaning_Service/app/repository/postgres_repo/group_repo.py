from Data_Cleaning_Service.app.db.postgres_db.models import Group
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_group(name, subgroup_name=None):

    filters = {"name": name}
    entity = Group(
        name=name,
        subgroup_name=subgroup_name,
    )
    return PostgresCRUD.get_or_insert(Group, filters, entity)
