import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


# --- Configuration ---
CLIENT_ID = os.environ.get('EVE_CLIENT_ID')
# Note: CLIENT_SECRET is not used with PKCE tokens
REFRESH_TOKEN = os.environ.get('EVE_REFRESH_TOKEN')

if not CLIENT_ID or not REFRESH_TOKEN:
    raise ValueError("❌ EVE_CLIENT_ID and EVE_REFRESH_TOKEN environment variables must be set.")

# --- Step 1: Automatically Get a New Access Token (PKCE version) ---
def get_access_token():
    url = "https://login.eveonline.com/v2/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID  # Required in body for PKCE
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['access_token']

# --- Step 2: Call the Endpoint with the Fresh Token ---
def get_corp_contracts():
    access_token = get_access_token()
    url = "https://esi.evetech.net/corporations/98224639/contracts"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# --- Your Main Logic ---
contracts_data = get_corp_contracts()
os.makedirs('data', exist_ok=True)
with open('data/dng_contracts_current.json', 'w') as f:
    json.dump(contracts_data, f, indent=2)
print("✅ Contracts data saved to data/dng_contracts_current.json")
