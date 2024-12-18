from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, Text, Date
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.models import Base

event_targets_type = Table(
    'event_target_type', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('target_type_id', Integer, ForeignKey('target_types.id'), primary_key=True)
)

event_events_type = Table(
    "event_event_type",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("event_type_id", Integer, ForeignKey("event_types.id"), primary_key=True),
)

event_weapons_type = Table(
    "event_weapon_type",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("weapon_type_id", Integer, ForeignKey("weapon_types.id"), primary_key=True),
)

event_groups = Table(
    "event_group",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)

event_attacks_type = Table(
    "event_attack_type",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("attack_type_id", Integer, ForeignKey("attack_types.id"), primary_key=True),
)