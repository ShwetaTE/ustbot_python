import sys
import os
import msal
import aiohttp
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DefaultConfig

CONFIG = DefaultConfig()

CLIENT_ID = CONFIG.APP_ID
TENANT_ID = CONFIG.APP_TENANTID

SCOPES = ["User.Read"]
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}/"

# Function to get access token asynchronously
async def get_access_token():
    print("[DEBUG] Initializing MSAL PublicClientApplication...")
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    accounts = app.get_accounts()
    
    print(f"[DEBUG] Found accounts: {accounts}")
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        print("[DEBUG] Acquired token silently.")
    else:
        loop = asyncio.get_event_loop()
        print("[DEBUG] Acquiring token interactively...")
        result = await loop.run_in_executor(None, app.acquire_token_interactive, SCOPES)
    
    if not result or "access_token" not in result:
        print("[ERROR] Failed to acquire access token.")
        return None
    
    print("[DEBUG] Access token acquired successfully.")
    return result.get("access_token")

# Function to fetch user email asynchronously
async def fetch_user_email():
    print("[DEBUG] Fetching access token...")
    token = await get_access_token()
    if not token:
        print("[ERROR] Authentication failed.")
        return None

    url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {token}"}

    print("[DEBUG] Sending request to Microsoft Graph API...")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                user_data = await response.json()
                print(f"[DEBUG] User data retrieved: {user_data}")
                return user_data.get("mail") or user_data.get("userPrincipalName")
            else:
                print(f"[ERROR] Failed to fetch user email. Status: {response.status}")

    return None

# Synchronous wrapper to fetch user email
async def get_user_email():
    return await fetch_user_email()
