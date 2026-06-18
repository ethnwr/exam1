from flask import Flask, render_template, request, redirect, url_for, session, flash
from Module1_Catalog.catalog import load_products, get_all_products, search_by_name, filter_by_category, find_product
from Module2_Cart.cart import Cart
from Module3_Order.order import create_order
from Module4_Admin.admin import get_all_orders, change_order_status, add_product, edit_product, delete_product
from logger import logger
import os

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'bookshop-secret-key-2024'  # для сессий


def get_cart():
    """Получить корзину из сессии"""
    if 'cart' not in session:
        session['cart'] = {}
    cart = Cart()
    cart.from_dict(session['cart'])
    return cart


def save_cart(cart):
    """Сохранить корзину в сессию"""
    session['cart'] = cart.to_dict()
    session.modified = True


# ========== ГЛАВНАЯ (КАТАЛОГ) ==========
@app.route('/')
def index():
    data = load_products()
    products = get_all_products(data)
    query = request.args.get('q', '').strip()
    cat = request.args.get('cat', '').strip()

    if query:
        products = search_by_name(data, query)
    elif cat:
        products = filter_by_category(data, cat)
        for p in products:
            p['category'] = next((c['name'] for c in data['categories'] if c['id'] == cat), '')

    return render_template('index.html', products=products, data=data, query=query, cat=cat)


# ========== КОРЗИНА ==========
@app.route('/cart')
def cart_view():
    cart = get_cart()
    return render_template('cart.html', cart=cart)


@app.route('/cart/add/<product_id>')
def cart_add(product_id):
    data = load_products()
    product = find_product(data, product_id)
    if product:
        cart = get_cart()
        cart.add(product)
        save_cart(cart)
        flash(f'"{product["name"]}" добавлена в корзину', 'success')
    return redirect(url_for('index'))


@app.route('/cart/remove/<product_id>')
def cart_remove(product_id):
    cart = get_cart()
    cart.remove(product_id)
    save_cart(cart)
    flash('Товар удалён из корзины', 'info')
    return redirect(url_for('cart_view'))


@app.route('/cart/update/<product_id>', methods=['POST'])
def cart_update(product_id):
    qty = int(request.form.get('quantity', 1))
    cart = get_cart()
    cart.update_quantity(product_id, qty)
    save_cart(cart)
    return redirect(url_for('cart_view'))


# ========== ОФОРМЛЕНИЕ ЗАКАЗА ==========
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = get_cart()
    if not cart.get_items():
        flash('Корзина пуста', 'warning')
        return redirect(url_for('cart_view'))

    if request.method == 'POST':
        customer = {
            'last_name': request.form['last_name'],
            'first_name': request.form['first_name'],
            'address': request.form['address'],
            'phone': request.form['phone'],
            'email': request.form['email']
        }
        order, errors = create_order(customer, cart.get_items(), cart.get_total())
        if order:
            cart.clear()
            save_cart(cart)
            flash(f'Заказ №{order["order_id"]} оформлен! Сумма: {order["total"]:.2f} руб.', 'success')
            return render_template('cart.html', cart=cart, order=order)
        else:
            for e in errors:
                flash(e, 'danger')

    return render_template('cart.html', cart=cart, checkout=True)


# ========== АДМИН-ПАНЕЛЬ ==========
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == 'admin':
            session['admin'] = True
        else:
            flash('Неверный пароль', 'danger')
            return render_template('admin.html', logged_in=False)

    if not session.get('admin'):
        return render_template('admin.html', logged_in=False)

    data = load_products()
    orders = get_all_orders()
    action = request.args.get('action', '')

    # Смена статуса заказа
    if action == 'status' and request.method == 'POST':
        oid = request.form['order_id']
        status = request.form['status']
        ok, msg = change_order_status(oid, status)
        flash(msg, 'success' if ok else 'danger')

    # Добавление товара
    if action == 'add_product' and request.method == 'POST':
        ok, msg = add_product(
            request.form['category_id'],
            request.form['name'],
            request.form['author'],
            float(request.form['price']),
            int(request.form['stock']),
            request.form['description']
        )
        flash(msg, 'success' if ok else 'danger')

    # Редактирование товара
    if action == 'edit_product' and request.method == 'POST':
        updates = {}
        for field in ['name', 'author', 'price', 'stock', 'description']:
            val = request.form.get(field, '').strip()
            if val:
                updates[field] = float(val) if field == 'price' else (int(val) if field == 'stock' else val)
        if updates:
            ok, msg = edit_product(request.form['product_id'], updates)
            flash(msg, 'success' if ok else 'danger')

    # Удаление товара
    if action == 'delete_product':
        pid = request.args.get('id', '')
        ok, msg = delete_product(pid)
        flash(msg, 'success' if ok else 'danger')

    # Обновляем данные после изменений
    data = load_products()
    orders = get_all_orders()

    return render_template('admin.html', logged_in=True, data=data, orders=orders)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin'))


if __name__ == '__main__':
    logger.info("=== Запуск BookShop (Flask) ===")
    app.run(debug=True, port=5000)