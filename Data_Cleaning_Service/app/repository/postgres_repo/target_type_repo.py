from Data_Cleaning_Service.app.db.postgres_db.models import TargetType
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_target_type(target_type: TargetType):
    filters = {"name": target_type.name}
    return PostgresCRUD.get_or_insert(TargetType, filters, target_type)