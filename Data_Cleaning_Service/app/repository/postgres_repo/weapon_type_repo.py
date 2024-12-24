from Data_Cleaning_Service.app.db.postgres_db.models import WeaponType
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_weapon_type(weapon_type: WeaponType):
    filters = {"name": weapon_type.name}
    return PostgresCRUD.get_or_insert(WeaponType, filters, weapon_type)