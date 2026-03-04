import os
import json
from dotenv import load_dotenv
from pathlib import Path

# Load from .env file if it exists
load_dotenv()
# We try to load the user environment if it exists.
home_env = Path.home() / ".env"
if home_env.is_file():
    # Override is false by default, so it won't load any other variable if it's already set.
    load_dotenv(dotenv_path=home_env)

class Config:
    API_URL = os.getenv("TRANSPARENT_API_URL", "https://api.transparentcdn.com")
    CLIENT_ID = os.getenv("TRANSPARENT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TRANSPARENT_CLIENT_SECRET")
    BASE_DIR = os.path.expanduser("~/.te-api")
    TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
    CONTEXT_FILE = os.path.join(BASE_DIR, "context.json")

    @classmethod
    def validate(cls):
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            raise ValueError(
                "TRANSPARENT_CLIENT_ID and TRANSPARENT_CLIENT_SECRET must be set in environment variables or .env file."
            )

    @classmethod
    def set_context(cls, key, value):
        os.makedirs(cls.BASE_DIR, exist_ok=True)
        context = {}
        if os.path.exists(cls.CONTEXT_FILE):
            try:
                with open(cls.CONTEXT_FILE, "r") as f:
                    context = json.load(f)
            except json.JSONDecodeError:
                pass

        context[key] = value
        with open(cls.CONTEXT_FILE, "w") as f:
            json.dump(context, f)

    @classmethod
    def get_context(cls, key):
        if os.path.exists(cls.CONTEXT_FILE):
            try:
                with open(cls.CONTEXT_FILE, "r") as f:
                    context = json.load(f)
                    return context.get(key)
            except json.JSONDecodeError:
                pass
        return None
