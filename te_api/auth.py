import json
import os
import time
import requests
from .config import Config


def ensure_token_dir():
    os.makedirs(Config.BASE_DIR, exist_ok=True)


def get_valid_token():
    ensure_token_dir()

    token_data = None
    if os.path.exists(Config.TOKEN_FILE):
        try:
            with open(Config.TOKEN_FILE, "r") as f:
                token_data = json.load(f)
        except json.JSONDecodeError:
            pass

    if token_data:
        expires_at = token_data.get("expires_at")
        if expires_at and expires_at > time.time():
            return token_data.get("access_token")

    # If no valid token, authenticate
    Config.validate()

    auth_url = f"{Config.API_URL}/v1/oauth2/access_token/"
    payload = {
        "grant_type": "client_credentials",
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
    }

    try:
        response = requests.post(auth_url, data=payload)
        response.raise_for_status()
        data = response.json()

        access_token = data.get("access_token")
        expires_in = data.get("expires_in", 36000)

        token_data = {
            "access_token": access_token,
            "expires_at": time.time()
            + expires_in
            - 60,  # Subtract 60s for safety margin
        }

        with open(Config.TOKEN_FILE, "w") as f:
            json.dump(token_data, f)

        return access_token

    except requests.exceptions.RequestException as e:
        print(f"Error authenticating: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
        raise


def get_auth_headers():
    token = get_valid_token()
    return {"Authorization": f"Bearer {token}"}
