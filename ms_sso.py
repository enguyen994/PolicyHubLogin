import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')

authorize_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

def get_microsoft_auth_url():
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'response_mode': 'query',
        'scope': 'openid profile email'
    }
    return f"{authorize_url}?{urlencode(params)}"

def exchange_code_for_token(code):
    data = {
        'client_id': CLIENT_ID,
        'scope': 'openid profile email',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()
    return None