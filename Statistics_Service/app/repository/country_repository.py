import json

from sqlalchemy.sql import func
from Statistics_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import Country, Event, Location, City, Casualty


def get_countries_by_region(region_id):
    with session_maker() as session:
        countries = session.query(Country.id, Country.name).filter(Country.region_id == region_id).all()
        return [{"id": c.id, "name": c.name} for c in countries]



def calculate_average_victims_by_country(country_id):
    with session_maker() as session:
        query = (
            session.query(
                func.avg(Casualty.total_killed * 2 + Casualty.total_injured).label("average_victims"),
                Country.name.label("name")
            )
            .join(City, City.country_id == Country.id)
            .join(Location, Location.city_id == City.id)
            .join(Event, Event.location_id == Location.id)
            .join(Casualty, Event.casualty_id == Casualty.id)
            .filter(Country.id == country_id)
        )
        result = query.one_or_none()
        return {"name": result.name, "average_victims": result.average_victims} if result else {}





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



