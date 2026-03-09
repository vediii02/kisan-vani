from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from datetime import datetime, timezone
from db.base import Base
import enum

class FarmerStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Farmer(Base):
    __tablename__ = "farmers"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), index=True, nullable=False)
    name = Column(String(200))
    village = Column(String(200), default="Not provided", server_default="Not provided")
    district = Column(String(200), default="Not provided", server_default="Not provided")
    state = Column(String(200), default="Not provided", server_default="Not provided")
    crop_type = Column(String(200), default="Not provided", server_default="Not provided")
    land_size = Column(String(50), default="Not provided", server_default="Not provided")
    crop_area = Column(String(100), default="Not provided", server_default="Not provided")
    problem_area = Column(String(200), default="Not provided", server_default="Not provided")
    crop_age_days = Column(String(200), default="Not provided", server_default="Not provided")
    language = Column(String(10), default='hi')
    status = Column(SQLEnum(FarmerStatus), default=FarmerStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))