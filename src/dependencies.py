
from functools import lru_cache
from pathlib import Path
from src.load_q_values import load_q_values
from src.prediction_agent import PredictionAgent
from src.config_loader import Q_VALUES_PATH

@lru_cache(maxsize=1)
def get_prediction_agent() -> PredictionAgent:
    pkl_file_path = Path(Q_VALUES_PATH)
    q_values = load_q_values(pkl_file_path)
    return PredictionAgent(q_values)
