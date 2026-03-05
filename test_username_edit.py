import asyncio
from db.base import AsyncSessionLocal
from sqlalchemy import select
from db.models.user import User
from db.models.organisation import Organisation

async def main():
    async with AsyncSessionLocal() as db:
        # Simulate update_organisation logic
        org_id = 9
        body = {"username": "ad2", "admin_password": ""}
        
        result = await db.execute(select(Organisation).where(Organisation.id == org_id))
        org = result.scalar_one_or_none()
        
        admin_user_result = await db.execute(
            select(User).where(User.organisation_id == org.id, User.role == 'organisation')
        )
        admin_user = admin_user_result.scalars().first()

        if admin_user:
            if "username" in body and body["username"]:
                new_username = body["username"].strip()
                if new_username != admin_user.username:
                    print(f"Updating username from {admin_user.username} to {new_username}")
                    admin_user.username = new_username
                    db.add(admin_user)
            db.add(org)
            await db.commit()
            print("Commit successful!")
            
            # verify immediately
            await db.refresh(admin_user)
            print("After refresh:", admin_user.username)
        else:
            print("No admin user found")

asyncio.run(main())
