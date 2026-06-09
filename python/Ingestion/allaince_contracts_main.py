import requests
import json
import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
CLIENT_ID = os.environ.get("EVE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("EVE_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("EVE_REFRESH_TOKEN")  # Your saved refresh token


def get_access_token(refresh_token, client_id, client_secret):
    """Exchange refresh token for a new access token"""
    auth_url = "https://login.eveonline.com/v2/oauth/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "login.eveonline.com",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(auth_url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print(f"Failed to refresh token: {response.status_code}")
        print(response.text)
        return None


# --- Get a valid access token ---
access_token = get_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)

if not access_token:
    print("Cannot proceed without a valid access token")
    exit(1)

# --- API Call to get corporation contracts ---
url = "https://esi.evetech.net/corporations/98224639/contracts"

headers = {
    "Authorization": f"Bearer {access_token}",  # Now using proper access token
    "Accept-Language": "en-us",
    "Accept": "application/json",
}

# Optional: Add query parameters for better control
params = {
    "page": 1,
    # "status": "outstanding",  # Uncomment to filter by status
}

response = requests.get(url, headers=headers, params=params)

# --- Save response ---
if response.status_code == 200:
    with open("data/allaince_contracts_main.json", "w") as f:
        f.write(json.dumps(response.json(), indent=2))
    print(f"Successfully saved {len(response.json())} contracts")
else:
    print(f"Error {response.status_code}: {response.text}")
