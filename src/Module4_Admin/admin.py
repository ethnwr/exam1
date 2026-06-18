import json
import os
from logger import logger

PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')
ORDERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'orders.json')

def load_products_data():
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_products_data(data):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_orders():
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


def get_all_orders():
    """Получить все заказы"""
    return load_orders()


def change_order_status(order_id, new_status):
    """Изменить статус заказа"""
    valid_statuses = ['новый', 'в обработке', 'доставлен', 'отменен']
    if new_status not in valid_statuses:
        return False, f"Недопустимый статус. Допустимые: {', '.join(valid_statuses)}"

    orders = load_orders()
    for order in orders:
        if order['order_id'] == order_id:
            old = order['status']
            order['status'] = new_status
            save_orders(orders)
            logger.info(f"Заказ {order_id}: статус {old} -> {new_status}")
            return True, f"Статус изменен: {old} -> {new_status}"
    return False, "Заказ не найден"


def add_product(category_id, name, author, price, stock, description):
    """Добавить новый товар"""
    data = load_products_data()
    for cat in data['categories']:
        if cat['id'] == category_id:
            new_id = f"pr_{len(cat['products']) + 1:03d}"
            cat['products'].append({
                'id': new_id,
                'name': name,
                'author': author,
                'price': float(price),
                'stock': int(stock),
                'description': description
            })
            save_products_data(data)
            logger.info(f"Добавлен товар: {name}")
            return True, f"Товар '{name}' добавлен (ID: {new_id})"
    return False, "Категория не найдена"


def edit_product(product_id, updates):
    """Редактировать товар"""
    data = load_products_data()
    for cat in data['categories']:
        for p in cat['products']:
            if p['id'] == product_id:
                for key, value in updates.items():
                    if key in p:
                        p[key] = value
                save_products_data(data)
                logger.info(f"Товар {product_id} обновлен")
                return True, f"Товар '{p['name']}' обновлен"
    return False, "Товар не найден"


def delete_product(product_id):
    """Удалить товар"""
    data = load_products_data()
    for cat in data['categories']:
        for i, p in enumerate(cat['products']):
            if p['id'] == product_id:
                name = p['name']
                cat['products'].pop(i)
                save_products_data(data)
                logger.info(f"Товар удален: {name}")
                return True, f"Товар '{name}' удален"
    return False, "Товар не найден"