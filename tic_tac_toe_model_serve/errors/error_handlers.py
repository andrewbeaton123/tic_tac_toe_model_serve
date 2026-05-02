
from fastapi import Request
from fastapi.responses import JSONResponse


async def no_valid_moves_available_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=422,
        content={"detail": "No valid moves available."},
    )
