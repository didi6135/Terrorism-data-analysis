import json

from sqlalchemy import func

from Data_Cleaning_Service.app.db.postgres_db.models import Event, Casualty, Coordinate, Location, Group, Region, City, \
    event_groups, Country
from Statistics_Service.app.db.postgres_db.database import session_maker

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




# print(json.dumps(get_top_events_with_coordinates(5), indent=4))



# def get_top_active_groups(limit=5, region_id=None):
#     """
#     Retrieves the most active groups based on the number of events, filtered by region if provided.
#     """
#     with session_maker() as session:
#         query = (
#             session.query(
#                 Group.name.label("group_name"),
#                 func.count(Event.id).label("event_count"),
#                 Region.name.label("region_name"),
#                 func.array_agg(Event.id).label("event_ids")
#             )
#             .join(event_groups, Group.id == event_groups.c.group_id)
#             .join(Event, Event.id == event_groups.c.event_id)
#             .join(Location, Event.location_id == Location.id)
#             .join(City, Location.city_id == City.id)
#             .join(Region, City.country_id == Region.id)
#         )
#
#         if region_id:
#             query = query.filter(Region.id == region_id)
#
#         query = (
#             query.group_by(Group.name, Region.name)
#             .order_by(func.count(Event.id).desc())
#             .limit(limit)
#         )
#
#         results = query.all()
#
#         return [
#             {
#                 "group_name": row.group_name,
#                 "event_count": row.event_count,
#                 "region_name": row.region_name,
#                 "event_ids": row.event_ids,
#             }
#             for row in results
def get_top_groups_by_region():
    """
    Retrieves the top 5 most active groups for each region.
    """
    with session_maker() as session:
        # Query to count events per group per region
        results = (
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
            .all()
        )

        # Organize results by region
        grouped_results = {}
        for row in results:
            if row.region_name not in grouped_results:
                grouped_results[row.region_name] = []
            grouped_results[row.region_name].append({
                "group_name": row.group_name,
                "event_count": row.event_count
            })

        # For each region, keep only the top 5 groups
        top_groups_by_region = {
            region: groups[:5] for region, groups in grouped_results.items()
        }

        return top_groups_by_region

# Test the function
print(json.dumps(get_top_groups_by_region(), indent=4))


def get_region_coordinates():
    """
    Retrieve coordinates for each region's center.
    """
    with session_maker() as session:
        results = (
            session.query(
                Region.name.label("region_name"),
                func.avg(Coordinate.latitude).label("avg_latitude"),
                func.avg(Coordinate.longitude).label("avg_longitude")
            )
            .join(Country, Region.id == Country.region_id)
            .join(City, Country.id == City.country_id)
            .join(Location, City.id == Location.city_id)
            .join(Coordinate, Location.coordinate_id == Coordinate.id)
            .group_by(Region.name)
            .all()
        )

        return {
            row.region_name: {"latitude": row.avg_latitude, "longitude": row.avg_longitude}
            for row in results
        }



def get_top_5_groups_by_casualties():
    """
    Retrieves the top 5 groups with the highest number of casualties (killed + injured) over the years.
    """
    with session_maker() as session:
        results = (
            session.query(
                Group.name.label("group_name"),
                func.sum(Casualty.total_killed + Casualty.total_injured).label("total_casualties")
            )
            .join(Event.groups)
            .join(Casualty, Event.casualty_id == Casualty.id)
            .group_by(Group.name)
            .order_by(func.sum(Casualty.total_killed + Casualty.total_injured).desc())
            .limit(5)
            .all()
        )

        return [
            {
                "group_name": row.group_name,
                "total_casualties": row.total_casualties
            }
            for row in results
        ]


