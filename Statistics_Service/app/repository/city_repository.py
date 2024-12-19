from sqlalchemy import func

from Data_Cleaning_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import City, Casualty, Location, Event


def get_cities_by_country(country_id):
    with session_maker() as session:
        cities = session.query(City.id, City.name).filter(City.country_id == country_id).all()
        return [{"id": c.id, "name": c.name} for c in cities]



def calculate_average_victims_by_city(city_id):
    with session_maker() as session:
        query = (
            session.query(
                func.avg(Casualty.total_killed * 2 + Casualty.total_injured).label("average_victims"),
                City.name.label("name")
            )
            .join(Location, Location.city_id == City.id)
            .join(Event, Event.location_id == Location.id)
            .join(Casualty, Event.casualty_id == Casualty.id)
            .filter(City.id == city_id)
        )
        result = query.one_or_none()
        return {"name": result.name, "average_victims": result.average_victims} if result else {}
