import json

from sqlalchemy.sql import func
from Statistics_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import Country, Event, Location, City


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



