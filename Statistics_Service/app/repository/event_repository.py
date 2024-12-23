import json

from sqlalchemy import func
import pandas as pd
from Statistics_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import Event, Location, Coordinate, Casualty


def clean_and_extract_dates():
    with session_maker() as session:
        df = pd.DataFrame(session.query(Event.event_date).all(), columns=["event_date"])
        df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
        return df.dropna(subset=["event_date"]).assign(
            year=lambda x: x["event_date"].dt.year,
            month=lambda x: x["event_date"].dt.month,
        )



########################################################

def get_events_with_coordinates_and_victims():
    """
    Retrieves events with their coordinates and total victims.
    """
    with session_maker() as session:
        results = (
            session.query(
                Coordinate.latitude.label("latitude"),
                Coordinate.longitude.label("longitude"),
                Casualty.total_victims.label("total_victims")
            )
            .join(Location, Coordinate.id == Location.coordinate_id)
            .join(Event, Location.id == Event.location_id)
            .join(Casualty, Event.casualty_id == Casualty.id)
            .filter(Casualty.total_victims > 0)  # Only include events with casualties
            .all()
        )

        # Return results as a list of dictionaries
        return [
            {"latitude": row.latitude, "longitude": row.longitude, "total_victims": row.total_victims}
            for row in results
        ]

def get_all_years_repo():
    df = clean_and_extract_dates()
    yearly_df = (
        df.groupby("year")
        .size()
        .reset_index(name="event_count")
        .sort_values(by="year")
    )

    # Constructing the desired JSON structure
    result = {
        "years": [
            {"id": int(row["year"]), "name": str(row["year"])}
            for index, row in yearly_df.iterrows()
        ]
    }
    return result









def get_event_trends_cleaned(year=None):

    df = clean_and_extract_dates()

    yearly_df = df.groupby("year").size().reset_index(name="event_count").sort_values(by="year")

    if year:
        monthly_df = df[df["year"] == year].groupby("month").size().reset_index(name="event_count").sort_values(by="month")
    else:
        monthly_df = pd.DataFrame(columns=["month", "event_count"])

    return yearly_df, monthly_df







