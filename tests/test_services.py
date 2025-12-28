"""Тесты для модуля services."""
from typing import Any, Dict, List

import pandas
import pytest
from pandas import Timestamp

from src.services import simple_search


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "Дата платежа": Timestamp("2019-09-09 19:41:14"),
            "Дата операции": Timestamp("2019-09-09 19:41:14"),
            "Описание": "Покупка в Лента",
            "Категория": "Супермаркеты",
            "Сумма операции": -1500.00,
        },
        {
            "Дата платежа": Timestamp("2019-09-09 19:41:14"),
            "Дата операции": Timestamp("2019-09-09 19:41:14"),
            "Описание": "Ресторан",
            "Категория": "Рестораны",
            "Сумма операции": -2500.00,
        },
        {
            "Дата платежа": Timestamp("2019-09-09 19:41:14"),
            "Дата операции": Timestamp("2019-09-09 19:41:14"),
            "Описание": "Перевод другу",
            "Категория": "Переводы",
            "Сумма операции": -1000.00,
        },
    ]


@pytest.mark.parametrize(
    "query,expected_count",
    [
        ("Лента", 202),
        ("лента", 202),  # Проверка регистронезависимости
        ("Ресторан", 192),
        ("Перевод", 196),
        ("", 0),
    ],
)
def test_simple_search(query: str, expected_count: int, sample_transactions: list) -> None:
    """Тестирование простого поиска."""
    df = pandas.DataFrame(sample_transactions)
    result = simple_search(query, df)
    assert len(result) == expected_count


def test_simple_search_empty_input(sample_transactions: list) -> None:
    """Тестирование поиска с пустым списком транзакций."""
    df = pandas.DataFrame(sample_transactions)
    result = simple_search("Лента", df)
    assert len(result) == 202
