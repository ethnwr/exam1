import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Module1_Catalog.catalog import load_products, find_product
from Module2_Cart.cart import Cart
from Module3_Order.order import create_order
from Module4_Admin.admin import edit_product


def test_catalog_to_cart():
    """IT-01: Передача данных из каталога в корзину"""
    data = load_products()
    product = find_product(data, 'pr_005')  # Высшая математика

    cart = Cart()
    cart.add(product, 2)

    items = cart.get_items()
    assert items[0]['product']['name'] == product['name']
    assert items[0]['product']['price'] == product['price']
    assert items[0]['quantity'] == 2
    assert cart.get_total() == product['price'] * 2
    print("✅ IT-01 пройден: каталог → корзина")


def test_cart_to_order():
    """IT-02: Передача данных из корзины в заказ"""
    cart = Cart()
    cart.add({'id': 'pr_007', 'name': 'Сказки', 'price': 320.00}, 1)

    customer = {
        'last_name': 'Петров',
        'first_name': 'Пётр',
        'address': 'ул. Ленина, 1',
        'phone': '+79998887766',
        'email': 'petrov@mail.ru'
    }
    order, errors = create_order(customer, cart.get_items(), cart.get_total())

    assert order is not None
    assert order['items'][0]['name'] == 'Сказки'
    assert order['items'][0]['price'] == 320.00
    assert order['items'][0]['quantity'] == 1
    assert order['total'] == 320.00
    print(f"✅ IT-02 пройден: корзина → заказ {order['order_id']}")


def test_admin_to_catalog():
    """IT-03: Обновление каталога через админ-панель"""
    # Меняем цену
    ok, msg = edit_product('pr_001', {'price': 500.00})
    assert ok is True

    # Проверяем, что в каталоге цена обновилась
    data = load_products()
    product = find_product(data, 'pr_001')
    assert product['price'] == 500.00
    print(f"✅ IT-03 пройден: админ → каталог, цена обновлена до {product['price']}")


if __name__ == '__main__':
    test_catalog_to_cart()
    test_cart_to_order()
    test_admin_to_catalog()
    print("\n=== Все интеграционные тесты пройдены ===")