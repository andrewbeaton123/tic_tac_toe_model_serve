from pathlib import Path
import yaml

CONFIG_FILE = Path("config.yml")
if not CONFIG_FILE.exists():
    raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")

with open(CONFIG_FILE, 'r') as f:
    config = yaml.safe_load(f)

TIC_TAC_TOE_CONFIG = config.get("games", {}).get("tic_tac_toe", {})
ALLOWED_PLAYERS = TIC_TAC_TOE_CONFIG.get("allowed_players", [1, 2])
