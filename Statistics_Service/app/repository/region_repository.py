from sqlalchemy import func

from Data_Cleaning_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import Region, Casualty, Location, Event, Country, City, \
    Coordinate, event_groups, Group


def get_all_regions():
    with session_maker() as session:
        regions = session.query(Region.id, Region.name).all()
        return [{"id": r.id, "name": r.name} for r in regions]


def calculate_average_victims_by_region(region_id, limit=None):
    with session_maker() as session:
        query = (
            session.query(
                Event.id.label("event_id"),
                Event.description.label("event_description"),
                Coordinate.latitude.label("latitude"),
                Coordinate.longitude.label("longitude"),
                func.avg(Casualty.total_injured).label("average_injured"),
                func.avg(Casualty.total_killed).label("average_killed"),
                func.avg(Casualty.total_victims).label("average_victims"),
                Region.name.label("region_name")
            )
            .join(Country, Country.region_id == Region.id)
            .join(City, City.country_id == Country.id)
            .join(Location, Location.city_id == City.id)
            .join(Coordinate, Coordinate.id == Location.coordinate_id)
            .join(Event, Event.location_id == Location.id)
            .join(Casualty, Event.casualty_id == Casualty.id)
            .filter(Region.id == region_id)
            .group_by(Event.id, Region.name, Coordinate.latitude, Coordinate.longitude)
            .order_by(func.avg(Casualty.total_victims).desc())
        )

        if limit:
            query = query.limit(limit)

        results = query.all()

        return [
            {
                "event_id": row.event_id,
                "event_description": row.event_description,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "region_name": row.region_name,
                "average_injured": int(row.average_injured),
                "average_killed": int(row.average_killed),
                "score": int(row.average_victims),
            }
            for row in results
        ]


def get_unique_groups_by_region(region_id):
    with session_maker() as session:
        return [
            {
                "region_name": row.region_name,
                "unique_group_count": row.unique_group_count,
                "group_names": row.group_names,
                "latitude": row.latitude,
                "longitude": row.longitude
            }
            for row in session.query(
                Region.name.label("region_name"),
                func.count(Group.id.distinct()).label("unique_group_count"),
                func.array_agg(Group.name.distinct()).label("group_names"),
                func.avg(Coordinate.latitude).label("latitude"),
                func.avg(Coordinate.longitude).label("longitude")
            )
            .join(Country, Region.id == Country.region_id)
            .join(City, Country.id == City.country_id)
            .join(Location, City.id == Location.city_id)
            .join(Coordinate, Location.coordinate_id == Coordinate.id)
            .join(Event, Location.id == Event.location_id)
            .join(event_groups, Event.id == event_groups.c.event_id)
            .join(Group, Group.id == event_groups.c.group_id)
            .filter(Region.id == region_id)
            .group_by(Region.name)
        ]





