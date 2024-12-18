from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    # Relationships
    countries = relationship("Country", back_populates="region")

    __table_args__ = (
        Index("idx_region_name", "name"),
    )