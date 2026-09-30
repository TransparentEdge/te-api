import json
import os
import time
from typing import Any

import requests

from .config import Config


class AuthError(Exception):
    """Could not obtain an OAuth2 token: missing credentials, the token
    endpoint rejected them, or it could not be reached."""

    def __init__(self, message: str, status: int | None = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


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
    try:
        Config.validate()
    except ValueError as exc:
        raise AuthError(str(exc)) from exc

    auth_url = f"{Config.API_URL}/v1/oauth2/access_token/"
    payload = {
        "grant_type": "client_credentials",
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
    }

    try:
        response = requests.post(auth_url, data=payload, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        status = body = None
        if e.response is not None:
            status = e.response.status_code
            try:
                body = e.response.json()
            except ValueError:
                body = e.response.text
        raise AuthError(f"Error authenticating: {e}", status=status, body=body) from e

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


def get_auth_headers():
    token = get_valid_token()
    return {"Authorization": f"Bearer {token}"}
