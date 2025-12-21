"""Тесты для модуля views."""
from unittest.mock import MagicMock, patch

from src.views import home_page


@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_home_page_success(mock_stocks: MagicMock, mock_currencies: MagicMock) -> None:
    """Тестирование успешного выполнения home_page."""
    # Настраиваем моки
    mock_currencies.return_value = [{"currency": "USD", "rate": 75.5}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}]

    result = home_page("2023-10-20 15:30:00")

    assert "greeting" in result
    assert result["greeting"] == "Добрый день"
    assert "cards" in result
    assert "currency_rates" in result
    assert "stock_prices" in result


def test_home_page_invalid_date() -> None:
    """Тестирование с неверным форматом даты."""
    result = home_page("неправильная дата")
    assert "error" in result
