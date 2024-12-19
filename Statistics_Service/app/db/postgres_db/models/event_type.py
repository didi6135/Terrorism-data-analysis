from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base
from Data_Cleaning_Service.app.db.postgres_db.models.many_to_many_tables import event_events_type


class EventType(Base):
    __tablename__ = "event_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    details = Column(Text, nullable=True)

    # Relationships
    events = relationship(
        "Event",
        secondary=event_events_type,
        back_populates="event_types"
    )

    __table_args__ = (
        Index("idx_event_type_name", "name"),
    )