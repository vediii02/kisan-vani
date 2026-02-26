from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timezone

from core.auth import get_current_user
from db.session import get_db
from db.models.user import User
from db.models.organisation import Organisation
from db.models.company import Company

router = APIRouter()

# ============================================================================
# MIDDLEWARE: Verify Organisation Role
# ============================================================================

async def verify_organisation_role(current_user: dict = Depends(get_current_user)):
    """Verify that the current user has organisation role"""
    if current_user.get("role") != "organisation":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Organisation role required."
        )
    return current_user

# ============================================================================
# GET: Pending Company User Approvals
# ============================================================================

@router.get("/pending-approvals")
async def get_pending_approvals(
    current_user: dict = Depends(verify_organisation_role),
    db: AsyncSession = Depends(get_db)
):
    """Get all pending company user registration approvals for this organisation"""
    
    # Get current user's organisation
    user_result = await db.execute(
        select(User).where(User.username == current_user["username"])
    )
    current_db_user = user_result.scalar_one_or_none()
    
    if not current_db_user or not current_db_user.organisation_id:
        raise HTTPException(status_code=404, detail="Organisation not found")
    
    # Find company users in this organisation who are inactive (pending approval)
    result = await db.execute(
        select(User)
        .options(selectinload(User.company))
        .where(
            and_(
                User.role == "company",
                User.is_active == False,
                User.organisation_id == current_db_user.organisation_id
            )
        )
        .order_by(User.created_at.desc())
    )
    
    pending_users = result.scalars().all()
    
    approvals = []
    for user in pending_users:
        if user.company and user.company.status == "active":
            approvals.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "company_name": user.company.name,
                "company_id": user.company.id,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "status": "pending"
            })
    
    return {
        "pending_approvals": approvals,
        "total": len(approvals)
    }

# ============================================================================
# POST: Approve Company User Registration
# ============================================================================

@router.post("/approve-user/{user_id}")
async def approve_user(
    user_id: int,
    current_user: dict = Depends(verify_organisation_role),
    db: AsyncSession = Depends(get_db)
):
    """Approve a pending company user registration"""
    
    # Get current user's organisation
    user_result = await db.execute(
        select(User).where(User.username == current_user["username"])
    )
    current_db_user = user_result.scalar_one_or_none()
    
    if not current_db_user or not current_db_user.organisation_id:
        raise HTTPException(status_code=404, detail="Organisation not found")
    
    # Find the user to approve
    result = await db.execute(
        select(User)
        .options(selectinload(User.company))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role != "company":
        raise HTTPException(status_code=400, detail="Only company users can be approved through this endpoint")
    
    if user.is_active:
        raise HTTPException(status_code=400, detail="User is already approved")
    
    # Verify the user belongs to the same organisation
    if user.organisation_id != current_db_user.organisation_id:
        raise HTTPException(status_code=403, detail="You can only approve users from your organisation")
    
    # Approve the user
    user.is_active = True
    
    await db.commit()
    
    return {
        "message": f"User {user.username} approved successfully",
        "user_id": user.id,
        "username": user.username,
        "company_name": user.company.name if user.company else None
    }

# ============================================================================
# POST: Reject Company User Registration
# ============================================================================

@router.post("/reject-user/{user_id}")
async def reject_user(
    user_id: int,
    current_user: dict = Depends(verify_organisation_role),
    db: AsyncSession = Depends(get_db)
):
    """Reject a pending company user registration"""
    
    # Get current user's organisation
    user_result = await db.execute(
        select(User).where(User.username == current_user["username"])
    )
    current_db_user = user_result.scalar_one_or_none()
    
    if not current_db_user or not current_db_user.organisation_id:
        raise HTTPException(status_code=404, detail="Organisation not found")
    
    # Find the user to reject
    result = await db.execute(
        select(User)
        .options(selectinload(User.company))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role != "company":
        raise HTTPException(status_code=400, detail="Only company users can be rejected through this endpoint")
    
    # Verify the user belongs to the same organisation
    if user.organisation_id != current_db_user.organisation_id:
        raise HTTPException(status_code=403, detail="You can only reject users from your organisation")
    
    # Store details for response
    username = user.username
    company_name = user.company.name if user.company else "Unknown"
    
    # Delete the user and associated company
    if user.company:
        await db.delete(user.company)
    
    await db.delete(user)
    await db.commit()
    
    return {
        "message": f"User {username} and company {company_name} rejected and deleted successfully",
        "user_id": user_id,
        "username": username,
        "company_name": company_name
    }

# ============================================================================
# GET: Approval Statistics
# ============================================================================

@router.get("/approval-stats")
async def get_approval_stats(
    current_user: dict = Depends(verify_organisation_role),
    db: AsyncSession = Depends(get_db)
):
    """Get approval statistics for organisation dashboard"""
    
    # Get current user's organisation
    user_result = await db.execute(
        select(User).where(User.username == current_user["username"])
    )
    current_db_user = user_result.scalar_one_or_none()
    
    if not current_db_user or not current_db_user.organisation_id:
        raise HTTPException(status_code=404, detail="Organisation not found")
    
    # Count pending approvals
    pending_result = await db.execute(
        select(User)
        .where(
            and_(
                User.role == "company",
                User.is_active == False,
                User.organisation_id == current_db_user.organisation_id
            )
        )
    )
    pending_count = len(pending_result.scalars().all())
    
    # Count approved company users
    approved_result = await db.execute(
        select(User).where(
            and_(
                User.role == "company",
                User.is_active == True,
                User.organisation_id == current_db_user.organisation_id
            )
        )
    )
    approved_count = len(approved_result.scalars().all())
    
    # Today's registrations
    today = datetime.now(timezone.utc).date()
    today_result = await db.execute(
        select(User).where(
            and_(
                User.role == "company",
                User.organisation_id == current_db_user.organisation_id,
                User.created_at >= today
            )
        )
    )
    today_count = len(today_result.scalars().all())
    
    return {
        "pending_count": pending_count,
        "approved_count": approved_count,
        "today_registrations": today_count,
        "total_company_users": pending_count + approved_count
    }
