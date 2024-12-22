# from Data_Cleaning_Service.app.db.postgres_db.models import (
#     Casualty, WeaponType, TargetType, Event, Country, City
# )
# from Data_Cleaning_Service.app.repository.postgres_repo.attack_type_repo import insert_or_get_attack_type
# from Data_Cleaning_Service.app.repository.postgres_repo.casualty_repo import insert_new_casualty
# from Data_Cleaning_Service.app.repository.postgres_repo.city_repo import insert_or_get_city
# from Data_Cleaning_Service.app.repository.postgres_repo.coordinates import insert_or_get_coordinate
# from Data_Cleaning_Service.app.repository.postgres_repo.country_repo import insert_or_get_country
# from Data_Cleaning_Service.app.repository.postgres_repo.event_repo import insert_new_event
# from Data_Cleaning_Service.app.repository.postgres_repo.group_repo import insert_or_get_group
# from Data_Cleaning_Service.app.repository.postgres_repo.location_repo import insert_or_get_location
# from Data_Cleaning_Service.app.repository.postgres_repo.many_to_many_repo import link_weapon_type_to_event, link_group_to_event, \
#     link_target_type_to_event, link_attack_type_to_event
# from Data_Cleaning_Service.app.repository.postgres_repo.region_repo import insert_or_get_region
# from Data_Cleaning_Service.app.repository.postgres_repo.target_type_repo import insert_or_get_target_type
# from Data_Cleaning_Service.app.repository.postgres_repo.weapon_type_repo import insert_or_get_weapon_type
# from Data_Cleaning_Service.app.services.split_to_neo4j import process_region_and_country
# from Data_Cleaning_Service.app.utils.logger import log
# import pandas as pd
#
# def clean_row(row):
#     """Cleans a row by replacing NaN with default values."""
#     for key, value in row.items():
#         if pd.isna(value):  # Check for NaN
#             row[key] = "Unknown"  # Replace NaN with default string
#     return row
#
#
# def process_region_and_country(row):
#     """Insert or get region and country."""
#     region_name = row.get('region_txt', "Unknown")
#     country_name = row.get('country_txt', "Unknown")
#     log(f"Processing region: {region_name} and country: {country_name}")
#     region = insert_or_get_region(region_name)
#     country = insert_or_get_country(Country(name=country_name, region_id=region.id))
#     return region.id, country.id
#
#
# def process_city_and_location(row, country_id):
#     """Insert or get city and location."""
#     city_name = row.get('city', "Unknown")
#     latitude = 0 if row.get('latitude') == 'Unknown' else row.get('latitude')
#     longitude = 0 if row.get('longitude') == 'Unknown' else row.get('longitude')
#
#     log(f"Processing city: {city_name} with coordinates ({latitude}, {longitude})")
#     city = insert_or_get_city(city_name, country_id, City(name=city_name, country_id=country_id))
#     coordinate = insert_or_get_coordinate(latitude, longitude)
#     location = insert_or_get_location(city.id, coordinate.id)
#     return city.id, location.id
#
#
# def process_attack_types(row, event_id):
#     """Process multiple attack types for an event."""
#     attack_types = [row.get(f'attacktype{i}_txt', None) for i in range(1, 4)]
#
#     for attack_type_name in attack_types:
#         if attack_type_name and attack_type_name != "Unknown":
#             attack_type = insert_or_get_attack_type(attack_type_name)
#             link_attack_type_to_event(event_id, attack_type.id)
#             log(f"Linked attack type '{attack_type_name}' (ID: {attack_type.id}) to event ID: {event_id}")
#         else:
#             log(f"Invalid or missing attack type '{attack_type_name}'. Skipping...", level="warning")
#
#
#
# def process_target_types(row, event_id):
#     """Insert or get target types and link them to the event."""
#     for i in range(1, 4):
#         target_type_name = row.get(f'targtype{i}_txt', "Unknown")
#         target_subtype_name = row.get(f'targsubtype{i}_txt', "Unknown")
#         if target_type_name != "Unknown":
#             target_type = insert_or_get_target_type(TargetType(name=target_type_name, details=target_subtype_name))
#             link_target_type_to_event(event_id, target_type.id)
#
#
#
# def process_groups(row, event_id):
#     """Insert or get groups and link them to the event."""
#     for i in range(1, 4):
#         group_name = row.get(f'gname{i}', "Unknown")
#         subgroup_name = row.get(f'gsubname{i}', None)
#         if group_name != "Unknown":
#             group = insert_or_get_group(group_name, subgroup_name)
#             link_group_to_event(event_id, group.id)
#
#
#
# def process_weapon_types(row, event_id):
#     """Insert or get weapon types and link them to the event."""
#     for i in range(1, 5):
#         weapon_type_name = row.get(f'weaptype{i}_txt', "Unknown")
#         if weapon_type_name != "Unknown":
#             weapon_type = insert_or_get_weapon_type(WeaponType(name=weapon_type_name))
#             link_weapon_type_to_event(event_id, weapon_type.id)
#
#
#
# def process_casualties(row):
#     total_killed = row.get('nkill', 0) + row.get('nkillus', 0) + row.get('nkillter', 0)
#     total_injured = row.get('nwound', 0) + row.get('nwoundus', 0) + row.get('nwoundte', 0)
#     total_score = total_killed * 2 + total_injured * 1
#
#     casualty = Casualty(
#
#         total_killed= total_killed,
#         total_injured=total_injured,
#
#         total_victims= total_score,
#
#         killed_victims=row.get('nkill', 0),
#         killed_americans=row.get('nkillus', 0),
#         killed_attackers=row.get('nkillter', 0),
#
#         injured_victims=row.get('nwound', 0),
#         injured_americans=row.get('nwoundus', 0),
#         injured_attackers=row.get('nwoundte', 0)
#     )
#     return insert_new_casualty(casualty).id
#
#
# def process_event(row, location_id, casualty_id):
#     """Insert an event and return its ID."""
#     event = Event(
#         event_id=row.get('eventid'),
#         event_date=row.get('date'),
#         attack_motive=row.get('motive'),
#         is_successful=row.get('success', False),
#         is_suicide=row.get('suicide', False),
#         is_extended=row.get('extended', False),
#         is_multiple=row.get('multiple', False),
#         related_events=row.get('related'),
#         description=row.get('summary'),
#         source=row.get('source'),
#         source_id=row.get('source_id'),
#         location_id=location_id,
#         casualty_id=casualty_id
#     )
#     return insert_new_event(event).id
#
#
# def main_split(row):
#     try:
#         row = clean_row(row)  # Ensure row is cleaned
#         region_id, country_id = process_region_and_country(row)
#         city_id, location_id = process_city_and_location(row, country_id)
#         casualty_id = process_casualties(row)
#         event_id = process_event(row, location_id, casualty_id)
#
#         # Process many-to-many relationships
#         process_attack_types(row, event_id)
#         process_target_types(row, event_id)
#         process_groups(row, event_id)
#         process_weapon_types(row, event_id)
#
#         return event_id
#     except Exception as e:
#         log(f"Error in main_split: {e}", level="error")
#         return None
#
from sqlalchemy.orm import Session
from Data_Cleaning_Service.app.db.postgres_db.models import (
    Casualty, WeaponType, TargetType, Event, Country, City, Location, Region,
    event_groups, event_attacks_type, event_targets_type, event_weapons_type
)
from Data_Cleaning_Service.app.utils.logger import log
import pandas as pd



