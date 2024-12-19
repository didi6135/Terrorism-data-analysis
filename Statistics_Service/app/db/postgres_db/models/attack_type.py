from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base


class AttackType(Base):
    __tablename__ = "attack_types"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=True)
    details = Column(Text, nullable=True)

    events = relationship("Event", secondary="event_attack_type", back_populates="attack_types")

Index("idx_attack_type_name", AttackType.name)