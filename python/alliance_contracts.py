import requests
import json
url = "https://esi.evetech.net/corporations/98224639/contracts"

headers = {
    "Accept-Language": "",
    "If-None-Match": "",
    "X-Compatibility-Date": "2025-12-16",
    "X-Tenant": "",
    "If-Modified-Since": "",
    "Accept": "application/json",
}

response = requests.get(url, headers=headers)

with open('data/dng_contracts_current.json', 'w') as f:
 f.write(json.dumps(response.json()))
