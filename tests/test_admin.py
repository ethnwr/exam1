import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Module4_Admin.admin import add_product, change_order_status


def test_add_product():
    """TC-09: Проверка добавления товара"""
    ok, msg = add_product('cat_02', 'Git для профессионалов', 'Б. Штрауб', 1200, 5, 'Полное руководство')
    assert ok is True
    assert 'Git для профессионалов' in msg
    print(f"✅ TC-09 пройден: {msg}")


def test_change_order_status():
    """TC-10: Проверка изменения статуса заказа"""
    # Берём последний созданный заказ из TC-08
    from Module4_Admin.admin import load_orders
    orders = load_orders()
    assert len(orders) > 0
    order_id = orders[-1]['order_id']

    ok, msg = change_order_status(order_id, 'доставлен')
    assert ok is True
    assert 'доставлен' in msg.lower()
    print(f"✅ TC-10 пройден: {msg}")


if __name__ == '__main__':
    test_add_product()
    test_change_order_status()
    print("\n=== Все тесты админ-панели пройдены ===")