import requests
import pandas 
import json
import duckdb

def eve_esi(contract_id):
    url = f'https://esi.evetech.net/corporations/98224639/contracts/{contract_id}/items'
    headers = {
        "Accept-Language": "",
        "If-None-Match": "",
        "X-Compatibility-Date": "2025-12-16",
        "X-Tenant": "",
        "If-Modified-Since": "",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    res = json.dumps(response.json())
    print(res)


con = duckdb.connect("dirty_contracts.ddb")
contracts_ids = con.sql("SELECT distinct contract_id from stg.dng_contract")
ids = contracts_ids.fetchall().str()

con.close()

for ids in ids:
    print(ids)


