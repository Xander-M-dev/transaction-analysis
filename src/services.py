"""Сервисы для работы с транзакциями."""
import json
import logging

import pandas

logger = logging.getLogger(__name__)


def simple_search(query: str, df: pandas.DataFrame) -> str:
    """Простой поиск по транзакциям."""
    try:
        df["Дата платежа"] = df["Дата платежа"].dt.strftime("%d.%m.%Y")
        df["Дата операции"] = df["Дата операции"].dt.strftime("%d.%m.%Y")
        if not query:
            return ""

        results = []
        query_lower = query.lower()

        transactions = df.to_dict("records")
        for transaction in transactions:
            # Ищем в описании и категории
            description = str(transaction.get("Описание", "")).lower()
            category = str(transaction.get("Категория", "")).lower()

            if query_lower in description or query_lower in category:
                results.append(transaction)

        logger.info(f"Поиск '{query}' вернул {len(results)} результатов")
        return json.dumps(results, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка в simple_search: {e}")
        return ""
