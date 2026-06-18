import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Module1_Catalog.catalog import load_products, search_by_name, filter_by_category


def test_load_products():
    """TC-01: Проверка загрузки данных из JSON"""
    data = load_products()
    assert data['storeName'] == 'BookShop'
    assert len(data['categories']) == 4
    assert len(data['categories'][0]['products']) >= 1
    print("✅ TC-01 пройден: данные загружены")


def test_search_by_name():
    """TC-02: Проверка поиска по названию"""
    data = load_products()
    results = search_by_name(data, 'код')
    assert len(results) >= 1
    assert any('Чистый код' in r['name'] for r in results)
    print("✅ TC-02 пройден: поиск работает")


def test_filter_by_category():
    """TC-03: Проверка фильтрации по категории"""
    data = load_products()
    results = filter_by_category(data, 'cat_04')  # Детская литература
    assert len(results) == 2
    names = [r['name'] for r in results]
    assert 'Сказки' in names
    assert 'Незнайка на Луне' in names
    print("✅ TC-03 пройден: фильтрация работает")


if __name__ == '__main__':
    test_load_products()
    test_search_by_name()
    test_filter_by_category()
    print("\n=== Все тесты каталога пройдены ===")