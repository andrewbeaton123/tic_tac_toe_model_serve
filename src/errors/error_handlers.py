
from fastapi import Request
from fastapi.responses import JSONResponse
from src.errors.error_class import NoValidMovesAvailable

async def no_valid_moves_available_handler(request: Request, exc: NoValidMovesAvailable):
    return JSONResponse(
        status_code=422,
        content={"detail": "No valid moves available."},
    )
