from sqlalchemy import Column, Integer, Float, String, ForeignKey, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id", ondelete="CASCADE"))

    # Relationships
    region = relationship("Region", back_populates="countries")
    cities = relationship("City", back_populates="country")

    __table_args__ = (
        Index("idx_country_name", "name"),
        Index("idx_country_region", "region_id"),
    )