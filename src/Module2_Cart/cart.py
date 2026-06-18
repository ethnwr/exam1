from logger import logger


class Cart:
    def __init__(self):
        self.items = {}  # {product_id: {'product': {...}, 'quantity': int}}

    def add(self, product, quantity=1):
        """Добавить товар в корзину"""
        pid = product['id']
        if pid in self.items:
            self.items[pid]['quantity'] += quantity
        else:
            self.items[pid] = {'product': product, 'quantity': quantity}
        logger.info(f"Добавлено в корзину: {product['name']} x{quantity}")

    def remove(self, product_id):
        """Удалить товар из корзины"""
        if product_id in self.items:
            name = self.items[product_id]['product']['name']
            del self.items[product_id]
            logger.info(f"Удалено из корзины: {name}")

    def update_quantity(self, product_id, quantity):
        """Изменить количество"""
        if product_id in self.items:
            if quantity <= 0:
                self.remove(product_id)
            else:
                self.items[product_id]['quantity'] = quantity
            logger.info(f"Обновлено количество: {product_id} -> {quantity}")

    def get_total(self):
        """Общая сумма"""
        return sum(item['product']['price'] * item['quantity'] for item in self.items.values())

    def get_items(self):
        """Получить все товары корзины"""
        return list(self.items.values())

    def clear(self):
        """Очистить корзину"""
        self.items = {}
        logger.info("Корзина очищена")

    def to_dict(self):
        """Сериализация для сохранения"""
        return {pid: {'product': item['product'], 'quantity': item['quantity']} for pid, item in self.items.items()}

    def from_dict(self, data):
        """Загрузка из словаря"""
        self.items = data