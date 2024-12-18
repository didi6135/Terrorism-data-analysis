from data_cleaning.app.models import TargetType
from data_cleaning.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_target_type(target_type: TargetType):
    filters = {"name": target_type.name}
    # entity = TargetType(name=target_typename, details=details)
    return PostgresCRUD.get_or_insert(TargetType, filters, target_type)