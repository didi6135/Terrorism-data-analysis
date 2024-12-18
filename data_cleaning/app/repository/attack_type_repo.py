from data_cleaning.app.models import AttackType
from data_cleaning.app.utils.generic_for_postgres import PostgresCRUD


def insert_or_get_attack_type(attack_type_name):
    filter = {'name': attack_type_name}
    attack_type = AttackType(
        name=attack_type_name
    )
    return PostgresCRUD.get_or_insert(AttackType, filter, attack_type)