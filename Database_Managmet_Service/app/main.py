from dataclasses import dataclass
from typing import List, Optional

# Define data models for Neo4j


# Relationships


def create_neo4j_models(row: dict):
    """
    Create Neo4j models (nodes and relationships) from a single row of data.

    :param row: Dictionary representing a row of terrorism data.
    :return: Dictionary containing nodes and relationships.
    """
    try:
        # Create nodes
        event = Event(
            id=row['eventid'],
            date=row['date'],
            description=row.get('summary', "Unknown"),
            success=bool(row['success']),
            suicide=bool(row['suicide'])
        )

        location = Location(
            id=f"location-{row['latitude']}-{row['longitude']}",
            latitude=float(row['latitude']) if row['latitude'] != "Unknown" else 0.0,
            longitude=float(row['longitude']) if row['longitude'] != "Unknown" else 0.0,
            city=row.get('city', "Unknown")
        )

        region = Region(
            id=f"region-{row['region_txt']}",
            name=row['region_txt']
        )

        country = Country(
            id=f"country-{row['country_txt']}",
            name=row['country_txt'],
            region=row['region_txt']
        )

        city = City(
            id=f"city-{row['city']}-{row['country_txt']}",
            name=row.get('city', "Unknown"),
            country=row['country_txt']
        )

        attack_types = []
        for i in range(1, 4):
            attack_type_name = row.get(f'attacktype{i}_txt')
            if attack_type_name and attack_type_name != "Unknown":
                attack_types.append(AttackType(
                    id=f"attacktype-{attack_type_name}",
                    name=attack_type_name
                ))

        target_types = []
        for i in range(1, 4):
            target_type_name = row.get(f'targtype{i}_txt')
            if target_type_name and target_type_name != "Unknown":
                target_types.append(TargetType(
                    id=f"targettype-{target_type_name}",
                    name=target_type_name
                ))

        group = Group(
            id=f"group-{row['gname']}",
            name=row.get('gname', "Unknown")
        )

        casualty = Casualty(
            id=f"casualty-{row['eventid']}",
            killed=int(row.get('nkill', 0)),
            injured=int(row.get('nwound', 0))
        )

        # Create relationships
        relationships = [
            EventLocatedAt(event_id=event.id, location_id=location.id),
            EventCasualties(event_id=event.id, casualty_id=casualty.id),
            EventInvolvesGroup(event_id=event.id, group_id=group.id)
        ]

        for attack_type in attack_types:
            relationships.append(EventHasAttackType(event_id=event.id, attack_type_id=attack_type.id))

        for target_type in target_types:
            relationships.append(EventHasTargetType(event_id=event.id, target_type_id=target_type.id))

        # Return nodes and relationships
        return {
            "nodes": [event, location, region, country, city, *attack_types, *target_types, group, casualty],
            "relationships": relationships
        }

    except Exception as e:
        print(f"Error creating Neo4j models: {e}")
        return None