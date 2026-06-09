import requests
import json
import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
CLIENT_ID = os.environ.get("EVE_CLIENT_ID")
# Note: CLIENT_SECRET is not used with PKCE tokens
REFRESH_TOKEN = os.environ.get("EVE_REFRESH_TOKEN")


def get_access_token():
    url = "https://login.eveonline.com/v2/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,  # Required in body for PKCE
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


# -- eve esi bucket
def eve_esi(character_id):
    access_token = get_access_token()
    url = f"https://esi.evetech.net/v4/characters/{character_id}/"  # Added version and trailing slash
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",  # Added authorization header
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching character {character_id}: HTTP {response.status_code}")
        return None


# Fetch data
con = duckdb.connect("md:glitter_sword")
character_id = con.sql(
    "SELECT DISTINCT issuer_id FROM 'data/allaince_contracts_main.json'"
).fetchall()
ids_list = [int(row[0]) for row in character_id]
con.close()

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Export as NDJSON (BEST for DuckDB)
with open("data/issuer_records.json", "w") as f:
    for character_id in ids_list:
        print(f"Processing character {character_id}")
        contract_data = eve_esi(character_id)
        if contract_data:  # Only write if we got valid data
            f.write(json.dumps(contract_data) + "\n")

print("Exported as NDJSON to issuer_records.json")

con = duckdb.connect("md:glitter_sword")
acceptor_id = con.sql(
    "SELECT DISTINCT acceptor_id FROM 'data/allaince_contracts_main.json'"
).fetchall()
ids_list = [int(row[0]) for row in acceptor_id]
con.close()

# Export as NDJSON (BEST for DuckDB)
with open("data/acceptor_dimension.json", "w") as f:
    for acceptor_id in ids_list:
        print(f"Processing character {acceptor_id}")
        contract_data = eve_esi(acceptor_id)
        if contract_data:  # Only write if we got valid data
            f.write(json.dumps(contract_data) + "\n")

print("Exported as NDJSON to acceptor_id.json")
