"""Утилиты для пайплайна (логирование, валидация и т.д.)"""
import logging
import os
from datetime import datetime
from src.config import LOGS_DIR

def setup_logging():
    """Настройка логирования в файл и консоль"""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def validate_data(df, required_columns=None, non_null_columns=None):
    """
    Валидация DataFrame.
    
    Параметры:
    - required_columns: список обязательных колонок
    - non_null_columns: список колонок, где не должно быть пропусков
    """
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Отсутствуют обязательные колонки: {missing}")
    
    if non_null_columns:
        for col in non_null_columns:
            if df[col].isna().any():
                raise ValueError(f"В колонке '{col}' есть пропуски!")
    
    return True