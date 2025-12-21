"""Тесты для модуля services."""
from typing import Any, Dict, List

import pytest

from src.services import simple_search


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {"Описание": "Покупка в Лента", "Категория": "Супермаркеты", "Сумма операции": -1500.00},
        {"Описание": "Ресторан", "Категория": "Рестораны", "Сумма операции": -2500.00},
        {"Описание": "Перевод другу", "Категория": "Переводы", "Сумма операции": -1000.00},
    ]


@pytest.mark.parametrize(
    "query,expected_count",
    [
        ("Лента", 1),
        ("лента", 1),  # Проверка регистронезависимости
        ("Ресторан", 1),
        ("Перевод", 1),
        ("Несуществующий", 0),
        ("", 0),
    ],
)
def test_simple_search(query: str, expected_count: int, sample_transactions: list) -> None:
    """Тестирование простого поиска."""
    result = simple_search(query, sample_transactions)
    assert len(result) == expected_count


def test_simple_search_empty_input() -> None:
    """Тестирование поиска с пустым списком транзакций."""
    result = simple_search("Лента", [])
    assert len(result) == 0
    assert isinstance(result, list)
