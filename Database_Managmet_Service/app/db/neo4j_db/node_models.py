from dataclasses import dataclass, field
from typing import List, Optional

# Nodes
@dataclass
class Event:
    id: str
    date: str
    description: str
    success: bool
    suicide: bool

@dataclass
class Location:
    id: str
    latitude: float
    longitude: float
    city: str

@dataclass
class Region:
    id: str
    name: str

@dataclass
class Country:
    id: str
    name: str
    region: str

@dataclass
class City:
    id: str
    name: str
    country: str

@dataclass
class AttackType:
    id: str
    name: str

@dataclass
class TargetType:
    id: str
    name: str

@dataclass
class Group:
    id: str
    name: str

@dataclass
class Casualty:
    id: str
    killed: int
    injured: int