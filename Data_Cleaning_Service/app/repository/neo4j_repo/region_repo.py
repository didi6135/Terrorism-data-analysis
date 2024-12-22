from Data_Cleaning_Service.app.db.neo4j_db.database import driver
from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import  RegionNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD

#
# def insert_or_get_region(region_data):
#
#     existing_event = Neo4jCRUD.get_one("Region", "name", region_data["name"])
#     if existing_event:
#         print(f"Region with name {region_data['name']} already exists.")
#         return existing_event
#
#     print(f"Inserting new Region with name {region_data['name']}.")
#     return Neo4jCRUD.create("Region", region_data, RegionNeo4j)

def insert_or_get_region(region_data):
    """
    Insert or retrieve a region node in Neo4j.
    """
    query = """
        MERGE (r:Region {region_id: $region_id})
        ON CREATE SET r.name = $name
        RETURN r
    """
    params = {
        "region_id": region_data["region_id"],
        "name": region_data["name"]
    }
    with driver.session() as session:
        result = session.run(query, params).single()
        return dict(result["r"]) if result else None
