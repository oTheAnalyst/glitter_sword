import os
import requests
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

# --- CONFIGURATION: Replace these with your app's details ---
CLIENT_ID = os.environ.get('EVE_CLIENT_ID') or input("Enter your EVE Client ID: ")
CLIENT_SECRET = os.environ.get('EVE_CLIENT_SECRET') or input("Enter your EVE Client Secret: ")
SCOPES = "esi-contracts.read_corporation_contracts.v1"
REDIRECT_PORT = 65010  # Must match EXACTLY what is in your EVE Developer app
REDIRECT_URI = f"http://localhost:{REDIRECT_PORT}/callback"
# ----------------------------------------------------------

# Step 1: Generate the authorization URL
def get_auth_url():
    params = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "scope": SCOPES,
        "state": "unique-random-string"  # CSRF protection, can be any string
    }
    return f"https://login.eveonline.com/v2/oauth/authorize/?{urllib.parse.urlencode(params)}"

# Step 2: Simple HTTP server to catch the redirect with the authorization code
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the callback URL to extract the authorization code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        if 'code' in params:
            self.server.auth_code = params['code'][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this window and return to the terminal.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Error: No authorization code received.")
        
        # Shut down the server after handling the request
        threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        # Suppress log output to keep terminal clean
        return

import threading

# Step 3: Start the local server, open the browser, and wait for the callback
def get_authorization_code():
    server = HTTPServer(('localhost', REDIRECT_PORT), CallbackHandler)
    server.auth_code = None
    
    print(f"Opening your browser to log in to EVE Online...")
    webbrowser.open(get_auth_url())
    print(f"Waiting for authorization (listening on {REDIRECT_URI})...")
    
    server.timeout = 120  # 2-minute timeout
    server.handle_request()
    
    if server.auth_code is None:
        print("Error: Timeout waiting for authorization.")
        sys.exit(1)
    
    return server.auth_code

# Step 4: Exchange the authorization code for tokens
def exchange_code_for_tokens(auth_code):
    url = "https://login.eveonline.com/v2/oauth/token"
    auth = (CLIENT_ID, CLIENT_SECRET)
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(url, auth=auth, data=data)
    response.raise_for_status()
    return response.json()

# --- Main execution ---
if __name__ == "__main__":
    print("=== EVE Online One-Time OAuth Setup ===\n")
    
    auth_code = get_authorization_code()
    print("\nAuthorization code received. Exchanging for tokens...")
    
    tokens = exchange_code_for_tokens(auth_code)
    
    refresh_token = tokens['refresh_token']
    access_token = tokens['access_token']  # This one is short-lived, just for verification
    
    print("\n✅ Setup complete! Your tokens:")
    print(f"Access Token (valid 20 min): {access_token[:50]}...")
    print(f"\n🔑 REFRESH TOKEN (store this securely!):\n{refresh_token}")
    print("\n--- Instructions ---")
    print("1. Copy the refresh token above.")
    print("2. Set it as an environment variable or save it in a secure .env file:")
    print("   export EVE_REFRESH_TOKEN='your_refresh_token_here'")
    print("3. Your automated script will now use this to get new access tokens.")
