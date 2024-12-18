from Data_Cleaning_Service.app.models import WeaponType
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_weapon_type(weapon_type: WeaponType):
    filters = {"name": weapon_type.name}
    # entity = WeaponType(name=name, details=details)
    return PostgresCRUD.get_or_insert(WeaponType, filters, weapon_type)