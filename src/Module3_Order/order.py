import json
import os
import uuid
from datetime import datetime
from logger import logger

ORDERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'orders.json')


def load_orders():
    """Загрузить заказы из файла"""
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_orders(orders):
    """Сохранить заказы в файл"""
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


def validate_customer(data):
    """Валидация данных покупателя"""
    errors = []
    if not data.get('last_name', '').strip():
        errors.append("Фамилия обязательна")
    if not data.get('first_name', '').strip():
        errors.append("Имя обязательно")
    if not data.get('address', '').strip():
        errors.append("Адрес обязателен")
    if not data.get('phone', '').strip():
        errors.append("Телефон обязателен")
    email = data.get('email', '').strip()
    if not email or '@' not in email:
        errors.append("Некорректный email")
    return errors


def create_order(customer_data, cart_items, total):
    """Создать заказ"""
    errors = validate_customer(customer_data)
    if errors:
        return None, errors

    order = {
        'order_id': str(uuid.uuid4())[:8].upper(),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'новый',
        'customer': {
            'last_name': customer_data['last_name'],
            'first_name': customer_data['first_name'],
            'address': customer_data['address'],
            'phone': customer_data['phone'],
            'email': customer_data['email']
        },
        'items': [{'name': item['product']['name'], 'price': item['product']['price'], 'quantity': item['quantity']} for item in cart_items],
        'total': total
    }

    orders = load_orders()
    orders.append(order)
    save_orders(orders)

    logger.info(f"Заказ {order['order_id']} создан на сумму {total:.2f} руб.")
    return order, []