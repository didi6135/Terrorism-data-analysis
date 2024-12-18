from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import TargetTypeNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_target_type(target_type_data):

    existing_target_type = Neo4jCRUD.get_one("TargetType", "id", target_type_data["id"])
    if existing_target_type:
        print(f"TargetType with ID {target_type_data['id']} already exists.")
        return existing_target_type

    print(f"Inserting new TargetType with ID {target_type_data['id']}.")
    return Neo4jCRUD.create("TargetType", target_type_data, TargetTypeNeo4j)
