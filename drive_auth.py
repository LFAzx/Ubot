import os
import json
import sqlite3
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest

CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
APP_URL = os.environ.get("APP_URL")
REDIRECT_URI = f"{APP_URL}/oauth/callback" if APP_URL else None

SCOPES = ["https://www.googleapis.com/auth/drive"]

DB_PATH = "drive_tokens.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS tokens (user_id INTEGER PRIMARY KEY, token_json TEXT)")
    conn.commit()
    conn.close()


_init_db()

_pending_states = {}


def _client_config():
    return {
        "web": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI],
        }
    }


def build_auth_url(telegram_user_id):
    flow = Flow.from_client_config(_client_config(), scopes=SCOPES, redirect_uri=REDIRECT_URI)
    auth_url, state = flow.authorization_url(access_type="offline", prompt="consent")
    _pending_states[state] = telegram_user_id
    return auth_url


def handle_callback(state, code):
    telegram_user_id = _pending_states.pop(state, None)
    if telegram_user_id is None:
        return None

    flow = Flow.from_client_config(_client_config(), scopes=SCOPES, redirect_uri=REDIRECT_URI)
    flow.fetch_token(code=code)
    creds = flow.credentials

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO tokens (user_id, token_json) VALUES (?, ?)",
        (telegram_user_id, creds.to_json()),
    )
    conn.commit()
    conn.close()
    return telegram_user_id


def get_credentials(telegram_user_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT token_json FROM tokens WHERE user_id = ?", (telegram_user_id,)).fetchone()
    conn.close()
    if not row:
        return None

    creds = Credentials.from_authorized_user_info(json.loads(row[0]), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(GoogleRequest())
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE tokens SET token_json = ? WHERE user_id = ?", (creds.to_json(), telegram_user_id))
        conn.commit()
        conn.close()
    return creds


def disconnect(telegram_user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM tokens WHERE user_id = ?", (telegram_user_id,))
    conn.commit()
    conn.close()
