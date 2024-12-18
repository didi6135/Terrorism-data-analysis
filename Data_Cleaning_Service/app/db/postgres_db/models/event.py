from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Boolean, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base
from Data_Cleaning_Service.app.db.postgres_db.models.many_to_many_tables import (
    event_targets_type, event_events_type, event_weapons_type, event_groups, event_attacks_type
)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    event_id = Column(String, nullable=True)
    event_date = Column(String, nullable=False)
    attack_motive = Column(Text, nullable=True)
    is_successful = Column(Boolean, default=False)
    is_suicide = Column(Boolean, default=False)
    is_extended = Column(Boolean, default=False)
    is_multiple = Column(Boolean, default=False)
    related_events = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    source = Column(String(50), nullable=True)
    source_id = Column(String(100), nullable=True)

    location_id = Column(Integer, ForeignKey("locations.id"))
    casualty_id = Column(Integer, ForeignKey("casualties.id"))

    # Many-to-many relationships (use string references to avoid circular imports)
    target_types = relationship("TargetType", secondary=event_targets_type, back_populates="events")
    event_types = relationship("EventType", secondary=event_events_type, back_populates="events")
    weapon_types = relationship("WeaponType", secondary="event_weapon_type", back_populates="events")
    groups = relationship("Group", secondary=event_groups, back_populates="events")
    attack_types = relationship("AttackType", secondary=event_attacks_type, back_populates="events")
    casualty = relationship("Casualty", back_populates="events")
    location = relationship("Location", back_populates="events")


    __table_args__ = (
        Index("idx_event_date", "event_date"),
        Index("idx_event_is_successful", "is_successful"),
        Index("idx_event_location", "location_id"),
        Index("idx_event_casualty", "casualty_id"),
    )

