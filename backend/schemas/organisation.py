from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class OrganisationBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    status: Optional[str] = "active"
    plan_type: Optional[str] = "basic"
    phone_numbers: Optional[str] = None
    secondary_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    website_link: Optional[str] = None
    description: Optional[str] = None

class OrganisationCreate(OrganisationBase):
    pass

class OrganisationUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = None
    plan_type: Optional[str] = None
    phone_number: Optional[str] = None
    secondary_phone: Optional[str] = None
    phone_numbers: Optional[List[str]] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    website_link: Optional[str] = None
    description: Optional[str] = None

class OrganisationResponse(OrganisationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
