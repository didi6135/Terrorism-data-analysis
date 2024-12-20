from sqlalchemy import func

from Data_Cleaning_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import City, Casualty, Location, Event, Coordinate


def get_all_cities():
    with session_maker() as session:
        cities = session.query(City.id, City.name).order_by(City.name.asc()).all()
        return [{"id": c.id, "name": c.name} for c in cities]



def calculate_average_victims_by_city(city_id, limit=None):
    with session_maker() as session:
        query = (
            session.query(
                Event.id.label("event_id"),
                Event.description.label("event_description"),
                Coordinate.latitude.label("latitude"),
                Coordinate.longitude.label("longitude"),
                City.name.label("city_name"),
                func.avg(Casualty.total_injured).label("average_injured"),
                func.avg(Casualty.total_killed).label("average_killed"),
                func.avg(Casualty.total_victims).label("average_victims")
            )
            .join(Location, Location.city_id == City.id)
            .join(Coordinate, Coordinate.id == Location.coordinate_id)
            .join(Event, Event.location_id == Location.id)
            .join(Casualty, Event.casualty_id == Casualty.id)
            .filter(City.id == city_id)
            .group_by(Event.id, City.name, Coordinate.latitude, Coordinate.longitude)
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
                "city_name": row.city_name,
                "average_injured": int(row.average_injured),
                "average_killed": int(row.average_killed),
                "score": int(row.average_victims),
            }
            for row in results
        ]


