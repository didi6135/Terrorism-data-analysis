from Data_Cleaning_Service.app.db.postgres_db.models import Country
from Data_Cleaning_Service.app.utils.generic_for_postgres import PostgresCRUD



def insert_or_get_country(country: Country) -> Country:

    filters = {"name": country.name}
    entity = Country(name=country.name, region_id=country.region_id)

    return PostgresCRUD.get_or_insert(Country, filters, entity)


