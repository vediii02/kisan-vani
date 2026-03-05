import asyncio
import aiohttp
import json

async def main():
    payload = {
        "name": "adsas",
        "username": "ad2",  # changed from "ad" to "ad2"
        "admin_password": ""
    }
    headers = {
        "Content-Type": "application/json",
        # We need a superadmin token! Oh I don't have one
    }
    # It's better to just edit the endpoint to print what it receives
