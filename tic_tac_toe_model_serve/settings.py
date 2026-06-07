from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    API_KEY: str = Field(default = ..., description="API key for authentication")
    MLFLOW_MODEL_URI: str = Field(default=..., description="MLflow model URI (e.g. models:/tictactoe-agent/1 or local path)")
    ALLOWED_PLAYERS: List[int] = Field(default_factory= lambda: [1,2], description="List of allowed player IDs")
    MIN_PLAYERS: int = Field(default=2, description="Minimum number of players allowed")
    MAX_PLAYERS: int = Field(default =2, description="Maximum number of players allowed")
    DISPLAY_NAME: str = Field(default = "Tic Tac Toe", description="Display name for the game")

settings = Settings()
