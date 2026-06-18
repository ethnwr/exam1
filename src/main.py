from Module1_Catalog.catalog import load_products, get_all_products, search_by_name, filter_by_category, filter_by_price, find_product
from Module2_Cart.cart import Cart
from Module3_Order.order import create_order
from Module4_Admin.admin import get_all_orders, change_order_status, add_product, edit_product, delete_product
from logger import logger

def show_catalog(data):
    """Показать каталог"""
    products = get_all_products(data)
    print(f"\n{'='*60}")
    print(f"КАТАЛОГ КНИГ ({data['storeName']})")
    print(f"{'='*60}")
    for p in products:
        print(f"  [{p['id']}] {p['name']} — {p.get('author', '')} | {p['price']:.2f} руб. | ({p['category']})")


def show_cart(cart):
    """Показать корзину"""
    items = cart.get_items()
    if not items:
        print("\nКорзина пуста")
        return
    print(f"\n{'='*40}")
    print("КОРЗИНА")
    print(f"{'='*40}")
    for item in items:
        p = item['product']
        print(f"  {p['name']} x{item['quantity']} = {p['price']*item['quantity']:.2f} руб.")
    print(f"  Итого: {cart.get_total():.2f} руб.")


def customer_menu(cart, data):
    """Меню покупателя"""
    while True:
        print(f"\n{'─'*40}")
        print("МЕНЮ ПОКУПАТЕЛЯ:")
        print("  1. Показать каталог")
        print("  2. Поиск книг")
        print("  3. Фильтр по категории")
        print("  4. Фильтр по цене")
        print("  5. Добавить в корзину")
        print("  6. Показать корзину")
        print("  7. Изменить количество")
        print("  8. Удалить из корзины")
        print("  9. Оформить заказ")
        print("  0. Назад")
        choice = input("Выберите действие: ").strip()

        try:
            if choice == '1':
                show_catalog(data)

            elif choice == '2':
                q = input("Поиск по названию/автору: ")
                results = search_by_name(data, q)
                if results:
                    for p in results:
                        print(f"  [{p['id']}] {p['name']} — {p.get('author', '')} | {p['price']:.2f} руб.")
                else:
                    print("Ничего не найдено")

            elif choice == '3':
                print("\nКатегории: 1-Худ.лит, 2-Тех.лит, 3-Учеб.лит, 4-Дет.лит")
                cat_map = {'1': 'cat_01', '2': 'cat_02', '3': 'cat_03', '4': 'cat_04'}
                c = input("Номер категории: ").strip()
                if c in cat_map:
                    products = filter_by_category(data, cat_map[c])
                    for p in products:
                        print(f"  [{p['id']}] {p['name']} — {p['price']:.2f} руб.")
                else:
                    print("Неверный номер")

            elif choice == '4':
                try:
                    mn = float(input("Мин. цена (Enter=0): ") or 0)
                    mx = float(input("Макс. цена (Enter=999999): ") or 999999)
                    products = filter_by_price(get_all_products(data), mn, mx)
                    for p in products:
                        print(f"  [{p['id']}] {p['name']} — {p['price']:.2f} руб.")
                except ValueError:
                    print("Ошибка: введите число")

            elif choice == '5':
                pid = input("ID товара: ").strip()
                product = find_product(data, pid)
                if product:
                    try:
                        qty = int(input("Количество: ") or 1)
                        cart.add(product, qty)
                        print(f"Добавлено: {product['name']} x{qty}")
                    except ValueError:
                        print("Ошибка: введите число")
                else:
                    print("Товар не найден")

            elif choice == '6':
                show_cart(cart)

            elif choice == '7':
                show_cart(cart)
                pid = input("ID товара: ").strip()
                try:
                    qty = int(input("Новое количество: "))
                    cart.update_quantity(pid, qty)
                    print("Количество обновлено")
                except ValueError:
                    print("Ошибка: введите число")

            elif choice == '8':
                show_cart(cart)
                pid = input("ID товара для удаления: ").strip()
                cart.remove(pid)
                print("Товар удален")

            elif choice == '9':
                if not cart.get_items():
                    print("Корзина пуста!")
                    continue
                print("\nОФОРМЛЕНИЕ ЗАКАЗА")
                customer = {
                    'last_name': input("Фамилия: ").strip(),
                    'first_name': input("Имя: ").strip(),
                    'address': input("Адрес: ").strip(),
                    'phone': input("Телефон: ").strip(),
                    'email': input("Email: ").strip()
                }
                order, errors = create_order(customer, cart.get_items(), cart.get_total())
                if order:
                    print(f"\n{'='*40}")
                    print(f"ЗАКАЗ ОФОРМЛЕН!")
                    print(f"Номер заказа: {order['order_id']}")
                    print(f"Сумма: {order['total']:.2f} руб.")
                    print(f"Статус: {order['status']}")
                    print(f"{'='*40}")
                    cart.clear()
                else:
                    print("Ошибки валидации:")
                    for e in errors:
                        print(f"  - {e}")

            elif choice == '0':
                break
            else:
                print("Неверный выбор")

        except Exception as e:
            logger.error(f"Ошибка в меню покупателя: {e}")
            print(f"Произошла ошибка: {e}")


