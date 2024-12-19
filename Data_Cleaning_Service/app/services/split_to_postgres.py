from Data_Cleaning_Service.app.db.postgres_db.models import (
    Casualty, WeaponType, TargetType, Event, Country, City
)
from Data_Cleaning_Service.app.repository.postgres_repo.attack_type_repo import insert_or_get_attack_type
from Data_Cleaning_Service.app.repository.postgres_repo.casualty_repo import insert_new_casualty
from Data_Cleaning_Service.app.repository.postgres_repo.city_repo import insert_or_get_city
from Data_Cleaning_Service.app.repository.postgres_repo.coordinates import insert_or_get_coordinate
from Data_Cleaning_Service.app.repository.postgres_repo.country_repo import insert_or_get_country
from Data_Cleaning_Service.app.repository.postgres_repo.event_repo import insert_new_event
from Data_Cleaning_Service.app.repository.postgres_repo.group_repo import insert_or_get_group
from Data_Cleaning_Service.app.repository.postgres_repo.location_repo import insert_or_get_location
from Data_Cleaning_Service.app.repository.postgres_repo.many_to_many_repo import link_weapon_type_to_event, link_group_to_event, \
    link_target_type_to_event, link_attack_type_to_event
from Data_Cleaning_Service.app.repository.postgres_repo.region_repo import insert_or_get_region
from Data_Cleaning_Service.app.repository.postgres_repo.target_type_repo import insert_or_get_target_type
from Data_Cleaning_Service.app.repository.postgres_repo.weapon_type_repo import insert_or_get_weapon_type
from Data_Cleaning_Service.app.utils.logger import log
import pandas as pd

def clean_row(row):
    """Cleans a row by replacing NaN with default values."""
    for key, value in row.items():
        if pd.isna(value):  # Check for NaN
            row[key] = "Unknown"  # Replace NaN with default string
    return row


def process_region_and_country(row):
    """Insert or get region and country."""
    region_name = row.get('region_txt', "Unknown")
    country_name = row.get('country_txt', "Unknown")
    log(f"Processing region: {region_name} and country: {country_name}")
    region = insert_or_get_region(region_name)
    country = insert_or_get_country(Country(name=country_name, region_id=region.id))
    return region.id, country.id


def process_city_and_location(row, country_id):
    """Insert or get city and location."""
    city_name = row.get('city', "Unknown")
    latitude = 0 if row.get('latitude') == 'Unknown' else row.get('latitude')
    longitude = 0 if row.get('longitude') == 'Unknown' else row.get('longitude')

    log(f"Processing city: {city_name} with coordinates ({latitude}, {longitude})")
    city = insert_or_get_city(city_name, country_id, City(name=city_name, country_id=country_id))
    coordinate = insert_or_get_coordinate(latitude, longitude)
    location = insert_or_get_location(city.id, coordinate.id)
    return city.id, location.id


def process_attack_types(row, event_id):
    """Process multiple attack types for an event."""
    attack_types = [row.get(f'attacktype{i}_txt', None) for i in range(1, 4)]

    for attack_type_name in attack_types:
        if attack_type_name and attack_type_name != "Unknown":
            attack_type = insert_or_get_attack_type(attack_type_name)
            link_attack_type_to_event(event_id, attack_type.id)
            log(f"Linked attack type '{attack_type_name}' (ID: {attack_type.id}) to event ID: {event_id}")
        else:
            log(f"Invalid or missing attack type '{attack_type_name}'. Skipping...", level="warning")



def process_target_types(row, event_id):
    """Insert or get target types and link them to the event."""
    for i in range(1, 4):
        target_type_name = row.get(f'targtype{i}_txt', "Unknown")
        target_subtype_name = row.get(f'targsubtype{i}_txt', "Unknown")
        if target_type_name != "Unknown":
            target_type = insert_or_get_target_type(TargetType(name=target_type_name, details=target_subtype_name))
            link_target_type_to_event(event_id, target_type.id)



def process_groups(row, event_id):
    """Insert or get groups and link them to the event."""
    for i in range(1, 4):
        group_name = row.get(f'gname{i}', "Unknown")
        subgroup_name = row.get(f'gsubname{i}', None)
        if group_name != "Unknown":
            group = insert_or_get_group(group_name, subgroup_name)
            link_group_to_event(event_id, group.id)



def process_weapon_types(row, event_id):
    """Insert or get weapon types and link them to the event."""
    for i in range(1, 5):
        weapon_type_name = row.get(f'weaptype{i}_txt', "Unknown")
        if weapon_type_name != "Unknown":
            weapon_type = insert_or_get_weapon_type(WeaponType(name=weapon_type_name))
            link_weapon_type_to_event(event_id, weapon_type.id)



def process_casualties(row):
    total_killed = row.get('nkill', 0) + row.get('nkillus', 0) + row.get('nkillter', 0)
    total_injured = row.get('nwound', 0) + row.get('nwoundus', 0) + row.get('nwoundte', 0)
    total_score = total_killed * 2 + total_injured * 1

    casualty = Casualty(

        total_killed= total_killed,
        total_injured=total_injured,

        total_victims= total_score,

        killed_victims=row.get('nkill', 0),
        killed_americans=row.get('nkillus', 0),
        killed_attackers=row.get('nkillter', 0),

        injured_victims=row.get('nwound', 0),
        injured_americans=row.get('nwoundus', 0),
        injured_attackers=row.get('nwoundte', 0)
    )
    return insert_new_casualty(casualty).id


def process_event(row, location_id, casualty_id):
    """Insert an event and return its ID."""
    event = Event(
        event_id=row.get('eventid'),
        event_date=row.get('date'),
        attack_motive=row.get('motive'),
        is_successful=row.get('success', False),
        is_suicide=row.get('suicide', False),
        is_extended=row.get('extended', False),
        is_multiple=row.get('multiple', False),
        related_events=row.get('related'),
        description=row.get('summary'),
        source=row.get('source'),
        source_id=row.get('source_id'),
        location_id=location_id,
        casualty_id=casualty_id
    )
    return insert_new_event(event).id


def main_split(row):
    try:
        row = clean_row(row)  # Ensure row is cleaned
        region_id, country_id = process_region_and_country(row)
        city_id, location_id = process_city_and_location(row, country_id)
        casualty_id = process_casualties(row)
        event_id = process_event(row, location_id, casualty_id)

        # Process many-to-many relationships
        process_attack_types(row, event_id)
        process_target_types(row, event_id)
        process_groups(row, event_id)
        process_weapon_types(row, event_id)

        return event_id
    except Exception as e:
        log(f"Error in main_split: {e}", level="error")
        return None
