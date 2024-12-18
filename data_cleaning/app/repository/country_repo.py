from data_cleaning.app.models import Country
from data_cleaning.app.utils.generic_for_postgres import PostgresCRUD



def insert_or_get_country(country: Country) -> Country:

    filters = {"name": country.name}
    entity = Country(name=country.name, region_id=country.region_id)

    # Use the PostgresCRUD to get or insert
    return PostgresCRUD.get_or_insert(Country, filters, entity)


