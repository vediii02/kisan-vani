# db/models/organisation.py

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db.base import Base

class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=True)
    status = Column(String(50), default="active", nullable=False)  # active, inactive, suspended
    plan_type = Column(String(50), default="basic", nullable=False)  # basic, professional, enterprise
    phone_numbers = Column(Text, nullable=True)  # DEPRECATED - Use phone_numbers relationship instead
    
    # Primary phone number - THE number farmers will call (e.g., Exotel number)
    # Organisation can manage this from their dashboard
    # Unique constraint ensures one number = one organisation
    primary_phone = Column(String(20), unique=True, nullable=True, index=True)
    
    # Secondary phone number
    secondary_phone = Column(String(20), nullable=True)
    
    # Address fields
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
    )
    
    # Relationship to phone numbers - ONE organisation has MANY phone numbers
    # This is the proper way to manage phone numbers (not JSON column)
    phone_numbers_rel = relationship(
        "OrganisationPhoneNumber",
        back_populates="organisation",
        cascade="all, delete-orphan"
    )
    
    # Relationship to users
    users = relationship("User", back_populates="organisation")
