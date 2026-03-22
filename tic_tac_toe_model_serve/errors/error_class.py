
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    code: Optional[str] = None

class ProblemDetails(BaseModel):
    type: str
    title: str
    status: int
    detail: Optional[str] = None
    instance: Optional[str] = None
    errors: Optional[List[ErrorDetail]] = None # Custom extension for validation errors



class NoValidMovesAvailable(HTTPException):

    def  __init__ (self, game_state :List) -> JSONResponse:
        detail_message = f"Game state : {game_state} is has no valid moves to take"

        error_info =[
            ErrorDetail(
                field = "Game State",
                message = f"No valid moves in game  state : {game_state}",
                code= "NO_VALID_MOVES"
            )
        ]

        problem_content = ProblemDetails(
            type="docs/errors/no_valid_moves",
            title= "No valid moves to take",
            status = 422,
            detail_message = detail_message,
            errors= error_info ).model_dump(exclude_none=True)
        super().__init__(status_code=422, detail= problem_content)

        # return  JSONResponse(status_code  = status.HTTP_422_UNPROCESSABLE_ENTITY,
        #                     content = problem_content)