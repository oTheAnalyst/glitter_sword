import requests
import json
import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration (Store these securely, not in code!) ---
CLIENT_ID = os.environ.get("EVE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("EVE_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("EVE_REFRESH_TOKEN")  # The token you got once manually


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
def eve_esi(contract_id):
    access_token = get_access_token()
    url = f"https://esi.evetech.net/corporations/98224639/contracts/{contract_id}/items"
    headers = {
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


# Fetch data
con = duckdb.connect("md:glitter_sword")
contracts_ids = con.sql(
    "SELECT distinct contract_id from 'data/dng_contracts_current.json'"
).fetchall()
ids_list = [int(row[0]) for row in contracts_ids]
con.close()

# Export as NDJSON (BEST for DuckDB)
with open("data/mega_ndjson.json", "w") as f:
    for contract_id in ids_list:
        print(f"Processing contract {contract_id}")
        contract_data = eve_esi(contract_id)
        if contract_data:
            # Create a flat record for each item
            for item in contract_data:
                record = {
                    "contract_id": contract_id,
                    "record_id": item.get("record_id"),
                    "type_id": item.get("type_id"),
                    "quantity": item.get("quantity"),
                    "raw_quantity": item.get("raw_quantity"),
                    "singleton": item.get("singleton", False),
                    "flag": item.get("flag"),
                }
                f.write(json.dumps(record) + "\n")

print("Exported as NDJSON to mega_ndjson.json")
