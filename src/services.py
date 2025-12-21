"""Сервисы для работы с транзакциями."""
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def simple_search(query: str, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Простой поиск по транзакциям."""
    try:
        if not query:
            return []

        results = []
        query_lower = query.lower()

        for transaction in transactions:
            # Ищем в описании и категории
            description = str(transaction.get("Описание", "")).lower()
            category = str(transaction.get("Категория", "")).lower()

            if query_lower in description or query_lower in category:
                results.append(transaction)

        logger.info(f"Поиск '{query}' вернул {len(results)} результатов")
        return results

    except Exception as e:
        logger.error(f"Ошибка в simple_search: {e}")
        return []
