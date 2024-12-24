from sqlalchemy import Column, Integer, ForeignKey, Table

from Data_Cleaning_Service.app.db.postgres_db.models import Base

event_targets_type = Table(
    'event_target_type', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('target_type_id', Integer, ForeignKey('target_types.id'), primary_key=True)
)



event_weapons_type = Table(
    "event_weapon_type",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("weapon_type_id", Integer, ForeignKey("weapon_types.id"), primary_key=True),
)

event_groups = Table(
    "event_group_type",
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