import os
from fastapi import HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise Exception("API KEY NOT LOADED")
API_KEY_NAME = "tic-tac-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
