"""Основной модуль пайплайна обработки данных"""
import logging
import argparse
from pathlib import Path

import pandas as pd
from src.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    DEFAULT_PARAMS,
    LOGS_DIR,
)
from src.utils import setup_logging

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)


def load_data(filepath: Path) -> pd.DataFrame:
    """Загрузка данных из CSV/Excel/JSON"""
    if not filepath.exists():
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    ext = filepath.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(filepath)
    elif ext in [".xlsx", ".xls"]:
        return pd.read_excel(filepath)
    elif ext == ".json":
        return pd.read_json(filepath)
    else:
        raise ValueError(f"Неподдерживаемый формат: {ext}")


def save_data(df: pd.DataFrame, filepath: Path):
    """Сохранение данных в CSV/Excel"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    ext = filepath.suffix.lower()
    if ext == ".csv":
        df.to_csv(filepath, index=False)
    elif ext == ".parquet":
        df.to_parquet(filepath, index=False)
    elif ext in [".xlsx", ".xls"]:
        df.to_excel(filepath, index=False)
    else:
        raise ValueError(f"Неподдерживаемый формат сохранения: {ext}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Очистка данных (дубликаты, пропуски, типы)"""
    logger.info("Очистка данных...")
    
    # Пример логики (настройте под вашу задачу)
    df = df.drop_duplicates()
    
    # Пример удаления строк с пропусками
    # df = df.dropna()
    
    # Пример заполнения пропусков
    # df = df.fillna(method='ffill')
    
    logger.info(f"Очищено строк: {len(df)}")
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Преобразование признаков"""
    logger.info("Преобразование данных...")
    
    # Пример: нормализация числовых столбцов
    numeric_cols = df.select_dtypes(include=["number"]).columns
    # df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
    
    # Пример: кодирование категорий
    # from sklearn.preprocessing import LabelEncoder
    # for col in df.select_dtypes(include=["object"]).columns:
    #     le = LabelEncoder()
    #     df[col] = le.fit_transform(df[col].astype(str))
    
    return df


def run_pipeline(raw_file: str = "sample.csv", output_file: str = "processed_data.csv"):
    """Запуск пайплайна: загрузка -> очистка -> преобразование -> сохранение"""
    logger.info("=== ЗАПУСК ПАЙПЛАЙНА ===")
    
    raw_path = RAW_DATA_DIR / raw_file
    output_path = PROCESSED_DATA_DIR / output_file
    
    try:
        # 1. Загрузка
        df = load_data(raw_path)
        logger.info(f"Загружено строк: {len(df)}, признаков: {len(df.columns)}")
        
        # 2. Очистка
        df_clean = clean_data(df)
        
        # 3. Преобразование
        df_transformed = transform_data(df_clean)
        
        # 4. Сохранение
        save_data(df_transformed, output_path)
        logger.info(f"Результат сохранён: {output_path}")
        
        logger.info("=== ПАЙПЛАЙН ЗАВЕРШЁН ===")
        return df_transformed
    
    except Exception as e:
        logger.error(f"Ошибка пайплайна: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DS Pipeline")
    parser.add_argument("--input", "-i", default="sample.csv", help="Входной CSV-файл в data/raw/")
    parser.add_argument("--output", "-o", default="processed_data.csv", help="Имя выходного файла в data/processed/")
    
    args = parser.parse_args()
    run_pipeline(raw_file=args.input, output_file=args.output)