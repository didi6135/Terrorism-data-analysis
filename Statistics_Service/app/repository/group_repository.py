import json

from sqlalchemy import func, distinct, desc

from Data_Cleaning_Service.app.db.postgres_db.models import Event, Casualty, Coordinate, Location, Group, Region, City, \
    event_groups, Country, TargetType, event_targets_type
from Statistics_Service.app.db.postgres_db.database import session_maker

#############################################################
def get_top_5_groups_by_casualties():
    """
    Retrieves the top 5 groups with the highest number of casualties (killed + injured).
    """
    with session_maker() as session:
        return [
            {"group_name": row.group_name, "total_casualties": row.total_casualties}
            for row in (
                session.query(
                    Group.name.label("group_name"),
                    func.sum(Casualty.total_killed + Casualty.total_injured).label("total_casualties"),
                )
                .join(Event.groups)
                .join(Casualty, Event.casualty_id == Casualty.id)
                .group_by(Group.name)
                .order_by(desc("total_casualties"))
                .limit(5)
                .all()
            )
        ]


def get_top_groups_by_region(region_id=None):
    with session_maker() as session:
        query = (
            session.query(
                Region.name.label("region_name"),
                Group.name.label("group_name"),
                func.count(Event.id).label("event_count")
            )
            .join(Location, Location.id == Event.location_id)
            .join(City, City.id == Location.city_id)
            .join(Country, Country.id == City.country_id)
            .join(Region, Region.id == Country.region_id)
            .join(event_groups, event_groups.c.event_id == Event.id)
            .join(Group, Group.id == event_groups.c.group_id)
            .group_by(Region.name, Group.name)
            .order_by(Region.name, func.count(Event.id).desc())
        )
        if region_id:
            query = query.filter(Region.id == region_id)

        results = query.all()
        grouped = {}
        for row in results:
            grouped.setdefault(row.region_name, []).append({"group_name": row.group_name, "event_count": row.event_count})

        return {region: groups[:5] for region, groups in grouped.items()}






def get_groups_with_shared_targets_by_region(region_id):
    with session_maker() as session:
        results = session.query(
            TargetType.name.label("target_name"),
            func.array_agg(distinct(Group.name)).label("groups"),
            func.count(Event.id).label("event_count"),
            func.avg(Coordinate.latitude).label("latitude"),
            func.avg(Coordinate.longitude).label("longitude")
        ).join(event_targets_type, Event.id == event_targets_type.c.event_id
        ).join(TargetType, TargetType.id == event_targets_type.c.target_type_id
        ).join(event_groups, Event.id == event_groups.c.event_id
        ).join(Group, Group.id == event_groups.c.group_id
        ).join(Location, Location.id == Event.location_id
        ).join(City, City.id == Location.city_id
        ).join(Country, Country.id == City.country_id
        ).join(Region, Region.id == Country.region_id
        ).join(Coordinate, Location.coordinate_id == Coordinate.id
        ).filter(Region.id == region_id
        ).group_by(TargetType.name
        ).order_by(func.count(Event.id).desc()
        ).all()

        return [
            {
                "target_name": row.target_name,
                "groups": row.groups,
                "event_count": row.event_count,
                "latitude": row.latitude,
                "longitude": row.longitude
            }
            for row in results
        ]

#################################################################



def get_most_deadly_repo(limit=None):

    with session_maker() as session:
        query = (
            session.query(
                Event.id.label("event_id"),
                Event.description.label("event_description"),
                Casualty.total_victims.label("total_victims")
            )
            .join(Casualty, Event.casualty_id == Casualty.id)
            .order_by(Casualty.total_victims.desc())
        )

        if limit:
            query = query.limit(limit)

        results = query.all()

        return [
            {
                "event_id": row.event_id,
                "event_description": row.event_description,
                "total_victims": row.total_victims,
            }
            for row in results
        ]



# print(json.dumps(get_most_deadly_repo(5), indent=4))


