from dataclasses import dataclass, field
from typing import List, Optional

# Nodes
@dataclass
class EvenTNeo4j:
    event_id: str
    date: str
    description: str
    success: bool
    suicide: bool

@dataclass
class LocationNeo4j:
    location_id: str
    latitude: float
    longitude: float
    city: str

@dataclass
class RegionNeo4j:
    region_id: str
    name: str

@dataclass
class CountryNeo4j:
    country_id: str
    name: str
    region: str

@dataclass
class CityNeo4j:
    city_id: str
    name: str
    country: str

@dataclass
class AttackTypeNeo4j:
    attack_type_id: str
    name: str

@dataclass
class TargetTypeNeo4j:
    target_type_id: str
    name: str

@dataclass
class GroupNeo4j:
    group_id: str
    name: str

@dataclass
class CasualtyNeo4j:
    casualty_id: str
    killed: int
    injured: int