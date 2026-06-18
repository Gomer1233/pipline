"""Конфигурация проекта (пути, параметры и т.д.)"""
import os
from pathlib import Path

# Базовый путь проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Пути к данным
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

# Пути к другим ресурсам
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
SRC_DIR = BASE_DIR / "src"
LOGS_DIR = BASE_DIR / "logs"

# Создание директорий (если нет)
for d in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Параметры по умолчанию
DEFAULT_PARAMS = {
    "debug": False,
    "log_level": "INFO",
    "seed": 42,
    "test_size": 0.2,
    "n_jobs": -1,
}

# Пример: загрузка из .env (опционально)
# from dotenv import load_dotenv
# load_dotenv()