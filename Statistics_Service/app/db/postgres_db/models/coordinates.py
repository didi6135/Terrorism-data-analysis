from sqlalchemy import Column, Integer, Float, Index
from sqlalchemy.orm import relationship

from Data_Cleaning_Service.app.db.postgres_db.models import Base


class Coordinate(Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # # Unique constraint to avoid duplicate lat/lon pairs
    # __table_args__ = (
    #     {'sqlite_autoincrement': True},
    # )

    # Relationships
    locations = relationship("Location", back_populates="coordinate")

    __table_args__ = (
        Index("idx_coordinate_latitude_longitude", "latitude", "longitude"),
    )