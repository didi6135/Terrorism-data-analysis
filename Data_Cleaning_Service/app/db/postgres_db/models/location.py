from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base



class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    coordinate_id = Column(Integer, ForeignKey("coordinates.id", ondelete="CASCADE"))

    # Relationships
    city = relationship("City", back_populates="locations")
    coordinate = relationship("Coordinate", back_populates="locations")
    events = relationship("Event", back_populates="location")


    __table_args__ = (
        Index("idx_location_city", "city_id"),
        Index("idx_location_coordinate", "coordinate_id"),
    )