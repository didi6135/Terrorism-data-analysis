from data_cleaning.app.models import Group
from data_cleaning.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_group(name, subgroup_name=None):
    """
    Insert a new group or retrieve an existing one.
    """
    filters = {"name": name}
    entity = Group(
        name=name,
        subgroup_name=subgroup_name,
    )
    return PostgresCRUD.get_or_insert(Group, filters, entity)