def insert_m2m_data(session, table, data):
    """
    Inserts many-to-many relationship data using raw SQL.
    """
    try:
        if data:
            session.execute(table.insert(), data)
            session.commit()
            log(f"Inserted {len(data)} rows into many-to-many table {table.name}.")
    except Exception as e:
        session.rollback()
        log(f"Error inserting into many-to-many table {table.name}: {e}", level="error")

def insert_in_batches(session, model, data, batch_size=500):
    """
    Inserts data into a table in batches to improve performance, with logging for each batch.
    """
    try:
        total_batches = (len(data) + batch_size - 1) // batch_size  # Calculate total number of batches
        for batch_number, i in enumerate(range(0, len(data), batch_size), start=1):
            batch_data = data[i:i + batch_size]
            session.bulk_insert_mappings(model, batch_data)
            session.commit()
            log(f"Inserted batch {batch_number}/{total_batches} into {model.__tablename__}. Rows: {len(batch_data)}")
    except Exception as e:
        session.rollback()
        log(f"Error inserting into {model.__tablename__}: {e}", level="error")

def bulk_insert_all(data, session: Session, batch_size=1000):
    """
    Bulk inserts all data into the database in batches.
    """
    try:
        log("Starting bulk insert operation.")

        # Prepare bulk data for each table
        regions = {}
        countries = {}
        cities = {}
        locations = {}
        events = []
        casualties = []
        m2m_event_groups = []
        m2m_event_attack_types = []
        m2m_event_target_types = []
        m2m_event_weapon_types = []

        for row in data:
            # Clean row
            row = {k: (v if pd.notna(v) else "Unknown") for k, v in row.items()}

            # Prepare region
            region_name = row.get("region_txt", "Unknown")
            if region_name not in regions:
                regions[region_name] = {"name": region_name}

            # Prepare country
            country_name = row.get("country_txt", "Unknown")
            if country_name not in countries:
                countries[country_name] = {"name": country_name, "region_name": region_name}

            # Prepare city
            city_name = row.get("city", "Unknown")
            latitude = row.get("latitude", None)
            longitude = row.get("longitude", None)
            if city_name not in cities:
                cities[city_name] = {"name": city_name, "country_name": country_name}

            # Prepare location
            if (latitude, longitude) not in locations:
                locations[(latitude, longitude)] = {"city_name": city_name, "latitude": latitude,
                                                    "longitude": longitude}

            # Prepare casualty
            casualty = {
                "total_killed": row.get("nkill", 0),
                "total_injured": row.get("nwound", 0),
                "total_victims": row.get("nkill", 0) * 2 + row.get("nwound", 0),
                "killed_victims": row.get("nkill", 0),
                "killed_americans": row.get("nkillus", 0),
                "killed_attackers": row.get("nkillter", 0),
                "injured_victims": row.get("nwound", 0),
                "injured_americans": row.get("nwoundus", 0),
                "injured_attackers": row.get("nwoundte", 0)
            }
            casualties.append(casualty)

            # Prepare event
            event = {
                "event_id": row.get("eventid"),
                "event_date": row.get("date"),
                "attack_motive": row.get("motive"),
                "is_successful": row.get("success", False),
                "is_suicide": row.get("suicide", False),
                "is_extended": row.get("extended", False),
                "is_multiple": row.get("multiple", False),
                "related_events": row.get("related"),
                "description": row.get("summary"),
                "source": row.get("source"),
                "source_id": row.get("source_id")
            }
            events.append(event)

            # Many-to-Many Relationships
            for i in range(1, 4):
                attack_type_name = row.get(f"attacktype{i}_txt", "Unknown")
                if attack_type_name != "Unknown":
                    m2m_event_attack_types.append(
                        {"event_id": row.get("eventid"), "attack_type_name": attack_type_name})

                target_type_name = row.get(f"targtype{i}_txt", "Unknown")
                if target_type_name != "Unknown":
                    m2m_event_target_types.append(
                        {"event_id": row.get("eventid"), "target_type_name": target_type_name})

                group_name = row.get(f"gname{i}", "Unknown")
                if group_name != "Unknown":
                    m2m_event_groups.append({"event_id": row.get("eventid"), "group_name": group_name})

            for i in range(1, 5):
                weapon_type_name = row.get(f"weaptype{i}_txt", "Unknown")
                if weapon_type_name != "Unknown":
                    m2m_event_weapon_types.append(
                        {"event_id": row.get("eventid"), "weapon_type_name": weapon_type_name})

        # Insert Regions
        insert_in_batches(session, Region, list(regions.values()), batch_size)
        for region_name, region_data in regions.items():
            region = session.query(Region).filter_by(name=region_name).first()
            regions[region_name]["id"] = region.id
        log(f"Inserted {len(regions)} rows into regions.")

        # Insert Countries
        insert_in_batches(
            session,
            Country,
            [{"name": v["name"], "region_id": regions[v["region_name"]]["id"]} for v in countries.values()],
            batch_size,
        )
        for country_name, country_data in countries.items():
            country = session.query(Country).filter_by(name=country_name).first()
            countries[country_name]["id"] = country.id
        log(f"Inserted {len(countries)} rows into countries.")

        # Insert Cities
        insert_in_batches(
            session,
            City,
            [{"name": v["name"], "country_id": countries[v["country_name"]]["id"]} for v in cities.values()],
            batch_size,
        )
        for city_name, city_data in cities.items():
            city = session.query(City).filter_by(name=city_name).first()
            cities[city_name]["id"] = city.id
        log(f"Inserted {len(cities)} rows into cities.")

        # Insert Locations
        insert_in_batches(
            session,
            Location,
            [{"latitude": k[0], "longitude": k[1], "city_id": cities[v["city_name"]]["id"]} for k, v in locations.items()],
            batch_size,
        )
        log(f"Inserted {len(locations)} rows into locations.")

        # Insert Casualties
        insert_in_batches(session, Casualty, casualties, batch_size)
        log(f"Inserted {len(casualties)} rows into casualties.")

        # Insert Events
        insert_in_batches(session, Event, events, batch_size)
        log(f"Inserted {len(events)} rows into events.")

        # Insert Many-to-Many Relationships
        insert_m2m_data(session, event_attacks_type, m2m_event_attack_types)
        insert_m2m_data(session, event_targets_type, m2m_event_target_types)
        insert_m2m_data(session, event_groups, m2m_event_groups)
        insert_m2m_data(session, event_weapons_type, m2m_event_weapon_types)
        log("Bulk insert completed successfully.")

    except Exception as e:
        session.rollback()
        log(f"Error during bulk insert: {e}", level="error")



