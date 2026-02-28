"""
Script to create sample organisations for testing
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from db.session import AsyncSessionLocal
from db.models.organisation import Organisation


async def create_sample_organisations():
    """Create sample organisations for testing"""
    async with AsyncSessionLocal() as db:
        try:
            # Sample organisations to create
            sample_orgs = [
                {
                    "name": "Rasi Seeds",
                    "email": "info@rasi.com",
                    "status": "active",
                    "plan_type": "professional",
                    "phone_number": "+91 8012345678",
                    "address": "123, Agricultural Market, Bangalore",
                    "city": "Bangalore",
                    "state": "Karnataka",
                    "pincode": "560001",
                    "website_link": "https://www.rasiseeds.com",
                    "description": "Leading agricultural seed company providing quality seeds to farmers"
                },
                {
                    "name": "AgriTech Solutions",
                    "email": "contact@agritech.com",
                    "status": "active",
                    "plan_type": "basic",
                    "phone_number": "+91 9876543210",
                    "address": "456, Tech Park, Hyderabad",
                    "city": "Hyderabad",
                    "state": "Telangana",
                    "pincode": "500001",
                    "website_link": "https://www.agritechsolutions.com",
                    "description": "Innovative agricultural technology solutions provider"
                },
                {
                    "name": "Green Harvest Pvt Ltd",
                    "email": "info@greenharvest.com",
                    "status": "active",
                    "plan_type": "enterprise",
                    "phone_number": "+91 9123456789",
                    "address": "789, Industrial Area, Pune",
                    "city": "Pune",
                    "state": "Maharashtra",
                    "pincode": "411001",
                    "website_link": "https://www.greenharvest.com",
                    "description": "Sustainable farming solutions and organic products"
                }
            ]
            
            created_count = 0
            for org_data in sample_orgs:
                # Check if organisation already exists
                result = await db.execute(
                    select(Organisation).where(Organisation.name == org_data["name"])
                )
                existing_org = result.scalar_one_or_none()
                
                if existing_org:
                    print(f"⚠️  Organisation '{org_data['name']}' already exists (ID: {existing_org.id})")
                else:
                    # Create new organisation
                    new_org = Organisation(**org_data)
                    db.add(new_org)
                    await db.commit()
                    await db.refresh(new_org)
                    print(f"✅ Created organisation: {new_org.name} (ID: {new_org.id})")
                    created_count += 1
            
            print(f"\n📊 Summary: Created {created_count} new organisations")
            
            # Show all organisations
            result = await db.execute(select(Organisation).where(Organisation.status == "active"))
            organisations = result.scalars().all()
            
            print(f"\n📋 All Active Organisations ({len(organisations)}):")
            for org in organisations:
                print(f"  - {org.name} (ID: {org.id})")
                
        except Exception as e:
            print(f"❌ Error creating organisations: {str(e)}")
            await db.rollback()


if __name__ == "__main__":
    asyncio.run(create_sample_organisations())
