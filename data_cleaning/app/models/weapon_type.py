from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import relationship

from data_cleaning.app.models import Base
from data_cleaning.app.models.many_to_many_tables import event_weapons_type


class WeaponType(Base):
    __tablename__ = "weapon_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    details = Column(Text, nullable=True)

    # Relationships
    events = relationship("Event", secondary="event_weapon_type", back_populates="weapon_types")

    __table_args__ = (
        Index("idx_weapon_type_name", "name"),
    )