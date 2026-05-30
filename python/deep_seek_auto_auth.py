import requests
import json
import os

# --- Configuration (Store these securely, not in code!) ---
CLIENT_ID = os.environ.get('EVE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('EVE_CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('EVE_REFRESH_TOKEN') # The token you got once manually

# --- Step 1: Automatically Get a New Access Token ---
def get_access_token():
    url = "https://login.eveonline.com/v2/oauth/token"
    auth = (CLIENT_ID, CLIENT_SECRET)
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    response = requests.post(url, auth=auth, data=data)
    response.raise_for_status() # Handle errors like an expired refresh token
    return response.json()['access_token']

# --- Step 2: Call the Endpoint with the Fresh Token ---
def get_corp_contracts():
    access_token = get_access_token()
    url = "https://esi.evetech.net/corporations/98224639/contracts"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}" # The magic part!
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# --- Your Main Logic ---
contracts_data = get_corp_contracts()
with open('data/dng_contracts_current.json', 'w') as f:
    json.dump(contracts_data, f, indent=2)
