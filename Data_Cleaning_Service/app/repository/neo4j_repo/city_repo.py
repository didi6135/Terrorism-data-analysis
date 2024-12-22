from Data_Cleaning_Service.app.db.neo4j_db.database import driver
from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import CityNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


# def insert_or_get_city(city_data):
#
#     existing_city = Neo4jCRUD.get_one("City", "name", city_data["name"])
#     if existing_city:
#         print(f"City with name {city_data['name']} already exists.")
#         return existing_city
#
#     print(f"Inserting new City with name {city_data['name']}.")
#     return Neo4jCRUD.create("City", city_data, CityNeo4j)

def insert_or_get_city(city_data):
    """
    Insert or retrieve a city node in Neo4j.
    """
    query = """
        MERGE (ci:City {city_id: $city_id})
        ON CREATE SET ci.name = $name, ci.country_id = $country_id
        RETURN ci
    """
    params = {
        "city_id": city_data["city_id"],
        "name": city_data["name"],
        "country_id": city_data["country_id"]
    }
    with driver.session() as session:
        result = session.run(query, params).single()
        return dict(result["ci"]) if result else None
