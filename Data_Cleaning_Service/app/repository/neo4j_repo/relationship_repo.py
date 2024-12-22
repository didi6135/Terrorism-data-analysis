from Data_Cleaning_Service.app.db.neo4j_db.database import driver


def create_country_region_relationship(country_id, region_id):
    """
    Create a LOCATED_IN_REGIN relationship between a country and a region.
    """
    query = """
        MATCH (c:Country {country_id: $country_id})
        MATCH (r:Region {region_id: $region_id})
        MERGE (c)-[rel:LOCATED_IN_REGIN]->(r)
        RETURN rel
    """
    params = {
        "country_id": country_id,
        "region_id": region_id
    }
    with driver.session() as session:
        result = session.run(query, params).single()
        return dict(result["rel"]) if result["rel"] else None


def create_city_country_relationship(city_id, country_id):
    """
    Create a LOCATED_IN_COUNTRY relationship between a city and a country.
    """
    query = """
        MATCH (ci:City {city_id: $city_id})
        MATCH (co:Country {country_id: $country_id})
        MERGE (ci)-[rel:LOCATED_IN_COUNTRY]->(co)
        RETURN rel
    """
    params = {
        "city_id": city_id,
        "country_id": country_id
    }
    with driver.session() as session:
        result = session.run(query, params).single()
        return result["rel"] if result else None



def create_location_city_relationship(location_id, city_id):
    """
    Create a LOCATED_IN_CITY relationship between a location and a city.
    """
    query = """
        MATCH (l:Location {location_id: $location_id})
        MATCH (c:City {city_id: $city_id})
        MERGE (l)-[rel:LOCATED_IN_CITY]->(c)
        RETURN rel
    """
    params = {
        "location_id": location_id,
        "city_id": city_id
    }
    with driver.session() as session:
        try:
            result = session.run(query, params).single()
            if result and "rel" in result:
                print(f"Relationship created: Location ({location_id}) -> City ({city_id})")
                return result["rel"]
        except Exception as e:
            print(f"Error creating relationship: {e}")
        return None
