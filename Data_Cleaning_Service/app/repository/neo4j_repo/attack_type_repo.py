from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import EvenTNeo4j, AttackTypeNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_attack_type(attack_type_data):
    print(f'ffff: {attack_type_data}')
    existing_attack_type = Neo4jCRUD.get_one("AttackType", "attack_type_id", attack_type_data["attack_type_id"])
    if existing_attack_type:
        print(f"Attack type with ID {attack_type_data['attack_type_id']} already exists.")
        return existing_attack_type

    print(f"Inserting new Attack type with ID {attack_type_data['attack_type_id']}.")
    return Neo4jCRUD.create("AttackType", attack_type_data, AttackTypeNeo4j)
