from flask import render_template, jsonify, redirect, url_for, flash, abort
import os
from marketplace.forms import ResetPasswordForm
import time
from flask_restful import reqparse
from marketplace import app, email_tools, db
from marketplace.api_folder.utils import product_utils, category_utils, producer_utils, cart_utils, order_utils
from marketplace.models import Category, Product, Producer, Consumer, Order, User, Cart
from flask_login import current_user, login_user, logout_user, login_required


# каталог
@app.route('/')
def index():
    categories = Category.query.filter_by(parent_id=0).all()
    popular_products = product_utils.get_popular_products()
    return render_template(
        'index.html',
        categories=categories,
        popular_products=popular_products,
        producers=Producer.query.all(),
        current_user=current_user,
    )


@app.route('/category/<category_name>')
def category(category_name):
    category = category_utils.get_category_by_name(category_name)
    subcategories = category_utils.get_subcategories_by_category_id(category.id)
    category_name = category.name.title()
    producers = producer_utils.get_all_producers()
    products = product_utils.get_products_by_category_id(category.id)
    return render_template('category.html', products=products, subcategories=subcategories, category=category,
                           category_name=category_name, producers=producers, current_user=current_user)


@app.route('/products/<product_id>')
def product_card(product_id):
    product = product_utils.get_product_by_id(product_id)
    category = category_utils.get_category_by_id(product.category_id)
    producer = producer_utils.get_producer_by_id(product.producer_id)
    return render_template('product_card.html', category_name=category.name.title(), product=product,
                           producer_name=producer.name.title(), category=category, current_user=current_user)


# товары производителя
@app.route('/producer/<producer_id>/products')
def producer_products(producer_id):
    products = product_utils.get_products_by_producer_id(producer_id)
    if current_user.id == int(producer_id):
        return render_template('producer_products.html', products=products, current_user=current_user)
    else:
        return redirect(url_for('index'))


# Продумать что делать с неиспользованными id в методах
@app.route('/producer/<producer_id>/products/<product_id>/edit')
def edit_product(producer_id, product_id):
    product = product_utils.get_product_by_id(product_id)
    categories = Category.query.all()
    measurement_units = ['кг', 'л', 'шт']
    if current_user.id == int(producer_id):
        return render_template('edit_product.html', product=product, categories=categories,
                               measurement_units=measurement_units, current_user=current_user)
    else:
        return redirect(url_for('index'))


@app.route('/producer/<producer_id>/create_product')
def create_product(producer_id):
    if current_user.id == int(producer_id):
        return render_template('create_product.html', current_user=current_user)
    else:
        return redirect(url_for('index'))


# корзина
@app.route('/cart/<user_id>')
def cart(user_id):
    # user = Consumer.query.filter_by(id=user_id).first()
    items = {}
    products = {}
    cart = Cart.query.filter_by(consumer_id=current_user.id).first()
    if cart is not None:
        items = {int(k): (v) for k, v in cart.items.items()}
        products = cart_utils.get_products_from_cart(items)
    # producer_ids = set(product.producer_id for product in products)
    # producers = [utils.get_producer_by_id(id) for id in producer_ids]
    if current_user.id == int(user_id):
        return render_template('cart.html', current_user=current_user, items=items,
                               products=products)
    else:
        return redirect(url_for('index'))


@app.route('/cart/<user_id>/order_registration/')
def order_registration(user_id):
    user = Consumer.query.filter_by(id=user_id).first()
    items = Cart.query.filter_by(consumer_id=user.id).first().items
    items = {int(k): (v) for k, v in items.items()}
    products = cart_utils.get_products_from_cart(items)
    producer_ids = set(product.producer_id for product in products)
    producers = [producer_utils.get_producer_by_id(id) for id in producer_ids]
    if current_user.id == int(user_id):
        return render_template('order_registration.html', current_user=current_user, producers=producers, items=items,
                               products=products)
    else:
        return redirect(url_for('index'))


# покупатель
@app.route('/user/<user_id>')
def consumer_profile(user_id):
    user = Consumer.query.filter_by(id=user_id).first()
    if current_user.id == int(user_id):
        return render_template('consumer_profile.html', user=user, current_user=current_user)
    else:
        return redirect(url_for('index'))


@app.route('/user/edit/<user_id>')
def edit_consumer(user_id):
    user = Consumer.query.filter_by(id=user_id).first()
    if current_user.id == int(user_id):
        return render_template('edit_consumer.html', user=user, current_user=current_user)
    else:
        return redirect(url_for('index'))


@app.route('/order_history/<user_id>')
def order_history(user_id):
    orders = Order.query.filter_by(consumer_id=user_id).all()
    all_products = []
    producer_names = {}
    for order in orders:
        all_products += (product_utils.get_all_products_from_order(order.id))
        producer_names[order.producer_id] = producer_utils.get_producer_by_id(int(order.producer_id)).name
    if current_user.id == int(user_id):
        return render_template('order_history.html', orders=orders, current_user=current_user, products=all_products,
                               producer_names=producer_names)
    else:
        return redirect(url_for('index'))


# производитель
@app.route('/producer/<producer_id>')
def producer_profile(producer_id):
    producer = Producer.query.filter_by(id=producer_id).first()
    if producer != None:
        return render_template('producer_profile.html', producer=producer, current_user=current_user)


@app.route('/producer/<producer_id>/edit')
def edit_producer(producer_id):
    producer = Producer.query.filter_by(id=producer_id).first()
    if current_user.id == int(producer_id):
        return render_template('edit_producer.html', producer=producer, current_user=current_user)
    else:
        return redirect(url_for('index'))


@app.route('/producer/<producer_id>/orders')
def producer_orders(producer_id):
    if current_user.id == int(producer_id):
        orders = Order.query.filter_by(producer_id=int(producer_id)).all()
        products = {}
        for order in orders:
            products[order.id] = order_utils.get_all_products_from_order(order.id)
        return render_template('producer_orders.html', current_user=current_user, orders=orders, products=products )
    else:
        return redirect(url_for('index'))


# о нас и помощь
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/consumer_help')
def consumer_help():
    return render_template('consumer_help.html')


@app.route('/producer_help')
def producer_help():
    return render_template('producer_help.html')


@app.route('/version')
def version():
    return jsonify(version=1.0)


@app.route('/email_confirm/<token>')
def email_confirm(token):
    user_email = email_tools.confirm_token(token)
    if user_email is None:
        return abort(404)
    user = User.query.filter_by(email=user_email).first()
    if user is None:
        return abort(404)
    user.verify_email()
    db.session.add(user)
    db.session.commit()
    flash('Адрес электронной почты подтвержден', category='info')
    return redirect(url_for('index'))


@app.route('/password/recovery/<token>', methods=['GET', 'POST'])
def password_recovery(token):
    payload = email_tools.confirm_token(token)
    if payload is None:
        return redirect(url_for('index'))
    user = User.query.filter_by(email=payload['email']).first()
    if user is None:
        return redirect(url_for('index'))
    expires_on = payload['expires']
    if expires_on - time.time() < 0:
        flash('Время действия ссылки закончилось', category='info')
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Пароль успешно изменен', category='info')
        return redirect(url_for('index'))
    return render_template('reset_password.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 503


if __name__ == '__main__':
    app.run(port=8000)
