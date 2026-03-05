import asyncio
import aiohttp
import sys

async def main():
    async with aiohttp.ClientSession() as session:
        # First login to get a superadmin token
        login_data = {
            "username": "vedii02", # The superadmin from the screenshot
            "password": "rootpassword" # Assuming standard local pw
        }
        res = await session.post("http://kisanvani_backend:8001/api/auth/login", data=login_data)
        if res.status != 200:
            print("Login failed:", await res.text())
            return
            
        data = await res.json()
        token = data.get("access_token")
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        # Now update organisation 10 (ddd)
        payload = {
            "name": "Org 10 Test",
            "username": "ddd_updated",
            "email": "ddd@example.com"
        }
        
        update_res = await session.put("http://kisanvani_backend:8001/api/superadmin/organisations/10", json=payload, headers=headers)
        print("Update response status:", update_res.status)
        print("Update response body:", await update_res.text())

asyncio.run(main())
