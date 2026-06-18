import json
import os
from logger import logger

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')


def load_products():
    """Загрузка товаров из JSON-файла"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info("Каталог загружен")
        return data
    except FileNotFoundError:
        logger.error(f"Файл {DATA_FILE} не найден")
        return {"storeName": "BookShop", "categories": []}
    except json.JSONDecodeError:
        logger.error("Ошибка чтения JSON")
        return {"storeName": "BookShop", "categories": []}


def get_all_products(data):
    """Получить все товары плоским списком"""
    products = []
    for cat in data['categories']:
        for p in cat['products']:
            p['category'] = cat['name']
            p['category_id'] = cat['id']
            products.append(p)
    return products


def search_by_name(data, query):
    """Поиск по названию или автору"""
    query = query.lower()
    results = []
    for cat in data['categories']:
        for p in cat['products']:
            if query in p['name'].lower() or query in p.get('author', '').lower():
                p_copy = p.copy()
                p_copy['category'] = cat['name']
                results.append(p_copy)
    return results


def filter_by_category(data, category_id):
    """Фильтрация по категории"""
    for cat in data['categories']:
        if cat['id'] == category_id:
            return cat['products']
    return []


def filter_by_price(products, min_price=0, max_price=float('inf')):
    """Фильтрация по цене"""
    return [p for p in products if min_price <= p['price'] <= max_price]


def find_product(data, product_id):
    """Найти товар по ID"""
    for cat in data['categories']:
        for p in cat['products']:
            if p['id'] == product_id:
                return p
    return None