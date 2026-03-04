from pathlib import Path
import pickle as pkl 
from loguru import logger
import pandas as pd 
from typing import Dict
def load_q_values(pkl_file_path:Path) -> Dict:

    try:
            with open(pkl_file_path, 'rb') as f:
                q_values  = pkl.load(f)
            logger.info("Successfully loaded .pkl file from artifact.")
            return(q_values)

    except FileNotFoundError:
        print(f"Error: The .pkl file '{pkl_file_path}' was not found in the artifacts.")
        exit(1)

    except Exception as e:
        print(f"Error loading .pkl file: {e}")
        exit(1)
    
