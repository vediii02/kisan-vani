import asyncio
from db.session import async_session
from sqlalchemy import select
from db.models.user import User

async def main():
    async with async_session() as db:
        admin_user_result = await db.execute(
            select(User).where(User.organisation_id == 9, User.role == 'organisation')
        )
        admin_user = admin_user_result.scalars().first()
        if admin_user:
            print(f"Found user: {admin_user.username}")
        else:
            print("No admin user found.")

asyncio.run(main())
