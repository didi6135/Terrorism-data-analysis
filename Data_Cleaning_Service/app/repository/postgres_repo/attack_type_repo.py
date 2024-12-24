from Data_Cleaning_Service.app.db.postgres_db.models import AttackType
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_attack_type(attack_type_name):
    filters = {'name': attack_type_name}
    attack_type = AttackType(
        name=attack_type_name
    )
    return PostgresCRUD.get_or_insert(AttackType, filters, attack_type)