import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Module2_Cart.cart import Cart


def test_add_to_cart():
    """TC-04: Проверка добавления товара в корзину"""
    cart = Cart()
    product = {'id': 'pr_001', 'name': 'Мастер и Маргарита', 'price': 450.00}
    cart.add(product, 2)
    items = cart.get_items()
    assert len(items) == 1
    assert items[0]['product']['name'] == 'Мастер и Маргарита'
    assert items[0]['quantity'] == 2
    assert cart.get_total() == 900.00
    print("✅ TC-04 пройден: добавление работает")


def test_remove_from_cart():
    """TC-05: Проверка удаления товара из корзины"""
    cart = Cart()
    product = {'id': 'pr_001', 'name': 'Мастер и Маргарита', 'price': 450.00}
    cart.add(product, 1)
    cart.remove('pr_001')
    assert len(cart.get_items()) == 0
    assert cart.get_total() == 0
    print("✅ TC-05 пройден: удаление работает")


def test_update_quantity():
    """TC-06: Проверка изменения количества"""
    cart = Cart()
    product = {'id': 'pr_002', 'name': '1984', 'price': 380.00}
    cart.add(product, 1)
    cart.update_quantity('pr_002', 3)
    items = cart.get_items()
    assert items[0]['quantity'] == 3
    assert cart.get_total() == 1140.00
    print("✅ TC-06 пройден: изменение количества работает")


if __name__ == '__main__':
    test_add_to_cart()
    test_remove_from_cart()
    test_update_quantity()
    print("\n=== Все тесты корзины пройдены ===")