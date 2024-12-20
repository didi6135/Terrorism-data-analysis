import json

from sqlalchemy import func
import pandas as pd
from Statistics_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import Event, Location, Coordinate, Casualty


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





def get_yearly_trends():

    df = clean_and_extract_dates()
    yearly_df = (
        df.groupby("year")
        .size()
        .reset_index(name="event_count")
        .sort_values(by="year")
    )
    return yearly_df


def get_monthly_trends(year):

    df = clean_and_extract_dates()
    monthly_df = (
        df[df["year"] == year]
        .groupby("month")
        .size()
        .reset_index(name="event_count")
        .sort_values(by="month")
    )
    return monthly_df



def get_event_trends_cleaned(year=None):

    df = clean_and_extract_dates()

    yearly_df = df.groupby("year").size().reset_index(name="event_count").sort_values(by="year")

    if year:
        monthly_df = df[df["year"] == year].groupby("month").size().reset_index(name="event_count").sort_values(by="month")
    else:
        monthly_df = pd.DataFrame(columns=["month", "event_count"])

    return yearly_df, monthly_df





def clean_and_extract_dates():

    with session_maker() as session:
        results = session.query(Event.event_date).all()

        df = pd.DataFrame(results, columns=["event_date"])

        df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")

        df = df.dropna(subset=["event_date"])

        df["year"] = df["event_date"].dt.year
        df["month"] = df["event_date"].dt.month

        return df


