import hashlib
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
import math

def generate_deterministic_uuid(value: str) -> str:
    """Generate a UUID based on a hash of the input value."""
    return str(uuid.UUID(hashlib.md5(value.encode()).hexdigest()))


def process_region_and_country_to_neo4j(row):
    """Insert Region, Country, and link Event to Country."""
    region_name = row.get("region_txt", "Unknown")
    region_data = {
        "region_id": generate_deterministic_uuid(region_name),
        "name": region_name
    }

    # Insert or get Region node
    region_node = insert_or_get_region(region_data)

    country_name = row.get("country_txt", "Unknown")
    country_data = {
        "country_id": generate_deterministic_uuid(country_name),
        "name": country_name,
        "region": region_node["region_id"]
    }

    # Insert or get Country node
    country_node = insert_or_get_country(country_data)

    # Create or update the relationship
    rel = Neo4jCRUD.create_relationship(
        "Country",
        "country_id",
        country_node["country_id"],
        "Region",
        "region_id",
        region_node["region_id"],
        "LOCATED_IN_REGIN",
        {"region_id": region_data["region_id"], "country_id": country_data["country_id"]}
    )

    if not rel:
        print(
            f"Failed to create relationship: Region ({region_data['region_id']}) -> Country ({country_data['country_id']})")

    return country_data

def process_city_to_neo4j(row, country_data):

    city_name = row.get("city", "Unknown")
    city_id = generate_deterministic_uuid(f"{city_name}-{country_data['country_id']}")

    city_data = {
        "city_id": city_id,
        "name": city_name,
        "country_id": country_data['country_id']
    }

    # Ensure city exists
    city_node = insert_or_get_city(city_data)
    if not city_node:
        print(f"Failed to insert or retrieve city: {city_data['name']}")
        return None

    # Ensure relationship exists
    rel = Neo4jCRUD.create_relationship(
        "City",
        "city_id",
        city_node["city_id"],
        "Country",
        "country_id",
        country_data["country_id"],
        "LOCATED_IN_COUNTRY",
        {"city_id": city_node["city_id"], "country_id": country_data["country_id"]}
    )
    if not rel:
        print(f"Failed to create relationship: City ({city_node['city_id']}) -> Country ({country_data['country_id']})")
    return city_node


def process_location_to_neo4j(row, city_data):
    """Insert Location and link to City."""
    # Generate a deterministic UUID for the location based on latitude and longitude
    latitude = row.get("latitude", 0)
    longitude = row.get("longitude", 0)

    # Create location data
    location_data = {
        "location_id": generate_deterministic_uuid(f"{latitude}-{longitude}"),
        "latitude": latitude,
        "longitude": longitude,
        "city": city_data["city_id"]
    }

    # Ensure location exists
    location_node = insert_or_get_location(location_data)
    if not location_node:
        print(f"Failed to insert or retrieve location for latitude: {latitude}, longitude: {longitude}.")
        return None

    # Ensure relationship exists
    rel = Neo4jCRUD.create_relationship(
        "Location",
        "location_id",
        location_node["location_id"],
        "City",
        "city_id",
        city_data["city_id"],
        "LOCATED_IN_CITY",
        {"location_id": location_node["location_id"], "city_id": city_data["city_id"]}
    )
    if not rel:
        print(f"Failed to create relationship: Location ({location_node['location_id']}) -> City ({city_data['city_id']})")
    return location_node




def process_event_to_neo4j(row, location_data):
    """Insert Event into Neo4j."""
    event_data = {
        "event_id": row.get("eventid"),
        "description": row.get("summary", "No Description"),
        "date": row.get("date"),
        "success": row.get("success", False),
        "suicide": row.get("suicide", False)
    }
    event_node = insert_or_get_event(event_data)
    if not event_node:
        print(f"Failed to insert or retrieve event with ID: {event_data['event_id']}")
        return None

    # Ensure relationship exists
    rel = Neo4jCRUD.create_relationship(
        "Event", "event_id", event_node["event_id"],
        "Location", "location_id", location_data["location_id"],
        "LOCATED_AT",
        {"event_id": event_node["event_id"], "location_id": location_data["location_id"]}
    )
    if not rel:
        print(f"Failed to create LOCATED_AT relationship for Event ID: {event_node['event_id']}")
    return event_node


def process_attack_types_to_neo4j(row, event_node):
    """Insert AttackType nodes and link them to the Event."""
    attack_types = [row.get(f"attacktype{i}_txt") for i in range(1, 4)]
    print(attack_types)
    for attack_type in attack_types:
        if attack_type and attack_type != "Unknown" and not (isinstance(attack_type, float) and math.isnan(attack_type)):
            # Prepare AttackType data
            attack_type_data = {"attack_type_id": generate_deterministic_uuid(f'{attack_type}'), "name": attack_type}

            # Insert or retrieve AttackType
            attack_type_node = insert_or_get_attack_type(attack_type_data)
            if attack_type_node:
                # Create relationship between Event and AttackType
                Neo4jCRUD.create_relationship(
                    "Event", "event_id", event_node["event_id"],
                    "AttackType", "attack_type_id", attack_type_node["attack_type_id"],
                    "USES_ATTACK_TYPE",
                    {"event_id": event_node["event_id"], "attack_type_id": attack_type_node["attack_type_id"]}
                )
            else:
                print(f"Failed to insert or retrieve AttackType: {attack_type}")




def process_groups_to_neo4j(row, event_node):
    """Insert Groups and link them to the Event."""
    group_names = [row.get(f"gname{i}", "Unknown") for i in range(1, 4)]  # Handle multiple groups
    for group_name in group_names:
        if group_name and group_name != "Unknown" :
            # Prepare Group data
            group_data = {"group_id": str(uuid.uuid4()), "name": group_name}

            # Insert or retrieve Group
            group_node = insert_or_get_group(group_data)
            if group_node:
                # Create relationship between Event and Group
                Neo4jCRUD.create_relationship(
                    "Event", "event_id", event_node["event_id"],
                    "Group", "group_id", group_node["group_id"],
                    "CAUSED_BY",
                    {"event_id": event_node["event_id"], "group_id": group_node["group_id"]}
                )
            else:
                print(f"Failed to insert or retrieve Group: {group_name}")




def process_casualties_to_neo4j(row, event_node):
    """Insert Casualty node and link it to the Event."""
    # Prepare Casualty data
    casualty_data = {
        "casualty_id": str(uuid.uuid4()),
        "killed": row.get("nkill", 0),
        "injured": row.get("nwound", 0)
    }

    # Insert or retrieve Casualty
    casualty_node = insert_or_get_casualty(casualty_data)
    if casualty_node:
        # Create relationship between Event and Casualty
        Neo4jCRUD.create_relationship(
            "Event", "event_id", event_node["event_id"],
            "Casualty", "casualty_id", casualty_node["casualty_id"],
            "RESULTED_IN",
            {"event_id": event_node["event_id"], "casualty_id": casualty_node["casualty_id"]}
        )
    else:
        print(f"Failed to insert or retrieve Casualty for Event ID: {event_node['event_id']}")


def process_row_to_neo4j(row):
    """Process a single row and insert all related nodes into Neo4j."""
    # Insert Event Node


    # Insert related nodes and relationships
    country_data = process_region_and_country_to_neo4j(row)
    city_data = process_city_to_neo4j(row, country_data)
    location_data = process_location_to_neo4j(row, city_data)
    event_node = process_event_to_neo4j(row, location_data)
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
