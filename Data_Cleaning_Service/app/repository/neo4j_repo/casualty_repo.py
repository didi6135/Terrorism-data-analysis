from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import EvenTNeo4j, CasualtyNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_casualty(casualty_data):

    existing_casualty = Neo4jCRUD.get_one("Casualty", "casualty_id", casualty_data["casualty_id"])
    if existing_casualty:
        print(f"Casualty with ID {casualty_data['casualty_id']} already exists.")
        return existing_casualty

    print(f"Inserting new Casualty with ID {casualty_data['casualty_id']}.")
    return Neo4jCRUD.create("Casualty", casualty_data, CasualtyNeo4j)
