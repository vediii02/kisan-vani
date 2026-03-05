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
            print(f"Current username: {admin_user.username}")
        else:
            print("No admin user found.")
            
asyncio.run(main())
