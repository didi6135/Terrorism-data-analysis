import json
import pandas as pd
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker

from Data_Cleaning_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import AttackType, TargetType, event_attacks_type, Event, \
    event_targets_type, Casualty, City, Region, Country, Location, Group, event_groups, Coordinate

from sqlalchemy import func, desc

def get_most_deadly_attack_types(limit=None):
    with session_maker() as session:
        query = (
            session.query(
                AttackType.name.label("attack_type"),
                func.sum(Casualty.total_killed).label("total_killed"),
                func.sum(Casualty.total_injured).label("total_injured"),
                (func.sum(Casualty.total_killed * 2 + Casualty.total_injured)).label("score"),
            )
            .join(Event.attack_types)
            .join(Event.casualty)
            .group_by(AttackType.name)
            .order_by(desc("score"))
        )
        results = query.limit(limit).all() if limit else query.all()
        return [
            {col: getattr(row, col) for col in ["attack_type", "total_killed", "total_injured", "score"]}
            for row in results
        ]


def analyze_attack_target_correlation():
    with session_maker() as session:
        results = (
            session.query(AttackType.name.label("attack_type"), TargetType.name.label("target_type"))
            .join(event_attacks_type, event_attacks_type.c.attack_type_id == AttackType.id)
            .join(Event, Event.id == event_attacks_type.c.event_id)
            .join(event_targets_type, event_targets_type.c.event_id == Event.id)
            .join(TargetType, TargetType.id == event_targets_type.c.target_type_id)
            .all()
        )
        data = pd.DataFrame(results, columns=["attack_type", "target_type"])
        return pd.crosstab(data["attack_type"], data["target_type"]).to_dict()


def get_attack_strategies_by_region(region_id=None):
    with session_maker() as session:
        query = session.query(
            Region.name.label("region_name"),
            AttackType.name.label("attack_type"),
            func.count(func.distinct(Group.id)).label("unique_group_count"),
            func.array_agg(func.distinct(Group.name)).label("group_names"),
            func.avg(Coordinate.latitude).label("latitude"),
            func.avg(Coordinate.longitude).label("longitude")
        ).join(Country, Region.id == Country.region_id
        ).join(City, Country.id == City.country_id
        ).join(Location, City.id == Location.city_id
        ).join(Coordinate, Location.coordinate_id == Coordinate.id
        ).join(Event, Location.id == Event.location_id
        ).join(event_attacks_type, event_attacks_type.c.event_id == Event.id
        ).join(AttackType, AttackType.id == event_attacks_type.c.attack_type_id
        ).join(event_groups, event_groups.c.event_id == Event.id
        ).join(Group, Group.id == event_groups.c.group_id
        ).group_by(Region.name, AttackType.name
        ).order_by(func.count(func.distinct(Group.id)).desc())

        if region_id:
            query = query.filter(Region.id == region_id)

        return [
            {
                "region_name": row.region_name,
                "attack_type": row.attack_type,
                "unique_group_count": row.unique_group_count,
                "group_names": row.group_names,
                "latitude": row.latitude,
                "longitude": row.longitude
            }
            for row in query.all()
        ]



def get_attack_strategies_by_country(country_id=None):
    """
    Retrieves attack strategies with coordinates for a specific country or globally.
    """
    with session_maker() as session:
        # Explicitly set the FROM clause to start from the Event table
        query = (
            session.query(
                Country.name.label("country_name"),
                AttackType.name.label("attack_type"),
                func.count(Group.id.distinct()).label("unique_group_count"),
                func.array_agg(Group.name.distinct()).label("group_names"),
                func.avg(Coordinate.latitude).label("latitude"),
                func.avg(Coordinate.longitude).label("longitude")
            )
            .select_from(Event)  # Explicitly start from the Event table
            .join(Location, Event.location_id == Location.id)
            .join(City, Location.city_id == City.id)
            .join(Country, City.country_id == Country.id)
            .join(Coordinate, Location.coordinate_id == Coordinate.id)
            .join(event_attacks_type, Event.id == event_attacks_type.c.event_id)
            .join(AttackType, event_attacks_type.c.attack_type_id == AttackType.id)
            .join(event_groups, Event.id == event_groups.c.event_id)
            .join(Group, event_groups.c.group_id == Group.id)
            .group_by(Country.name, AttackType.name)
            .order_by(func.count(Group.id.distinct()).desc())
        )

        if country_id:
            query = query.filter(Country.id == country_id)

        return [
            {
                "country_name": row.country_name,
                "attack_type": row.attack_type,
                "unique_group_count": row.unique_group_count,
                "group_names": row.group_names,
                "latitude": row.latitude,
                "longitude": row.longitude
            }
            for row in query.all()
        ]
