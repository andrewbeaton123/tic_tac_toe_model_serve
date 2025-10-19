from loguru import logger
from src.logging_intercept import setup_logging

logger.add("logs/app.log", rotation="10 MB", serialize=True, level="INFO")

setup_logging()