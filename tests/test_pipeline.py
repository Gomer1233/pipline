"""Тесты для модулей пайплайна"""
import pytest
import pandas as pd
from pathlib import Path

# Относительный импорт для тестов в подпапке src/tests
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline import clean_data, transform_data

# Тестовые данные
SAMPLE_DF = pd.DataFrame({
    "A": [1, 2, 2, 3],
    "B": ["x", "y", "y", "z"],
    "C": [10, 20, 20, 30]
})

def test_clean_data_removes_duplicates():
    cleaned = clean_data(SAMPLE_DF.copy())
    assert len(cleaned) == 3  # удаляется один дубликат

def test_clean_data_preserves_columns():
    cleaned = clean_data(SAMPLE_DF.copy())
    assert list(cleaned.columns) == ["A", "B", "C"]

# TODO: Добавьте тесты для transform_data, load_data и т.д.