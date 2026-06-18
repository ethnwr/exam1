import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Module3_Order.order import create_order


def test_validation():
    """TC-07: Проверка валидации данных"""
    customer = {
        'last_name': '',
        'first_name': 'Иван',
        'address': 'ул. Мира, 5',
        'phone': '+79991234567',
        'email': 'неправильный'
    }
    order, errors = create_order(customer, [], 0)
    assert order is None
    assert len(errors) >= 2
    assert any('Фамилия обязательна' in e for e in errors)
    assert any('email' in e.lower() for e in errors)
    print("✅ TC-07 пройден: валидация работает")


def test_save_order():
    """TC-08: Проверка сохранения заказа"""
    customer = {
        'last_name': 'Иванов',
        'first_name': 'Иван',
        'address': 'ул. Мира, 5',
        'phone': '+79991234567',
        'email': 'ivan@mail.ru'
    }
    cart_items = [{'product': {'name': 'Чистый код', 'price': 890.00}, 'quantity': 1}]
    order, errors = create_order(customer, cart_items, 890.00)
    assert order is not None
    assert len(errors) == 0
    assert order['status'] == 'новый'
    assert order['total'] == 890.00
    assert len(order['order_id']) == 8
    assert order['customer']['last_name'] == 'Иванов'
    print(f"✅ TC-08 пройден: заказ {order['order_id']} сохранён")


if __name__ == '__main__':
    test_validation()
    test_save_order()
    print("\n=== Все тесты заказов пройдены ===")