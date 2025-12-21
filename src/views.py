"""Функции для генерации JSON-ответов для веб-страниц."""
import logging
from datetime import datetime

from src.utils import get_currency_rates, get_greeting_by_time, get_stock_prices, load_user_settings

logger = logging.getLogger(__name__)


def home_page(date_time_str: str) -> dict:
    """Генерирует JSON-ответ для главной страницы."""
    try:
        # Преобразуем строку в datetime
        target_datetime = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        # Определяем приветствие
        greeting = get_greeting_by_time(target_datetime)

        # Загружаем настройки пользователя
        settings = load_user_settings()

        # Получаем курсы валют и цены акций
        currency_rates = get_currency_rates(settings.get("user_currencies", []))
        stock_prices = get_stock_prices(settings.get("user_stocks", []))

        # Заглушки для остальных данных
        cards = [
            {"last_digits": "5814", "total_spent": 1262.00, "cashback": 12.62},
            {"last_digits": "7512", "total_spent": 7.94, "cashback": 0.08},
        ]

        top_transactions = [
            {
                "date": "21.12.2021",
                "amount": 1198.23,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {"date": "20.12.2021", "amount": 829.00, "category": "Супермаркеты", "description": "Лента"},
        ]

        return {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_transactions[:5],
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }

    except ValueError as e:
        logger.error(f"Неверный формат даты: {e}")
        return {"error": "Неверный формат даты"}
    except Exception as e:
        logger.error(f"Ошибка в home_page: {e}")
        return {"error": "Внутренняя ошибка сервера"}
