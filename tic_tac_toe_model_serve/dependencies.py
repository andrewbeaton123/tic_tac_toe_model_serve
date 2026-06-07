from functools import lru_cache
import mlflow.pyfunc
from mlflow.pyfunc import PyFuncModel
from tic_tac_toe_model_serve.settings import settings


@lru_cache(maxsize=1)
def get_model() -> PyFuncModel:
    return mlflow.pyfunc.load_model(settings.MLFLOW_MODEL_URI)
