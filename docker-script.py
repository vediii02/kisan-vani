import asyncio
from db.base import AsyncSessionLocal
from sqlalchemy import select
from db.models.user import User

async def main():
    async with AsyncSessionLocal() as db:
        admin_user_result = await db.execute(
            select(User).where(User.organisation_id == 9, User.role == 'organisation')
        )
        admin_user = admin_user_result.scalars().first()
        if admin_user:
            print(f"Found user before update: {admin_user.username}")
            admin_user.username = admin_user.username + "_test"
            db.add(admin_user)
            await db.commit()
            print(f"Updated user to: {admin_user.username}")
        else:
            print("No admin user found.")
            
        admin_user_result2 = await db.execute(
            select(User).where(User.organisation_id == 9, User.role == 'organisation')
        )
        admin_user2 = admin_user_result2.scalars().first()
        print(f"Verification from DB: {admin_user2.username}")
        
        # restore
        admin_user2.username = admin_user2.username.replace("_test", "")
        db.add(admin_user2)
        await db.commit()

asyncio.run(main())
