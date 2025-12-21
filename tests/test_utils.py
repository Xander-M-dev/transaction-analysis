"""Тесты для модуля utils."""
import json
from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.utils import get_currency_rates, get_greeting_by_time, get_stock_prices, load_user_settings, read_excel_file


# Тесты для get_greeting_by_time
@pytest.mark.parametrize(
    "hour,expected",
    [
        (5, "Доброе утро"),
        (11, "Доброе утро"),
        (12, "Добрый день"),
        (17, "Добрый день"),
        (18, "Добрый вечер"),
        (22, "Добрый вечер"),
        (23, "Доброй ночи"),
        (0, "Доброй ночи"),
        (4, "Доброй ночи"),
    ],
)
def test_get_greeting_by_time(hour: int, expected: str) -> None:
    """Тестирование определения приветствия по времени."""
    test_time = datetime(2023, 1, 1, hour, 0, 0)
    result = get_greeting_by_time(test_time)
    assert result == expected


def test_get_greeting_by_time_invalid() -> None:
    """Тестирование с некорректным временем."""
    with pytest.raises(AttributeError):
        get_greeting_by_time("not a datetime")


# Тесты для load_user_settings
def test_load_user_settings_success() -> None:
    """Тест успешной загрузки настроек."""
    mock_data = '{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL"]}'

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_user_settings()

    assert result == {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL"]}


def test_load_user_settings_file_not_found() -> None:
    """Тест обработки отсутствующего файла."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_user_settings()

    assert result == {"user_currencies": [], "user_stocks": []}


def test_load_user_settings_json_decode_error() -> None:
    """Тест обработки некорректного JSON."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = load_user_settings()

    assert result == {"user_currencies": [], "user_stocks": []}


# Тесты для read_excel_file
@patch("pandas.read_excel")
def test_read_excel_file_success(mock_read_excel: MagicMock) -> None:
    """Тест успешного чтения Excel файла."""
    mock_df = pd.DataFrame(
        {
            "Дата операции": ["2023-01-01", "2023-01-02"],
            "Дата платежа": ["2023-01-02", "2023-01-03"],
            "Сумма операции": [100, 200],
        }
    )
    mock_read_excel.return_value = mock_df

    result = read_excel_file("test.xlsx")

    assert len(result) == 2
    assert "Дата операции" in result.columns


@patch("pandas.read_excel")
def test_read_excel_file_exception(mock_read_excel: MagicMock) -> None:
    """Тест обработки исключения при чтении файла."""
    mock_read_excel.side_effect = Exception("File not found")

    result = read_excel_file("nonexistent.xlsx")

    assert result.empty


# Тесты для get_currency_rates
@patch("requests.get")
@patch("src.utils.API_KEY", "test_key")
def test_get_currency_rates_success(mock_get: MagicMock) -> None:
    """Тест успешного получения курсов валют."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rates": {
            "USD": 75.5,
            "EUR": 85.3,
        }
    }
    mock_get.return_value = mock_response

    result = get_currency_rates(["USD", "EUR"])

    assert len(result) == 2
    assert result[0]["currency"] == "USD"
    assert result[0]["rate"] == 75.5
    assert result[1]["currency"] == "EUR"
    assert result[1]["rate"] == 85.3


@patch("requests.get")
def test_get_currency_rates_api_key_missing(mock_get: MagicMock) -> None:
    """Тест поведения при отсутствии API ключа."""
    with patch("src.utils.API_KEY", None):
        result = get_currency_rates(["USD", "EUR"])

    assert result == []
    mock_get.assert_not_called()


@patch("requests.get")
@patch("src.utils.API_KEY", "test_key")
def test_get_currency_rates_request_exception(mock_get: MagicMock) -> None:
    """Тест обработки исключения при запросе."""
    mock_get.side_effect = Exception("Network error")

    result = get_currency_rates(["USD"])

    assert result == []


# Тесты для get_stock_prices
@patch("requests.get")
@patch("src.utils.API_KEY", "test_key")
def test_get_stock_prices_success(mock_get: MagicMock) -> None:
    """Тест успешного получения цен акций."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"close": 150.25}
    mock_get.return_value = mock_response

    result = get_stock_prices(["AAPL"])

    assert len(result) == 1
    assert result[0]["stock"] == "AAPL"
    assert result[0]["price"] == 150.25


@patch("requests.get")
@patch("src.utils.API_KEY", "test_key")
def test_get_stock_prices_no_close_price(mock_get: MagicMock) -> None:
    """Тест обработки ответа без поля close."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    result = get_stock_prices(["AAPL"])

    assert result == []


@patch("requests.get")
def test_get_stock_prices_api_key_missing(mock_get: MagicMock) -> None:
    """Тест поведения при отсутствии API ключа."""
    with patch("src.utils.API_KEY", None):
        result = get_stock_prices(["AAPL"])

    assert result == []
    mock_get.assert_not_called()


@patch("requests.get")
@patch("src.utils.API_KEY", "test_key")
def test_get_stock_prices_request_exception(mock_get: MagicMock) -> None:
    """Тест обработки исключения при запросе."""
    mock_get.side_effect = Exception("Network error")

    result = get_stock_prices(["AAPL"])

    assert result == []