def admin_menu():
    """Меню администратора"""
    password = input("Пароль администратора: ").strip()
    if password != "admin":
        print("Неверный пароль")
        return

    while True:
        print(f"\n{'─'*40}")
        print("АДМИН-ПАНЕЛЬ:")
        print("  1. Все заказы")
        print("  2. Изменить статус заказа")
        print("  3. Добавить товар")
        print("  4. Редактировать товар")
        print("  5. Удалить товар")
        print("  0. Назад")
        choice = input("Выберите действие: ").strip()

        try:
            if choice == '1':
                orders = get_all_orders()
                if not orders:
                    print("Заказов нет")
                for o in orders:
                    print(f"\n  Заказ #{o['order_id']} | {o['date']} | Статус: {o['status']}")
                    print(f"  Клиент: {o['customer']['last_name']} {o['customer']['first_name']}")
                    for item in o['items']:
                        print(f"    - {item['name']} x{item['quantity']}")
                    print(f"  Сумма: {o['total']:.2f} руб.")

            elif choice == '2':
                oid = input("ID заказа: ").strip()
                print("Статусы: новый, в обработке, доставлен, отменен")
                status = input("Новый статус: ").strip().lower()
                ok, msg = change_order_status(oid, status)
                print(msg)

            elif choice == '3':
                print("\nКатегории: 1-Худ.лит, 2-Тех.лит, 3-Учеб.лит, 4-Дет.лит")
                cat_map = {'1': 'cat_01', '2': 'cat_02', '3': 'cat_03', '4': 'cat_04'}
                c = input("Номер категории: ").strip()
                if c in cat_map:
                    name = input("Название: ").strip()
                    author = input("Автор: ").strip()
                    price = float(input("Цена: "))
                    stock = int(input("Количество на складе: "))
                    desc = input("Описание: ").strip()
                    ok, msg = add_product(cat_map[c], name, author, price, stock, desc)
                    print(msg)
                else:
                    print("Неверный номер категории")

            elif choice == '4':
                pid = input("ID товара: ").strip()
                print("Оставьте поле пустым, чтобы не менять")
                updates = {}
                name = input("Новое название: ").strip()
                if name: updates['name'] = name
                author = input("Новый автор: ").strip()
                if author: updates['author'] = author
                price = input("Новая цена: ").strip()
                if price: updates['price'] = float(price)
                stock = input("Новый остаток: ").strip()
                if stock: updates['stock'] = int(stock)
                desc = input("Новое описание: ").strip()
                if desc: updates['description'] = desc
                if updates:
                    ok, msg = edit_product(pid, updates)
                    print(msg)
                else:
                    print("Нет изменений")

            elif choice == '5':
                pid = input("ID товара для удаления: ").strip()
                confirm = input(f"Удалить товар {pid}? (да/нет): ").strip().lower()
                if confirm == 'да':
                    ok, msg = delete_product(pid)
                    print(msg)
                else:
                    print("Отменено")

            elif choice == '0':
                break
            else:
                print("Неверный выбор")

        except Exception as e:
            logger.error(f"Ошибка в админ-панели: {e}")
            print(f"Произошла ошибка: {e}")


def main():
    """Главное меню"""
    logger.info("=== Запуск BookShop ===")
    data = load_products()
    cart = Cart()

    while True:
        print(f"\n{'='*40}")
        print(f"  {data['storeName']} — КНИЖНЫЙ МАГАЗИН")
        print(f"{'='*40}")
        print("  1. Магазин (покупатель)")
        print("  2. Админ-панель")
        print("  0. Выход")
        choice = input("Выберите раздел: ").strip()

        if choice == '1':
            customer_menu(cart, data)
        elif choice == '2':
            admin_menu()
        elif choice == '0':
            print("До свидания!")
            logger.info("=== Завершение BookShop ===")
            break
        else:
            print("Неверный выбор")


if __name__ == '__main__':
    main()