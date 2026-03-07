from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.auth import get_current_user
from db.session import get_db
from db.models.company import Company
from db.models.brand import Brand
from db.models.organisation import Organisation
from pydantic import BaseModel, Field
from typing import Optional, List

router = APIRouter()

class CompanyProfileResponse(BaseModel):
    id: int
    name: str
    organisation_name: Optional[str] = None
    business_type: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    secondary_phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    website_link: Optional[str] = None
    description: Optional[str] = None
    gst_number: Optional[str] = None
    registration_number: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: Optional[str] = None

class CompanyProfileUpdate(BaseModel):
    name: Optional[str] = None
    business_type: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    secondary_phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    website_link: Optional[str] = None
    description: Optional[str] = None
    gst_number: Optional[str] = None
    registration_number: Optional[str] = None
    notes: Optional[str] = None

@router.get("/profile", response_model=CompanyProfileResponse)
async def get_company_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's company profile details"""
    if current_user.get("role") != "company":
        raise HTTPException(status_code=403, detail="Access denied. Company role required.")
    
    company_id = current_user.get("company_id")
    if not company_id:
        raise HTTPException(status_code=404, detail="Company not found for user.")
    
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found.")
    
    # Get organisation name
    org_name = None
    if company.organisation_id:
        org_result = await db.execute(select(Organisation).where(Organisation.id == company.organisation_id))
        org = org_result.scalar_one_or_none()
        if org:
            org_name = org.name
    
    return CompanyProfileResponse(
        id=company.id,
        name=company.name,
        organisation_name=org_name,
        business_type=company.business_type,
        contact_person=company.contact_person,
        phone=company.phone,
        secondary_phone=company.secondary_phone,
        email=company.email,
        address=company.address,
        city=company.city,
        state=company.state,
        pincode=company.pincode,
        website_link=company.website_link,
        description=company.description,
        gst_number=company.gst_number,
        registration_number=company.registration_number,
        status=company.status,
        notes=company.notes,
        created_at=company.created_at.isoformat() if company.created_at else None
    )

@router.put("/profile", response_model=CompanyProfileResponse)
async def update_company_profile(
    profile_update: CompanyProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's company profile details"""
    if current_user.get("role") != "company":
        raise HTTPException(status_code=403, detail="Access denied. Company role required.")
    
    company_id = current_user.get("company_id")
    if not company_id:
        raise HTTPException(status_code=404, detail="Company not found for user.")
    
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found.")
    
    # Update only provided fields
    update_data = profile_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    await db.commit()
    await db.refresh(company)
    
    return CompanyProfileResponse(
        id=company.id,
        name=company.name,
        business_type=company.business_type,
        contact_person=company.contact_person,
        phone=company.phone,
        secondary_phone=company.secondary_phone,
        email=company.email,
        address=company.address,
        city=company.city,
        state=company.state,
        pincode=company.pincode,
        website_link=company.website_link,
        description=company.description,
        gst_number=company.gst_number,
        registration_number=company.registration_number,
        status=company.status,
        notes=company.notes,
        created_at=company.created_at.isoformat() if company.created_at else None
    )
