from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import LocationNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


# def insert_or_get_location(location_data):
#
#     existing_location = Neo4jCRUD.get_one("Location", "location_id", location_data["location_id"])
#     if existing_location:
#         print(f"Location with ID {location_data['location_id']} already exists.")
#         return existing_location
#
#     print(f"Inserting new Location with ID {location_data['location_id']}.")
#     return Neo4jCRUD.create("Location", location_data, LocationNeo4j)
from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import LocationNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_location(location_data):

    query = """
        MATCH (l:Location {latitude: $latitude, longitude: $longitude})
        RETURN l
    """
    params = {"latitude": location_data["latitude"], "longitude": location_data["longitude"]}
    existing_location = Neo4jCRUD.query_single(query, params)

    if existing_location:
        print(f"Location with latitude {location_data['latitude']} and longitude {location_data['longitude']} already exists.")
        return None

    # If not exists, insert a new location
    print(f"Inserting new Location with latitude {location_data['latitude']} and longitude {location_data['longitude']}.")
    return Neo4jCRUD.create("Location", location_data, LocationNeo4j)
