from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from core.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    get_current_active_user
)
from db.session import get_db
from db.models.user import User
from db.models.organisation import Organisation
from db.models.company import Company

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=[" authentication"])

# Models
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    role: str = "company"
    organisation_name: Optional[str] = None
    organisation_id: Optional[int] = None
    company_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserProfile(BaseModel):
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: str

@router.get("/organisations")
async def get_active_organisations(db: AsyncSession = Depends(get_db)):
    """Get list of active organisations for company registration"""
    try:
        result = await db.execute(
            select(Organisation)
            .where(Organisation.status == "active")
            .order_by(Organisation.name)
        )
        organisations = result.scalars().all()
        
        org_list = []
        for org in organisations:
            org_list.append({
                "id": org.id,
                "name": org.name,
                "domain": org.domain
            })
        
        return {
            "organisations": org_list,
            "total": len(org_list)
        }
    except Exception as e:
        logger.error(f"Error fetching organisations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch organisations")

@router.post("/register", response_model=dict)
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).where(
        (User.username == user.username) | (User.email == user.email)
    ))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already registered")
        else:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        role=user.role,
        is_active=True
    )
    
    db.add(new_user)
    await db.flush()  # Get the user ID without committing
    
    # Create organisation if role is organisation
    if user.role == "organisation" and user.organisation_name:
        # Generate domain from organisation name
        domain = user.organisation_name.lower().replace(" ", "").replace(".", "") + ".kisanvani.ai"
        
        new_organisation = Organisation(
            name=user.organisation_name,
            domain=domain,
            status="pending",  # Set as pending for approval
            plan_type="basic",
            preferred_languages="hi",
            greeting_message=f"Namaste, aap {user.organisation_name} Kisan Sahayak AI se baat kar rahe hain"
        )
        
        db.add(new_organisation)
        await db.flush()  # Get the organisation ID
        
        # Link user to organisation and set user as inactive until approved
        new_user.organisation_id = new_organisation.id
        new_user.is_active = False  # User cannot login until approved
        
        logger.info(f"Organisation created with pending status: {user.organisation_name} with user: {user.username}")
    
    # Create company if role is company
    elif user.role == "company" and user.company_name:
        # For company users, we need an organisation first
        if user.organisation_id:
            # Use the selected organisation by ID
            org_result = await db.execute(select(Organisation).where(Organisation.id == user.organisation_id))
            organisation = org_result.scalar_one_or_none()
            
            if not organisation:
                raise HTTPException(status_code=400, detail="Selected organisation not found")
            
            if organisation.status != "active":
                raise HTTPException(status_code=400, detail="Selected organisation is not active")
        elif user.organisation_name:
            # Fallback to organisation name (for backward compatibility)
            org_result = await db.execute(select(Organisation).where(Organisation.name == user.organisation_name))
            organisation = org_result.scalar_one_or_none()
            
            if not organisation:
                raise HTTPException(status_code=400, detail="Organisation not found")
        else:
            raise HTTPException(status_code=400, detail="Organisation is required for company registration")
        
        # Create company
        new_company = Company(
            name=user.company_name,
            organisation_id=organisation.id,
            business_type="Agriculture",
            brand_name=user.company_name,
            contact_person=user.full_name,
            email=user.email,
            status="active"
        )
        
        db.add(new_company)
        await db.flush()
        
        # Link user to company and organisation
        new_user.company_id = new_company.id
        new_user.organisation_id = organisation.id
        new_user.is_active = False  # Company users need organisation approval
        
        logger.info(f"Company created: {user.company_name} under organisation: {organisation.name} with user: {user.username}")
    
    await db.commit()
    logger.info(f"User registered: {user.username} with role: {user.role}")
    
    return {
        "message": "User registered successfully",
        "username": user.username,
        "role": user.role
    }

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Find user
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        # For organisation users, check if their organisation is approved
        if user.role == "organisation" and user.organisation_id:
            org_result = await db.execute(select(Organisation).where(Organisation.id == user.organisation_id))
            organisation = org_result.scalar_one_or_none()
            
            if organisation and organisation.status == "pending":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Your organisation registration is pending approval. Please wait for super admin approval."
                )
            elif organisation and organisation.status == "inactive":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Your organisation account has been deactivated. Please contact support."
                )
        
        # For company users, check if they are approved by organisation
        elif user.role == "company":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your company user registration is pending approval. Please wait for organisation admin approval."
            )
        
        # For other inactive users
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated. Please contact support."
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    # Prepare user data
    user_data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }
    
    logger.info(f"User logged in: {user.username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }

@router.post("/login-json", response_model=Token)
async def login_json(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    # Find user
    result = await db.execute(select(User).where(User.username == credentials.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    # Prepare user data
    user_data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }
    
    logger.info(f"User logged in: {user.username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }

@router.get("/me", response_model=UserProfile)
async def get_profile(current_user: dict = Depends(get_current_active_user)):
    return current_user

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_active_user)):
    logger.info(f"User logged out: {current_user['username']}")
    return {"message": "Logged out successfully"}

@router.put("/profile")
async def update_profile(
    full_name: Optional[str] = None,
    email: Optional[EmailStr] = None,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Get current user from DB
    result = await db.execute(select(User).where(User.username == current_user["username"]))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is already taken
    if email and email != user.email:
        result = await db.execute(select(User).where(User.email == email))
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = email
    
    if full_name:
        user.full_name = full_name
    
    await db.commit()
    await db.refresh(user)
    logger.info(f"Profile updated: {user.username}")
    
    # Return updated user
    return {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Get user from DB
    result = await db.execute(select(User).where(User.username == current_user["username"]))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify old password
    if not verify_password(password_data.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    # Update password
    user.hashed_password = get_password_hash(password_data.new_password)
    await db.commit()
    
    logger.info(f"Password changed: {user.username}")
    return {"message": "Password changed successfully"}
