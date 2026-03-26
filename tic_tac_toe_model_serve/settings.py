from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    API_KEY: str = Field(default = ..., description="API key for authentication")
    Q_VALUES_PATH: str = Field("saved_q_values.pkl", description="Path to the saved Q-values file")
    ALLOWED_PLAYERS: List[int] = Field([1, 2], description="List of allowed player IDs")
    MIN_PLAYERS: int = Field(2, description="Minimum number of players allowed")
    MAX_PLAYERS: int = Field(2, description="Maximum number of players allowed")
    DISPLAY_NAME: str = Field("Tic Tac Toe", description="Display name for the game")

settings = Settings()
