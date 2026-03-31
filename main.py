"""FastAPI entry point for Cloud Run deployment."""

import os

import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DB_URI = "sqlite+aiosqlite:///./sessions.db"
ALLOWED_ORIGINS = ["*"]
SERVE_WEB_UI = True

app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URI,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_UI,
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
