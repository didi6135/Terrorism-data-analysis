from sqlalchemy import Column, Integer, String, Text, Boolean, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base
from Data_Cleaning_Service.app.db.postgres_db.models.many_to_many_tables import event_groups


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    subgroup_name = Column(String(100), nullable=True)
    is_uncertain = Column(Boolean, default=False)
    description = Column(Text, nullable=True)

    # Relationships
    events = relationship(
        "Event",
        secondary=event_groups,
        back_populates="groups"
    )

    __table_args__ = (
        Index("idx_group_name", "name"),
    )