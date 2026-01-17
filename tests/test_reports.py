"""Тесты для модуля reports."""
import json

import pandas as pd
import pytest
from pandas import DataFrame

from src.reports import spending_by_category


@pytest.fixture
def sample_dataframe() -> DataFrame:
    """Фикстура с тестовым DataFrame."""
    dates = pd.date_range(start="2023-07-01", end="2023-10-20", freq="D")
    data = {
        "Дата операции": dates,
        "Категория": ["Супермаркеты"] * len(dates),
        "Сумма операции": [-100.0] * len(dates),
    }
    return pd.DataFrame(data)


def test_spending_by_category(sample_dataframe: DataFrame) -> None:
    """Тестирование расчета трат по категории."""
    result = spending_by_category(sample_dataframe, "Супермаркеты", "2023-10-20")
    conv_json = json.loads(result)

    assert "category" in conv_json
    assert conv_json["category"] == "Супермаркеты"
    assert "total_spent" in conv_json
    assert conv_json["total_spent"] > 0


def test_spending_by_category_empty() -> None:
    """Тестирование с пустым DataFrame."""
    df = pd.DataFrame()
    result = spending_by_category(df, "Супермаркеты")
    assert "error" in result
