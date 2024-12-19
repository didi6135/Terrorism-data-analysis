from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import CityNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_city(city_data):

    existing_city = Neo4jCRUD.get_one("City", "name", city_data["name"])
    if existing_city:
        print(f"City with name {city_data['name']} already exists.")
        return existing_city

    print(f"Inserting new City with name {city_data['name']}.")
    return Neo4jCRUD.create("City", city_data, CityNeo4j)
