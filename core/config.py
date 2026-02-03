import json
from pathlib import Path

CONFIG_PATH = Path("config.json")

if not CONFIG_PATH.exists():
    raise RuntimeError("❌ config.json no encontrado")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)


# ==========================
# ACCESORES CLAROS
# ==========================

LIBRARY_PATH = Path(CONFIG["library"]["base_path"])

SERIES_NAME = CONFIG["series"]["name"]
SEASON_NUMBER = CONFIG["series"]["season"]

RAR_PASSWORD = CONFIG["extractor"]["password"]

CONVERT_TO_MP4 = CONFIG["conversion"]["enabled"]
DELETE_MKV = CONFIG["conversion"]["delete_original_mkv"]

RENAMER_ENABLED = CONFIG["renamer"]["enabled"]
RENAMER_FORMAT = CONFIG["renamer"]["format"]
