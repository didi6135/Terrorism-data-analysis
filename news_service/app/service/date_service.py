import random
from datetime import datetime, timedelta


def random_date_between(start_year=1970, end_year=None):
    """
    Generate a random date between the start_year and end_year.
    If end_year is not provided, use the current year.
    """
    if end_year is None:
        end_year = datetime.now().year

    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)

    # Generate a random timedelta between start_date and end_date
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)