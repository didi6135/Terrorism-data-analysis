from sqlalchemy import func

from Data_Cleaning_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import Region, Casualty, Location, Event, Country, City


def get_all_regions():
    with session_maker() as session:
        regions = session.query(Region.id, Region.name).all()
        return [{"id": r.id, "name": r.name} for r in regions]



def calculate_average_victims_by_region(region_id):
    with session_maker() as session:
        query = (
            session.query(
                func.avg(Casualty.total_killed * 2 + Casualty.total_injured).label("average_victims"),
                Region.name.label("region_name")
            )
            .join(Country, Country.region_id == Region.id)
            .join(City, City.country_id == Country.id)
            .join(Location, Location.city_id == City.id)
            .join(Event, Event.location_id == Location.id)
            .join(Casualty, Event.casualty_id == Casualty.id)
            .filter(Region.id == region_id)
        )
        result = query.one_or_none()
        return {"region_name": result.region_name, "average_victims": result.average_victims} if result else {}



print(calculate_average_victims_by_region(1))