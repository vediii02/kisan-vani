import asyncio
from db.base import AsyncSessionLocal
from sqlalchemy import select
from db.models.user import User

async def main():
    async with AsyncSessionLocal() as db:
        users = await db.execute(select(User).where(User.organisation_id == 9))
        for u in users.scalars():
            print(f"ID: {u.id}, Username: {u.username}, Role: {u.role}")

asyncio.run(main())
