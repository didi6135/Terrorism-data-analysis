from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship

from data_cleaning.app.models import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"))

    # Relationships
    country = relationship("Country", back_populates="cities")
    locations = relationship("Location", back_populates="city")

Index("idx_city_name_country", City.name, City.country_id)