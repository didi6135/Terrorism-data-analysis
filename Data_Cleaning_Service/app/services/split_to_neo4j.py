import uuid

from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import (
    EvenTNeo4j, LocationNeo4j, RegionNeo4j, CountryNeo4j, CityNeo4j,
    AttackTypeNeo4j, TargetTypeNeo4j, GroupNeo4j, CasualtyNeo4j
)
from Data_Cleaning_Service.app.repository.neo4j_repo.event_repo import insert_or_get_event
from Data_Cleaning_Service.app.repository.neo4j_repo.location_repo import insert_or_get_location
from Data_Cleaning_Service.app.repository.neo4j_repo.target_type_repo import insert_or_get_target_type
from Data_Cleaning_Service.app.repository.neo4j_repo.region_repo import insert_or_get_region
from Data_Cleaning_Service.app.repository.neo4j_repo.country_repo import insert_or_get_country
from Data_Cleaning_Service.app.repository.neo4j_repo.city_repo import insert_or_get_city
from Data_Cleaning_Service.app.repository.neo4j_repo.attack_type_repo import insert_or_get_attack_type
from Data_Cleaning_Service.app.repository.neo4j_repo.group_repo import insert_or_get_group
from Data_Cleaning_Service.app.repository.neo4j_repo.casualty_repo import insert_or_get_casualty
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def process_event_to_neo4j(row):
    """Insert Event into Neo4j."""
    event_data = {
        "event_id": row.get("eventid"),
        "description": row.get("summary", "No Description"),
        "date": row.get("date"),
        "success": row.get("success", False),
        "suicide": row.get("suicide", False)
    }
    return insert_or_get_event(event_data)


def process_location_to_neo4j(row, event_node):
    """Insert Location and link to Event."""
    location_data = {
        "location_id": str(uuid.uuid4()),
        "latitude": row.get("latitude", 0),
        "longitude": row.get("longitude", 0),
        "city": row.get("city", "Unknown")
    }
    location_node = insert_or_get_location(location_data)

    if location_node:
        Neo4jCRUD.create_relationship(
            "Event", "event_id", event_node["event_id"],
            "Location", "location_id", location_node["location_id"],
            "LOCATED_AT"
        )


def process_region_and_country_to_neo4j(row, event_node):
    """Insert Region, Country, and link Event to Country."""
    region_data = {"region_id": str(uuid.uuid4()), "name": row.get("region_txt", "Unknown")}
    region_node = insert_or_get_region(region_data)

    country_data = {"country_id": str(uuid.uuid4()), "name": row.get("country_txt", "Unknown"), "region": region_node["region_id"]}
    country_node = insert_or_get_country(country_data)

    Neo4jCRUD.create_relationship(
        "Event", "event_id", event_node["event_id"],
        "Country", "country_id", country_node["country_id"],
        "LOCATED_IN"
    )


def process_city_to_neo4j(row, event_node):
    """Insert City and link to Event."""
    city_data = {"city_id": str(uuid.uuid4()), "name": row.get("city", "Unknown"), "country": row.get("country_txt", "Unknown")}
    city_node = insert_or_get_city(city_data)

    Neo4jCRUD.create_relationship(
        "Event", "event_id", event_node["event_id"],
        "City", "city_id", city_node["city_id"],
        "LOCATED_AT"
    )


def process_attack_types_to_neo4j(row, event_node):
    """Insert AttackType and link to Event."""
    attack_types = [row.get(f"attacktype{i}_txt") for i in range(1, 4)]
    for attack_type in attack_types:
        if attack_type and attack_type != "Unknown":
            attack_type_data = {"attack_type_id": str(uuid.uuid4()), "name": attack_type}
            attack_type_node = insert_or_get_attack_type(attack_type_data)
            Neo4jCRUD.create_relationship(
                "Event", "event_id", event_node["event_id"],
                "AttackType", "attack_type_id", attack_type_node["attack_type_id"],
                "USES_ATTACK_TYPE"
            )


def process_groups_to_neo4j(row, event_node):
    """Insert Groups and link to Event."""
    group_name = row.get("gname", "Unknown")
    if group_name and group_name != "Unknown":
        group_data = {"group_id": str(uuid.uuid4()), "name": group_name}
        group_node = insert_or_get_group(group_data)
        Neo4jCRUD.create_relationship(
            "Event", "event_id", event_node["event_id"],
            "Group", "group_id", group_node["group_id"],
            "CAUSED_BY"
        )


def process_casualties_to_neo4j(row, event_node):
    """Insert Casualties and link to Event."""
    casualty_data = {
        "casualty_id": str(uuid.uuid4()),
        "killed": row.get("nkill", 0),
        "injured": row.get("nwound", 0)
    }
    casualty_node = insert_or_get_casualty(casualty_data)

    Neo4jCRUD.create_relationship(
        "Event", "event_id", event_node["event_id"],
        "Casualty", "casualty_id", casualty_node["casualty_id"],
        "RESULTED_IN"
    )


def process_row_to_neo4j(row):
    """Process a single row and insert all related nodes into Neo4j."""
    # Insert Event Node
    event_node = process_event_to_neo4j(row)

    # Insert related nodes and relationships
    process_location_to_neo4j(row, event_node)
    process_region_and_country_to_neo4j(row, event_node)
    process_city_to_neo4j(row, event_node)
    process_attack_types_to_neo4j(row, event_node)
    process_groups_to_neo4j(row, event_node)
    process_casualties_to_neo4j(row, event_node)


def main_process_neo4j(row):
    """Process a single row and insert data into Neo4j."""
    try:

        process_row_to_neo4j(row)

        # return event_id

    except Exception as e:
        raise Exception(f"Error processing row for Neo4j: {e}")
