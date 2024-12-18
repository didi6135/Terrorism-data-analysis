from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import GroupNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_group(group_data):

    existing_group = Neo4jCRUD.get_one("Group", "group_id", group_data["group_id"])
    if existing_group:
        print(f"Group with ID {group_data['group_id']} already exists.")
        return existing_group

    print(f"Inserting new Group with ID {group_data['group_id']}.")
    return Neo4jCRUD.create("Group", group_data, GroupNeo4j)
