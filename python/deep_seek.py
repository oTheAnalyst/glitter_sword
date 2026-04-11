import requests
import json
import duckdb

def eve_esi(contract_id):
    url = f'https://esi.evetech.net/corporations/98224639/contracts/{contract_id}/items'
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkpXVC1TaWduYXR1cmUtS2V5IiwidHlwIjoiSldUIn0.eyJzY3AiOlsiZXNpLWNhbGVuZGFyLnJlc3BvbmRfY2FsZW5kYXJfZXZlbnRzLnYxIiwiZXNpLWNhbGVuZGFyLnJlYWRfY2FsZW5kYXJfZXZlbnRzLnYxIiwiZXNpLWxvY2F0aW9uLnJlYWRfbG9jYXRpb24udjEiLCJlc2ktbG9jYXRpb24ucmVhZF9zaGlwX3R5cGUudjEiLCJlc2ktbWFpbC5vcmdhbml6ZV9tYWlsLnYxIiwiZXNpLW1haWwucmVhZF9tYWlsLnYxIiwiZXNpLW1haWwuc2VuZF9tYWlsLnYxIiwiZXNpLXNraWxscy5yZWFkX3NraWxscy52MSIsImVzaS1za2lsbHMucmVhZF9za2lsbHF1ZXVlLnYxIiwiZXNpLXdhbGxldC5yZWFkX2NoYXJhY3Rlcl93YWxsZXQudjEiLCJlc2ktc2VhcmNoLnNlYXJjaF9zdHJ1Y3R1cmVzLnYxIiwiZXNpLWNsb25lcy5yZWFkX2Nsb25lcy52MSIsImVzaS1jaGFyYWN0ZXJzLnJlYWRfY29udGFjdHMudjEiLCJlc2ktdW5pdmVyc2UucmVhZF9zdHJ1Y3R1cmVzLnYxIiwiZXNpLWtpbGxtYWlscy5yZWFkX2tpbGxtYWlscy52MSIsImVzaS1jb3Jwb3JhdGlvbnMucmVhZF9jb3Jwb3JhdGlvbl9tZW1iZXJzaGlwLnYxIiwiZXNpLWFzc2V0cy5yZWFkX2Fzc2V0cy52MSIsImVzaS1wbGFuZXRzLm1hbmFnZV9wbGFuZXRzLnYxIiwiZXNpLWZsZWV0cy5yZWFkX2ZsZWV0LnYxIiwiZXNpLWZsZWV0cy53cml0ZV9mbGVldC52MSIsImVzaS11aS5vcGVuX3dpbmRvdy52MSIsImVzaS11aS53cml0ZV93YXlwb2ludC52MSIsImVzaS1jaGFyYWN0ZXJzLndyaXRlX2NvbnRhY3RzLnYxIiwiZXNpLWZpdHRpbmdzLnJlYWRfZml0dGluZ3MudjEiLCJlc2ktZml0dGluZ3Mud3JpdGVfZml0dGluZ3MudjEiLCJlc2ktbWFya2V0cy5zdHJ1Y3R1cmVfbWFya2V0cy52MSIsImVzaS1jb3Jwb3JhdGlvbnMucmVhZF9zdHJ1Y3R1cmVzLnYxIiwiZXNpLWNoYXJhY3RlcnMucmVhZF9sb3lhbHR5LnYxIiwiZXNpLWNoYXJhY3RlcnMucmVhZF9tZWRhbHMudjEiLCJlc2ktY2hhcmFjdGVycy5yZWFkX3N0YW5kaW5ncy52MSIsImVzaS1jaGFyYWN0ZXJzLnJlYWRfYWdlbnRzX3Jlc2VhcmNoLnYxIiwiZXNpLWluZHVzdHJ5LnJlYWRfY2hhcmFjdGVyX2pvYnMudjEiLCJlc2ktbWFya2V0cy5yZWFkX2NoYXJhY3Rlcl9vcmRlcnMudjEiLCJlc2ktY2hhcmFjdGVycy5yZWFkX2JsdWVwcmludHMudjEiLCJlc2ktY2hhcmFjdGVycy5yZWFkX2NvcnBvcmF0aW9uX3JvbGVzLnYxIiwiZXNpLWxvY2F0aW9uLnJlYWRfb25saW5lLnYxIiwiZXNpLWNvbnRyYWN0cy5yZWFkX2NoYXJhY3Rlcl9jb250cmFjdHMudjEiLCJlc2ktY2xvbmVzLnJlYWRfaW1wbGFudHMudjEiLCJlc2ktY2hhcmFjdGVycy5yZWFkX2ZhdGlndWUudjEiLCJlc2kta2lsbG1haWxzLnJlYWRfY29ycG9yYXRpb25fa2lsbG1haWxzLnYxIiwiZXNpLWNvcnBvcmF0aW9ucy50cmFja19tZW1iZXJzLnYxIiwiZXNpLXdhbGxldC5yZWFkX2NvcnBvcmF0aW9uX3dhbGxldHMudjEiLCJlc2ktY2hhcmFjdGVycy5yZWFkX25vdGlmaWNhdGlvbnMudjEiLCJlc2ktY29ycG9yYXRpb25zLnJlYWRfZGl2aXNpb25zLnYxIiwiZXNpLWNvcnBvcmF0aW9ucy5yZWFkX2NvbnRhY3RzLnYxIiwiZXNpLWFzc2V0cy5yZWFkX2NvcnBvcmF0aW9uX2Fzc2V0cy52MSIsImVzaS1jb3Jwb3JhdGlvbnMucmVhZF90aXRsZXMudjEiLCJlc2ktY29ycG9yYXRpb25zLnJlYWRfYmx1ZXByaW50cy52MSIsImVzaS1jb250cmFjdHMucmVhZF9jb3Jwb3JhdGlvbl9jb250cmFjdHMudjEiLCJlc2ktY29ycG9yYXRpb25zLnJlYWRfc3RhbmRpbmdzLnYxIiwiZXNpLWNvcnBvcmF0aW9ucy5yZWFkX3N0YXJiYXNlcy52MSIsImVzaS1pbmR1c3RyeS5yZWFkX2NvcnBvcmF0aW9uX2pvYnMudjEiLCJlc2ktbWFya2V0cy5yZWFkX2NvcnBvcmF0aW9uX29yZGVycy52MSIsImVzaS1jb3Jwb3JhdGlvbnMucmVhZF9jb250YWluZXJfbG9ncy52MSIsImVzaS1pbmR1c3RyeS5yZWFkX2NoYXJhY3Rlcl9taW5pbmcudjEiLCJlc2ktaW5kdXN0cnkucmVhZF9jb3Jwb3JhdGlvbl9taW5pbmcudjEiLCJlc2ktcGxhbmV0cy5yZWFkX2N1c3RvbXNfb2ZmaWNlcy52MSIsImVzaS1jb3Jwb3JhdGlvbnMucmVhZF9mYWNpbGl0aWVzLnYxIiwiZXNpLWNvcnBvcmF0aW9ucy5yZWFkX21lZGFscy52MSIsImVzaS1jaGFyYWN0ZXJzLnJlYWRfdGl0bGVzLnYxIiwiZXNpLWFsbGlhbmNlcy5yZWFkX2NvbnRhY3RzLnYxIiwiZXNpLWNoYXJhY3RlcnMucmVhZF9md19zdGF0cy52MSIsImVzaS1jb3Jwb3JhdGlvbnMucmVhZF9md19zdGF0cy52MSIsImVzaS1jb3Jwb3JhdGlvbnMucmVhZF9wcm9qZWN0cy52MSIsImVzaS1jb3Jwb3JhdGlvbnMucmVhZF9mcmVlbGFuY2Vfam9icy52MSIsImVzaS1jaGFyYWN0ZXJzLnJlYWRfZnJlZWxhbmNlX2pvYnMudjEiLCJlc2ktc3RydWN0dXJlcy5yZWFkX2NvcnBvcmF0aW9uLnYxIiwiZXNpLXN0cnVjdHVyZXMucmVhZF9jaGFyYWN0ZXIudjEiLCJlc2ktYWN0aXZpdGllcy5yZWFkX2NoYXJhY3Rlci52MSIsImVzaS1hY2Nlc3MucmVhZF9saXN0cy52MSJdLCJqdGkiOiJkMjU4NTQ0ZC0yMzM2LTQ5MTEtOTAxNC1hOWYxMjE1ZWM5NTciLCJraWQiOiJKV1QtU2lnbmF0dXJlLUtleSIsInN1YiI6IkNIQVJBQ1RFUjpFVkU6OTIwNDgzOTIiLCJhenAiOiJkZXZlbG9wZXJzX2V2ZW9ubGluZV9jb20iLCJ0ZW5hbnQiOiJ0cmFucXVpbGl0eSIsInRpZXIiOiJsaXZlIiwicmVnaW9uIjoid29ybGQiLCJhdWQiOlsiZGV2ZWxvcGVyc19ldmVvbmxpbmVfY29tIiwiRVZFIE9ubGluZSJdLCJuYW1lIjoiQWxtYW5hYyBPbWFyaXN0b3MiLCJvd25lciI6Ik9xd3FBZjU1SXdaaG9nL3hiaW1QUkRPY1Erbz0iLCJleHAiOjE3NzUyMjEzOTksImlhdCI6MTc3NTIyMDE5OSwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5ldmVvbmxpbmUuY29tIn0.MIlcS7w56g10V3u8lqvInidHK0mhNVCo8gQcfFc8GkWXjjUiFZpV7gnE0hhTM3j5fBFP3j2wkCdgkMGb0EPVSkqKXPuES4WuZMKQM8D0GFHinwkXF-0jq2nVNJ6ICKaU6ukjArxWpxLv4yVBk9Jen1V7eLNFxztcKj79x3BXMkrMpIxp7dcqKQnRee6FItKgMr55WT47Oe4eH6SD9V_eQWG48AGXa8sOtMlYl_UWZX0WHI3P6ThrUzR6un7EIveMdWYPt2Cmwo_KHCSKRDI1_bUtkVYCKCJZv-V8FktK3AbF83RbT1VGC2GeYDb8_d6Tw19NaKwUCJA4XtrO7QQP6Q"
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

