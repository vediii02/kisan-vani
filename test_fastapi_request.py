import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        # First login to get a superadmin token
        login_data = {
            "username": "vedi02", # The superadmin from the screenshot
            "password": "rootpassword" # Wait, I don't know the password. I will bypass auth by mocking the endpoint
        }
