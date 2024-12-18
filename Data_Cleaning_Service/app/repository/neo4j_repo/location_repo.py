from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import LocationNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_location(location_data):

    existing_location = Neo4jCRUD.get_one("Location", "location_id", location_data["location_id"])
    if existing_location:
        print(f"Location with ID {location_data['location_id']} already exists.")
        return existing_location

    print(f"Inserting new Location with ID {location_data['location_id']}.")
    return Neo4jCRUD.create("Location", location_data, LocationNeo4j)