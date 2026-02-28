"""
Test script to verify company profile API
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from db.session import AsyncSessionLocal
from db.models.user import User
from db.models.company import Company
from core.auth import verify_password, create_access_token


async def test_company_profile():
    """Test company profile API with real data"""
    async with AsyncSessionLocal() as db:
        try:
            # Find company user
            result = await db.execute(
                select(User).where(User.username == "nihu02")
            )
            user = result.scalar_one_or_none()
            
            if not user:
                print("❌ User 'nihu02' not found")
                return
            
            print(f"✅ Found user: {user.username} (Role: {user.role}, Company ID: {user.company_id})")
            
            # Get company details
            result = await db.execute(
                select(Company).where(Company.id == user.company_id)
            )
            company = result.scalar_one_or_none()
            
            if not company:
                print("❌ Company not found for user")
                return
            
            print(f"✅ Found company: {company.name}")
            print(f"   - Email: {company.email}")
            print(f"   - Phone: {company.phone}")
            print(f"   - Address: {company.address}")
            print(f"   - City: {company.city}")
            print(f"   - State: {company.state}")
            print(f"   - Pincode: {company.pincode}")
            print(f"   - Website: {company.website_link}")
            print(f"   - Description: {company.description}")
            
            # Create access token
            token_data = {
                "sub": user.username,
                "user_id": user.id,
                "role": user.role,
                "company_id": user.company_id,
                "organisation_id": user.organisation_id
            }
            access_token = create_access_token(data=token_data)
            print(f"✅ Generated access token for testing")
            
            print(f"\n🔗 Test API calls:")
            print(f"GET: http://localhost:8001/api/company/profile")
            print(f"Authorization: Bearer {access_token}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_company_profile())