def get_top_events_with_coordinates(limit=5):
    """
    Retrieves the top events with the highest casualties and their geographic coordinates.
    """
    with session_maker() as session:
        results = (
            session.query(
                Event.id.label("event_id"),
                Event.description.label("event_description"),
                Casualty.total_victims.label("total_victims"),
                Casualty.total_killed.label("total_killed"),  # Added total_killed
                Casualty.total_injured.label("total_injured"),  # Added total_injured
                Coordinate.latitude.label("latitude"),
                Coordinate.longitude.label("longitude")
            )
            .join(Casualty, Event.casualty_id == Casualty.id)
            .join(Location, Event.location_id == Location.id)
            .join(Coordinate, Location.coordinate_id == Coordinate.id)
            .filter(Coordinate.latitude != 0.0, Coordinate.longitude != 0.0)
            .order_by(Casualty.total_victims.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "event_id": row.event_id,
                "event_description": row.event_description,
                "score": row.total_victims,
                "total_killed": row.total_killed,  # No error here anymore
                "total_injured": row.total_injured,  # Added to results
                "latitude": row.latitude,
                "longitude": row.longitude,
            }
            for row in results
        ]















def get_groups_with_shared_targets_by_country(country_id):

    with session_maker() as session:
        results = (
            session.query(
                TargetType.name.label("target_name"),
                func.array_agg(distinct(Group.name)).label("groups"),  # Unique groups
                func.count(Event.id).label("event_count"),
                func.avg(Coordinate.latitude).label("latitude"),
                func.avg(Coordinate.longitude).label("longitude")
            )
            .join(event_targets_type, Event.id == event_targets_type.c.event_id)
            .join(TargetType, TargetType.id == event_targets_type.c.target_type_id)
            .join(event_groups, Event.id == event_groups.c.event_id)
            .join(Group, Group.id == event_groups.c.group_id)
            .join(Location, Location.id == Event.location_id)
            .join(City, City.id == Location.city_id)
            .join(Country, Country.id == City.country_id)
            .join(Coordinate, Location.coordinate_id == Coordinate.id)
            .filter(Country.id == country_id)
            .group_by(TargetType.name)
            .order_by(func.count(Event.id).desc())
            .all()
        )

        return [
            {
                "target_name": row.target_name,
                "groups": row.groups,
                "event_count": row.event_count,
                "latitude": row.latitude,
                "longitude": row.longitude
            }
            for row in results
        ]





def get_groups_with_shared_events():
    """
    Retrieves events where multiple groups participated in the same attack.
    Returns a list of events with group names and locations.
    """
    with session_maker() as session:
        # Query to get events with multiple groups
        results = (
            session.query(
                Event.id.label("event_id"),
                Event.description.label("event_description"),
                func.array_agg(distinct(Group.name)).label("groups"),
                func.avg(Coordinate.latitude).label("latitude"),
                func.avg(Coordinate.longitude).label("longitude"),
                City.name.label("city"),
                Country.name.label("country")
            )
            .join(event_groups, Event.id == event_groups.c.event_id)
            .join(Group, Group.id == event_groups.c.group_id)
            .join(Location, Location.id == Event.location_id)
            .join(City, City.id == Location.city_id)
            .join(Country, Country.id == City.country_id)
            .join(Coordinate, Location.coordinate_id == Coordinate.id)
            .group_by(Event.id, Event.description, City.name, Country.name)
            .having(func.count(distinct(Group.id)) > 1)  # Filter events with more than one group
            .order_by(Event.id)
            .all()
        )

        # Format results
        data = [
            {
                "event_id": row.event_id,
                "event_description": row.event_description,
                "groups": row.groups,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "location": f"{row.city}, {row.country}"
            }
            for row in results
        ]

        return data



def get_groups_by_target_type(target_type=None):
    """
    Retrieves groups that frequently attack the same target types.
    Filters by specific target type if provided.
    """
    with session_maker() as session:
        query = (
            session.query(
                TargetType.name.label("target_type"),
                Group.name.label("group_name"),
                func.count(Event.id).label("event_count")
            )
            .join(event_targets_type, Event.id == event_targets_type.c.event_id)
            .join(TargetType, TargetType.id == event_targets_type.c.target_type_id)
            .join(event_groups, event_groups.c.event_id == Event.id)
            .join(Group, Group.id == event_groups.c.group_id)
            .group_by(TargetType.name, Group.name)
            .order_by(TargetType.name, func.count(Event.id).desc())
        )

        # Apply filter if target_type is provided
        if target_type:
            query = query.filter(TargetType.id == target_type)

        results = query.all()

        # Organize results by target type
        grouped_results = {}
        for row in results:
            if row.target_type not in grouped_results:
                grouped_results[row.target_type] = []
            grouped_results[row.target_type].append({
                "group_name": row.group_name,
                "event_count": row.event_count
            })

        return [
            {
                "target_type": target_type,
                "groups": groups
            }
            for target_type, groups in grouped_results.items()
        ]
# print(json.dumps(get_groups_by_target_type(18), indent=2))