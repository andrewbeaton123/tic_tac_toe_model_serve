

import secrets
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from tic_tac_toe_model_serve.settings import settings

API_KEY = settings.API_KEY
API_KEY_NAME = "tic-tac-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if secrets.compare_digest(api_key_header, API_KEY):
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
