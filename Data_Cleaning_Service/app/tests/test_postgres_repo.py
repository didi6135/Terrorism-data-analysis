import pytest
from unittest.mock import patch, MagicMock
from Data_Cleaning_Service.app.db.postgres_db.models import (
    AttackType, Casualty, City, Coordinate, Country, Event,
    Group, Location, Region, TargetType, WeaponType
)
from Data_Cleaning_Service.app.repository.postgres_repo.attack_type_repo import insert_or_get_attack_type
from Data_Cleaning_Service.app.repository.postgres_repo.casualty_repo import insert_new_casualty
from Data_Cleaning_Service.app.repository.postgres_repo.city_repo import insert_or_get_city
from Data_Cleaning_Service.app.repository.postgres_repo.coordinates import insert_or_get_coordinate
from Data_Cleaning_Service.app.repository.postgres_repo.country_repo import insert_or_get_country
from Data_Cleaning_Service.app.repository.postgres_repo.event_repo import insert_new_event
from Data_Cleaning_Service.app.repository.postgres_repo.group_repo import insert_or_get_group
from Data_Cleaning_Service.app.repository.postgres_repo.location_repo import insert_or_get_location
from Data_Cleaning_Service.app.repository.postgres_repo.many_to_many_repo import link_entity_to_event
from Data_Cleaning_Service.app.repository.postgres_repo.region_repo import insert_or_get_region
from Data_Cleaning_Service.app.repository.postgres_repo.target_type_repo import insert_or_get_target_type
from Data_Cleaning_Service.app.repository.postgres_repo.weapon_type_repo import insert_or_get_weapon_type


@pytest.fixture
def mock_postgres_crud():
    with patch('Data_Cleaning_Service.app.utils.generic_for_postgres.PostgresCRUD') as mock_crud:
        yield mock_crud


@pytest.fixture
def mock_session_maker():
    with patch('Data_Cleaning_Service.app.db.postgres_db.database.session_maker', MagicMock()) as mock_session:
        yield mock_session


def test_insert_or_get_attack_type(mock_postgres_crud):
    mock_postgres_crud.get_or_insert.return_value = AttackType(name="test")
    result = insert_or_get_attack_type("test")
    assert result.name == "test"


def test_insert_new_casualty(mock_postgres_crud):
    mock_postgres_crud.insert.return_value = Casualty(total_killed=5)
    casualty = Casualty(total_killed=5)
    result = insert_new_casualty(casualty)
    assert result.total_killed == 5


def test_insert_or_get_city(mock_postgres_crud):
    mock_postgres_crud.get_or_insert.return_value = City(name="Test City")
    result = insert_or_get_city("Test City", 1, City(name="Test City", country_id=1))
    assert result.name == "Test City"


def test_insert_or_get_coordinate(mock_postgres_crud):
    mock_postgres_crud.get_or_insert.return_value = Coordinate(latitude=10.0, longitude=20.0)
    result = insert_or_get_coordinate(10.0, 20.0)
    assert result.latitude == 10.0
    assert result.longitude == 20.0


def test_insert_or_get_country(mock_postgres_crud):
    mock_postgres_crud.get_or_insert.return_value = Country(name="Test Country", region_id=1)
    country = Country(name="Test Country", region_id=1)
    result = insert_or_get_country(country)
    assert result.name == "Test Country"






def test_insert_or_get_group(mock_postgres_crud):
    mock_postgres_crud.get_or_insert.return_value = Group(name="Test Group")
    result = insert_or_get_group("Test Group")
    assert result.name == "Test Group"


def test_insert_or_get_location(mock_postgres_crud):
    mock_postgres_crud.get_or_insert.return_value = Location(city_id=1, coordinate_id=2)
    result = insert_or_get_location(1, 2)
    assert result.city_id == 1
    assert result.coordinate_id == 2


def test_insert_or_get_region(mock_postgres_crud):
    mock_postgres_crud.get_or_insert.return_value = Region(name="Test Region")
    result = insert_or_get_region("Test Region")
    assert result.name == "Test Region"


def test_insert_or_get_target_type(mock_postgres_crud):
    mock_postgres_crud.get_or_insert.return_value = TargetType(name="Test Target Type")
    result = insert_or_get_target_type(TargetType(name="Test Target Type"))
    assert result.name == "Test Target Type"


def test_insert_or_get_weapon_type(mock_postgres_crud):
    mock_postgres_crud.get_or_insert.return_value = WeaponType(name="Test Weapon Type")
    result = insert_or_get_weapon_type(WeaponType(name="Test Weapon Type"))
    assert result.name == "Test Weapon Type"


