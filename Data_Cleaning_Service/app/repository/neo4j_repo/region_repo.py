from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import  RegionNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_region(region_data):

    existing_event = Neo4jCRUD.get_one("Region", "name", region_data["name"])
    if existing_event:
        print(f"Region with name {region_data['name']} already exists.")
        return existing_event

    print(f"Inserting new Region with name {region_data['name']}.")
    return Neo4jCRUD.create("Region", region_data, RegionNeo4j)