from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base


class TargetType(Base):
    __tablename__ = "target_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    details = Column(Text, nullable=True)

    # Relationships
    events = relationship("Event", secondary="event_target_type", back_populates="target_types")

    __table_args__ = (
        Index("idx_target_type_name", "name"),
    )