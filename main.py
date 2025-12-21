"""Главный модуль приложения."""
import json
import logging

from src.reports import spending_by_category
from src.services import simple_search
from src.utils import read_excel_file
from src.views import home_page

logger = logging.getLogger(__name__)


def main() -> None:
    """Основная функция приложения."""
    print("=" * 50)
    print("Приложение для анализа транзакций")
    print("=" * 50)

    try:
        # 1. Загружаем транзакции из Excel
        print("\n1. Загрузка транзакций...")
        df = read_excel_file("data/operations.xlsx")

        print(f"Загружено {len(df)} транзакций")

        # 2. Главная страница
        print("\n2. Генерация главной страницы...")
        home_data = home_page("2023-10-20 15:30:00")
        print(json.dumps(home_data, ensure_ascii=False, indent=2))

        # 3. Простой поиск
        print("\n3. Простой поиск...")
        transactions_list = df.to_dict("records")
        search_results = simple_search("Лента", transactions_list)
        print(f"Найдено {len(search_results)} транзакций:")
        for result in search_results:
            print(f"  - {result.get('Описание')}: {result.get('Сумма операции')} руб.")

        # 4. Отчет по тратам по категории
        print("\n4. Генерация отчета по тратам...")
        if not df.empty:
            report = spending_by_category(df, "Супермаркеты", "2023-10-20")
            print(json.dumps(report, ensure_ascii=False, indent=2))

        print("\n" + "=" * 50)
        print("Выполнение завершено!")
        print("=" * 50)

    except Exception as e:
        logger.error(f"Ошибка в main: {e}")
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
