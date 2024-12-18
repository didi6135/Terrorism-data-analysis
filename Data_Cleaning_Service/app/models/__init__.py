from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from .event import Event
from .event_type import EventType

from .group import Group

from .casualties import Casualty

from .target_type import TargetType

from .weapon_type import WeaponType

from .location import Location
from .region import Region
from .country import Country
from .city import City
from .coordinates import Coordinate

from .attack_type import AttackType


