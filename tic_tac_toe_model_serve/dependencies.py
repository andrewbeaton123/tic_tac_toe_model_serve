from functools import lru_cache
from pathlib import Path
from tic_tac_toe_model_serve.load_q_values import load_q_values
from tic_tac_toe_model_serve.prediction_agent import PredictionAgent
from tic_tac_toe_model_serve.settings import settings

@lru_cache(maxsize=1)
def get_prediction_agent() -> PredictionAgent:
    pkl_file_path = Path(settings.Q_VALUES_PATH)
    q_values = load_q_values(pkl_file_path)
    return PredictionAgent(q_values)
