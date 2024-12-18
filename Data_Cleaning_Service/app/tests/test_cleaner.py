import pytest
from Data_Cleaning_Service.app.models import (
    Region, Country, City, Coordinate, Location, Group, EventType, Casualty, WeaponType, TargetType, Event
)
from Data_Cleaning_Service.app.repository.casualty_repo import insert_new_casualty
from Data_Cleaning_Service.app.repository.coordinates import insert_or_get_coordinate
from Data_Cleaning_Service.app.repository.region_repo import insert_or_get_region
from Data_Cleaning_Service.app.repository.country_repo import insert_or_get_country
from Data_Cleaning_Service.app.repository.city_repo import insert_or_get_city
from Data_Cleaning_Service.app.repository.location_repo import insert_or_get_location
from Data_Cleaning_Service.app.repository.group_repo import insert_or_get_group
from Data_Cleaning_Service.app.repository.event_type_repo import insert_or_get_event_type

from Data_Cleaning_Service.app.repository.event_repo import insert_new_event
from Data_Cleaning_Service.app.repository.target_type_repo import insert_or_get_target_type
from Data_Cleaning_Service.app.repository.weapon_type_repo import insert_or_get_weapon_type


@pytest.fixture
def mock_region():
    return "Test Region"


@pytest.fixture
def mock_country(mock_region):
    region_id = insert_or_get_region(mock_region).id
    return Country(name="Test Country", region_id=region_id)


@pytest.fixture
def mock_city(mock_country):
    country_id = insert_or_get_country(mock_country).id
    return City(name="Test City", country_id=country_id)


@pytest.fixture
def mock_coordinates():
    return {"latitude": 40.7128, "longitude": -74.0060}


@pytest.fixture
def mock_location(mock_city, mock_coordinates):
    city_entity = City(name=mock_city.name, country_id=mock_city.country_id)
    city_id = insert_or_get_city(mock_city.name, mock_city.country_id, city_entity).id
    coordinate_id = insert_or_get_coordinate(
        mock_coordinates["latitude"], mock_coordinates["longitude"]
    ).id
    return Location(city_id=city_id, coordinate_id=coordinate_id)


@pytest.fixture
def mock_group():
    return {"name": "Test Group", "subgroup_name": "Test Subgroup"}


@pytest.fixture
def mock_event_type():
    return {"name": "Test Event Type", "details": "Test Event Details"}


@pytest.fixture
def mock_weapon_type():
    return WeaponType(name="Test Weapon Type", details="Test Weapon Details")


@pytest.fixture
def mock_target_type():
    return TargetType(name="Test Target Type", details="Test Target Details")


def test_insert_or_get_region(mock_region):
    region = insert_or_get_region(mock_region)
    assert region is not None
    assert isinstance(region.id, int)
    assert region.name == mock_region


def test_insert_or_get_country(mock_country):
    country = insert_or_get_country(mock_country)
    assert country is not None
    assert isinstance(country.id, int)
    assert country.name == mock_country.name


def test_insert_or_get_city(mock_city):
    city = insert_or_get_city(mock_city.name, mock_city.country_id, mock_city)
    assert city is not None
    assert isinstance(city.id, int)
    assert city.name == mock_city.name


def test_insert_or_get_coordinate(mock_coordinates):
    coordinate = insert_or_get_coordinate(mock_coordinates["latitude"], mock_coordinates["longitude"])
    assert coordinate is not None
    assert isinstance(coordinate.id, int)
    assert coordinate.latitude == mock_coordinates["latitude"]
    assert coordinate.longitude == mock_coordinates["longitude"]


def test_insert_or_get_location(mock_location):
    location = insert_or_get_location(mock_location.city_id, mock_location.coordinate_id)
    assert location is not None
    assert isinstance(location.id, int)


def test_insert_or_get_group(mock_group):
    group = insert_or_get_group(mock_group["name"], mock_group["subgroup_name"])
    assert group is not None
    assert isinstance(group.id, int)
    assert group.name == mock_group["name"]


def test_insert_or_get_event_type(mock_event_type):
    event_type = insert_or_get_event_type(mock_event_type["name"], mock_event_type["details"])
    assert event_type is not None
    assert isinstance(event_type.id, int)
    assert event_type.name == mock_event_type["name"]


def test_insert_new_weapon_type(mock_weapon_type):
    weapon_type = insert_or_get_weapon_type(mock_weapon_type)
    assert weapon_type is not None
    assert isinstance(weapon_type.id, int)


def test_insert_new_target_type(mock_target_type):
    target_type = insert_or_get_target_type(mock_target_type)
    assert target_type is not None
    assert isinstance(target_type.id, int)


def test_insert_new_event(mock_location, mock_event_type, mock_group):
    # Insert or get valid foreign keys
    event_type = insert_or_get_event_type(mock_event_type["name"], mock_event_type["details"])
    group = insert_or_get_group(mock_group["name"], mock_group["subgroup_name"])
    casualty = insert_new_casualty(Casualty(
        total_victims=5,
        killed_victims=3,
        injured_victims=2,
        killed_americans=1,
        injured_americans=1,
        killed_attackers=1,
        injured_attackers=0
    ))
    weapon_type = insert_or_get_weapon_type(WeaponType(name="Weapon Type", details="Test Details"))
    target_type = insert_or_get_target_type(TargetType(name="Target Type", details="Test Details"))

    # Create the Event object with valid foreign keys
    event = Event(
        event_id="EV12345",  # Unique event identifier
        event_date="2023-12-01",  # Valid date
        attack_motive="Test Motive",  # Optional text field
        is_successful=True,  # Boolean field
        is_suicide=False,  # Boolean field
        is_extended=False,  # Boolean field
        is_multiple=True,  # Boolean field
        related_events="EV12344, EV12346",  # Comma-separated related events
        description="This is a test event for validation purposes.",  # Event description
        source="Test Source",  # Event source
        source_id="SRC001",  # Source identifier

        # Foreign keys
        event_type_id=event_type.id,  # Valid event type ID
        location_id=mock_location.city_id,  # Location ID from mock
        group_id=group.id,  # Valid group ID
        casualty_id=casualty.id,  # Valid casualty ID
        weapon_type_id=weapon_type.id,  # Valid weapon type ID
        target_type_id=target_type.id  # Valid target type ID
    )

    # Insert the Event into the database
    print(f"Inserting Event: {event}")
    event_id = insert_new_event(event)
    assert event_id is not None
    assert isinstance(event_id.id, int)
    print(f"Inserted event with ID: {event_id.id}")




