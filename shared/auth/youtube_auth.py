import json
import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from shared.config import get_settings

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_PATH = Path("token.json")
CLIENT_SECRET_PATH = Path("client_secret.json")


def get_youtube_client():
    """OAuth2 인증을 통해 YouTube 업로드 클라이언트를 반환합니다."""
    settings = get_settings()
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_PATH.exists():
                _write_client_secret(settings)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")

    return build("youtube", "v3", credentials=creds)


def get_youtube_data_client():
    """API 키 기반 YouTube Data 조회 클라이언트를 반환합니다."""
    settings = get_settings()
    return build("youtube", "v3", developerKey=settings.youtube_api_key)


def _write_client_secret(settings) -> None:
    secret = {
        "installed": {
            "client_id": settings.youtube_client_id,
            "client_secret": settings.youtube_client_secret,
            "redirect_uris": ["http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    CLIENT_SECRET_PATH.write_text(json.dumps(secret), encoding="utf-8")
