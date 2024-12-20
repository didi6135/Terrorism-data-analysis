from dataclasses import dataclass

@dataclass
class EventLocatedAt:
    event_id: str
    location_id: str

@dataclass
class EventHasAttackType:
    event_id: str
    attack_type_id: str

@dataclass
class EventHasTargetType:
    event_id: str
    target_type_id: str

@dataclass
class EventInvolvesGroup:
    event_id: str
    group_id: str

@dataclass
class EventCasualties:
    event_id: str
    casualty_id: str

########################################
########################################

@dataclass
class CountryInRegionRel:
    region_id: str
    country_id: str

@dataclass
class CityInCountryRel:
    city_id:str
    country_id: str

@dataclass
class LocationInCityRel:
    city_id:str
    location_id:str

@dataclass
class EventInLocationRel:
    event_id:str
    location_id:str

