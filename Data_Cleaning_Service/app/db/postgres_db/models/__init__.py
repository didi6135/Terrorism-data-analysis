from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from .event import Event

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


from .many_to_many_tables import event_targets_type, event_attacks_type, event_groups, event_weapons_type