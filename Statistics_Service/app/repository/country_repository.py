import json

from sqlalchemy.sql import func
from Statistics_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import Country, Event, Location, City, Casualty, Coordinate


def get_all_countries():
    with session_maker() as session:
        countries = session.query(Country.id, Country.name).order_by(Country.name.asc()).all()
        return [{"id": c.id, "name": c.name} for c in countries]



def calculate_average_victims_by_country(country_id, limit=None):
    with session_maker() as session:
        query = (
            session.query(
                Event.id.label("event_id"),
                Event.description.label("event_description"),
                Coordinate.latitude.label("latitude"),
                Coordinate.longitude.label("longitude"),
                Country.name.label("country_name"),
                func.avg(Casualty.total_injured).label("average_injured"),
                func.avg(Casualty.total_killed).label("average_killed"),
                func.avg(Casualty.total_victims).label("average_victims")
            )
            .join(City, City.country_id == Country.id)
            .join(Location, Location.city_id == City.id)
            .join(Coordinate, Coordinate.id == Location.coordinate_id)
            .join(Event, Event.location_id == Location.id)
            .join(Casualty, Event.casualty_id == Casualty.id)
            .filter(Country.id == country_id)
            .group_by(Event.id, Country.name, Coordinate.latitude, Coordinate.longitude)
            .order_by(func.avg(Casualty.total_victims).desc())  # Order by highest average victims
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
                "country_name": row.country_name,
                "average_injured": int(row.average_injured),
                "average_killed": int(row.average_killed),
                "score": int(row.average_victims),
            }
            for row in results
        ]




def get_top_5_countries_by_events():
    """
    Retrieves the top 5 countries with the most events.
    """
    with session_maker() as session:
        results = (
            session.query(
                Country.name.label("country_name"),
                func.count(Event.id).label("event_count")
            )
            .join(City, Country.id == City.country_id)
            .join(Location, City.id == Location.city_id)
            .join(Event, Location.id == Event.location_id)
            .group_by(Country.name)
            .order_by(func.count(Event.id).desc())
            .limit(5)
            .all()
        )

        # Return results as a list of dictionaries
        return [{"country_name": row.country_name, "event_count": row.event_count} for row in results]



