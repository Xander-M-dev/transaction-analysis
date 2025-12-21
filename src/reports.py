"""Функции для генерации отчетов."""
import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def report_decorator(func: Callable | None = None, *, filename: str | None = None) -> Callable:
    """Декоратор для сохранения результатов отчета в файл."""

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            result = f(*args, **kwargs)

            # Определяем имя файла
            if filename:
                file_name = filename
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{f.__name__}_{timestamp}.json"

            # Сохраняем результат в файл
            try:
                with open(f"reports/{file_name}", "w", encoding="utf-8") as file:
                    json.dump(result, file, ensure_ascii=False, indent=2)
                logger.info(f"Отчет сохранен в reports/{file_name}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {e}")

            return result

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


@report_decorator
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict[str, Any]:
    """Рассчитывает траты по категории за последние три месяца."""
    try:
        # Определяем дату отсчета
        if date is None:
            target_date = datetime.now()
        else:
            target_date = datetime.strptime(date, "%Y-%m-%d")

        # Вычисляем дату начала периода (3 месяца назад)
        start_date = target_date - timedelta(days=90)

        # Фильтруем транзакции
        if "Дата операции" not in transactions.columns:
            return {"error": "В данных отсутствует колонка 'Дата операции'"}

        # Преобразуем даты если нужно
        if not pd.api.types.is_datetime64_any_dtype(transactions["Дата операции"]):
            transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")

        # Фильтруем по дате и категории
        mask = (
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= target_date)
            & (transactions["Категория"] == category)
        )

        filtered = transactions[mask]

        if filtered.empty:
            return {
                "category": category,
                "period": f"{start_date.strftime('%Y-%m-%d')} - {target_date.strftime('%Y-%m-%d')}",
                "total_spent": 0,
                "transactions_count": 0,
                "message": "Транзакции не найдены",
            }

        # Суммируем траты (отрицательные суммы)
        total_spent = filtered[filtered["Сумма операции"] < 0]["Сумма операции"].abs().sum()

        return {
            "category": category,
            "period": f"{start_date.strftime('%Y-%m-%d')} - {target_date.strftime('%Y-%m-%d')}",
            "total_spent": round(total_spent, 2),
            "transactions_count": len(filtered),
            "average_spent": round(total_spent / len(filtered), 2) if len(filtered) > 0 else 0,
        }

    except Exception as e:
        logger.error(f"Ошибка в spending_by_category: {e}")
        return {"error": f"Ошибка обработки: {str(e)}"}
