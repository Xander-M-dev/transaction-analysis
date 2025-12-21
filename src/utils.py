"""Вспомогательные функции для работы с данными."""
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


def load_user_settings() -> Any:
    """Загружает пользовательские настройки из файла user_settings.json."""
    try:
        with open("user_settings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Файл user_settings.json не найден")
        return {"user_currencies": [], "user_stocks": []}
    except json.JSONDecodeError:
        logger.error("Ошибка при чтении user_settings.json")
        return {"user_currencies": [], "user_stocks": []}


def read_excel_file(file_path: str) -> pd.DataFrame:
    """Читает Excel файл с транзакциями."""
    try:
        df = pd.read_excel(file_path)

        # Преобразуем даты
        date_columns = ["Дата операции", "Дата платежа"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

        logger.info(f"Успешно загружен файл {file_path}, строк: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return pd.DataFrame()


def get_greeting_by_time(time: datetime | str) -> str:
    """Определяет приветствие в зависимости от времени суток."""
    if isinstance(time, str):
        raise AttributeError
    hour = time.hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """
    Получает курсы валют через API.

    Args:
        currencies: Список валют для получения курса

    Returns:
        Список словарей с курсами валют
    """
    if not API_KEY:
        logger.error("API_KEY не установлен")
        return []

    try:
        url = "https://api.apilayer.com/exchangerates_data/latest"
        headers = {"apikey": API_KEY}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        rates = data.get("rates", {})

        result = []
        for currency in currencies:
            if currency in rates:
                result.append({"currency": currency, "rate": round(rates[currency], 2)})

        logger.info(f"Получены курсы для {len(result)} валют")
        return result
    except Exception as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")
        return []


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """
    Получает цены акций через API.

    Args:
        stocks: Список тикеров акций

    Returns:
        Список словарей с ценами акций
    """
    if not API_KEY:
        logger.error("API_KEY не установлен")
        return []

    result = []

    for stock in stocks:
        try:
            url = f"https://api.apilayer.com/stock_data/quote?symbol={stock}"
            headers = {"apikey": API_KEY}

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            price = data.get("close")

            if price:
                result.append({"stock": stock, "price": round(float(price), 2)})

        except Exception as e:
            logger.error(f"Ошибка при получении цены акции {stock}: {e}")

    logger.info(f"Получены цены для {len(result)} акций")
    return result
