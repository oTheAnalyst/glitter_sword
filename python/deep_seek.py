import requests
import json
import duckdb

def eve_esi(contract_id):
    url = f'https://esi.evetech.net/corporations/98224639/contracts/{contract_id}/items'
    headers = {
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

# Fetch data
con = duckdb.connect("dirty_contracts.ddb")
contracts_ids = con.sql("SELECT distinct contract_id from stg.dng_contract").fetchall()
ids_list = [int(row[0]) for row in contracts_ids]
con.close()

# Export as NDJSON (BEST for DuckDB)
with open('mega_ndjson.json', 'w') as f:
    for contract_id in ids_list:
        print(f"Processing contract {contract_id}")
        contract_data = eve_esi(contract_id)
        if contract_data:
            # Create a flat record for each item
            for item in contract_data:
                record = {
                    'contract_id': contract_id,
                    'record_id': item.get('record_id'),
                    'type_id': item.get('type_id'),
                    'quantity': item.get('quantity'),
                    'raw_quantity': item.get('raw_quantity'),
                    'singleton': item.get('singleton', False),
                    'flag': item.get('flag')
                }
                f.write(json.dumps(record) + '\n')

print("Exported as NDJSON to mega_ndjson.json")

