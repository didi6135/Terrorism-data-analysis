from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import CountryNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_country(country_data):

    existing_country = Neo4jCRUD.get_one("Country", "name", country_data["name"])
    if existing_country:
        print(f"Country with ID {country_data['name']} already exists.")
        return existing_country

    print(f"Inserting new Country with ID {country_data['name']}.")
    return Neo4jCRUD.create("Country", country_data, CountryNeo4j)
