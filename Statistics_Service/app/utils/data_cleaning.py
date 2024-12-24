from Statistics_Service.app.repository.event_repository import clean_and_extract_dates


def get_yearly_trends():
    df = clean_and_extract_dates()
    return (
        df.groupby("year").size()
        .reset_index(name="event_count")
        .sort_values(by="year")
    )


def get_monthly_trends(year):
    df = clean_and_extract_dates()
    return (
        df[df["year"] == year]
        .groupby("month")
        .size()
        .reset_index(name="event_count")
        .sort_values(by="month")
    )