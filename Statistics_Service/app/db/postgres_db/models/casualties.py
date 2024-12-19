from sqlalchemy import Column, Integer, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base


class Casualty(Base):
    __tablename__ = "casualties"

    id = Column(Integer, primary_key=True, index=True)
    total_victims = Column(Integer, default=0, index=True)
    killed_victims = Column(Integer, default=0, index=True)
    injured_victims = Column(Integer, default=0, index=True)
    killed_americans = Column(Integer, default=0, index=True)
    injured_americans = Column(Integer, default=0, index=True)
    killed_attackers = Column(Integer, default=0, index=True)
    injured_attackers = Column(Integer, default=0, index=True)

    # Relationships
    events = relationship("Event", back_populates="casualty")

# Add composite indexes if needed
Index("idx_total_killed_injured", Casualty.total_victims, Casualty.killed_victims, Casualty.injured_victims)
