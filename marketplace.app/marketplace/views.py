from flask import render_template, jsonify, redirect, url_for, flash, abort, request
import os
from marketplace.forms import ResetPasswordForm
import time
from flask_restful import reqparse
from marketplace import app, email_tools, db
from marketplace.api_folder.utils import product_utils, category_utils, producer_utils, cart_utils, order_utils, \
    comment_utils
from marketplace.models import Category, Product, Producer, Consumer, Order, User, Cart
from flask_login import current_user, login_user, logout_user, login_required


# каталог
@app.route('/')
def index():
    categories = Category.query.filter_by(parent_id=0).all()
    popular_products = product_utils.get_popular_products()
    meta_description = 'Маркетплейс фермерских товаров'
    # Временно. Без принта ломается: если entity == consumer, то на главной старнице
    # user - Anonymous вместо Consumer.
    print(current_user)
    return render_template(
        'index.html',
        categories=categories,
        popular_products=popular_products,
        producers=Producer.query.all(),
        current_user=current_user,
        meta_description=meta_description,
    )


@app.route('/category/<category_name>')
def category(category_name):
    category = category_utils.get_category_by_name(category_name)
    subcategories = category_utils.get_subcategories_by_category_id(category.id)
    category_name = category.name.title()
    producers = producer_utils.get_all_producers()
    products = product_utils.get_products_by_category_id(category.id)
    meta_description = 'каталог фермерских товаров маркетплейс'
    return render_template('category.html', products=products, subcategories=subcategories, category=category,
                           category_name=category_name, producers=producers, current_user=current_user,
                           meta_description=meta_description)


@app.route('/products/<int:product_id>')
def product_card(product_id):
    product = product_utils.get_product_by_id(product_id)
    category = category_utils.get_category_by_id(product.category_id)
    producer = producer_utils.get_producer_by_id(product.producer_id)
    comments = comment_utils.get_comments_by_product_id(product_id)
    next_page = comments.next_num
    meta_description = 'каталог фермерских товаров Маркетплейс'
    return render_template('product_card.html', category_name=category.name.title(), product=product,
                           producer_name=producer.name.title(), category=category, current_user=current_user,
                           comments=comments.items, next_page=next_page, meta_description=meta_description)


# товары производителя
@app.route('/producer/<int:producer_id>/products')
def producer_products(producer_id):
    if current_user.is_authenticated and current_user.id == producer_id and current_user.entity == 'producer':
        products = product_utils.get_products_by_producer_id(producer_id)
        meta_description = 'все товары производителя Маркетплейс'
        return render_template('producer_products.html', products=products, current_user=current_user,
                               meta_description=meta_description, producer_name=current_user.name)
    else:
        return redirect(url_for('index'))


# Продумать что делать с неиспользованными id в методах
@app.route('/producer/<int:producer_id>/products/<int:product_id>/edit')
def edit_product(producer_id, product_id):
    if current_user.is_authenticated and current_user.id == producer_id and current_user.entity == 'producer':
        product = product_utils.get_product_by_id(product_id)
        categories = Category.query.all()
        measurement_units = ['кг', 'л', 'шт']
        meta_description = 'редактирование товара Маркетплейс'
        return render_template('edit_product.html', product=product, categories=categories,
                               measurement_units=measurement_units, current_user=current_user,
                               meta_description=meta_description)
    else:
        return redirect(url_for('index'))


@app.route('/producer/<int:producer_id>/create_product')
def create_product(producer_id):
    if current_user.is_authenticated and current_user.id == producer_id and current_user.entity == 'producer':
        meta_description = 'Добавление товара Маркетплейс'
        return render_template('create_product.html', current_user=current_user, meta_description=meta_description)
    else:
        return redirect(url_for('index'))


# корзина
@app.route('/cart/<int:user_id>')
def cart(user_id):
    if current_user.is_authenticated and current_user.id == user_id and current_user.entity == 'consumer':
        items = {}
        products = {}
        cart = Cart.query.filter_by(consumer_id=current_user.id).first()
        meta_description = 'Корзина Маркетплейс'
        if cart is not None:
            items = {int(k): (v) for k, v in cart.items.items()}
            products = cart_utils.get_products_from_cart(items)
            return render_template('cart.html', current_user=current_user, items=items,
                                   products=products, meta_description=meta_description)
    else:
        return redirect(url_for('index'))


@app.route('/cart/<int:user_id>/order_registration')
def order_registration(user_id):

    if current_user.is_authenticated and current_user.id == user_id and current_user.entity == 'consumer':
        cart = Cart.query.filter_by(consumer_id=current_user.id).first()
        if not cart or not cart.items:
            return redirect(url_for('cart', user_id=user_id))
        products = cart_utils.get_products_from_cart(cart.items)
        producer_ids = set(product.producer_id for product in products)
        producers = [producer_utils.get_producer_by_id(id) for id in producer_ids]
        meta_description = 'Оформление заказа Маркетплейс'
        return render_template(
            'order_registration.html',
            current_user=current_user,
            producers=producers,
            items=cart.items,
            products=products,
            meta_description=meta_description
        )
    else:
        return redirect(url_for('index'))


# покупатель
@app.route('/user/<int:user_id>')
def consumer_profile(user_id):
    if current_user.is_authenticated and current_user.id == user_id and current_user.entity == 'consumer':
        meta_description = 'Профиль пользователя Маркетплейс'
        return render_template(
            'consumer_profile.html',
            user=current_user,
            current_user=current_user,
            meta_description=meta_description
        )
    else:
        return redirect(url_for('index'))


@app.route('/user/edit/<int:user_id>')
def edit_consumer(user_id):
    if current_user.is_authenticated and current_user.id == user_id and current_user.entity == 'consumer':
        meta_description = 'Редактирование профиля пользователя Маркетплейс'
        return render_template(
            'edit_consumer.html',
            user=current_user,
            current_user=current_user,
            meta_description=meta_description
        )
    else:
        return redirect(url_for('index'))


@app.route('/order_history/<int:user_id>')
def order_history(user_id):
    if current_user.is_authenticated and current_user.id == user_id and current_user.entity == 'consumer':
        meta_description = 'История заказов пользователя Маркетплейс'
        return render_template(
            'order_history.html',
            current_user=current_user,
            meta_description=meta_description,
            user=current_user
        )
    else:
        return redirect(url_for('index'))


# производитель
@app.route('/producer/<int:producer_id>')
def producer_profile(producer_id):
    producer = Producer.query.filter_by(id=producer_id).first()
    meta_description = 'Профиль производителя Маркетплейс'
    if producer is not None and producer.entity == 'producer':
        return render_template(
            'producer_profile.html',
            producer=producer,
            current_user=current_user,
            meta_description=meta_description
        )
    else:
        return abort(404)


@app.route('/producer/<int:producer_id>/edit')
def edit_producer(producer_id):
    if current_user.is_authenticated and current_user.id == producer_id and current_user.entity == 'producer':
        meta_description = 'Редактирование профиля производителя Маркетплейс'
        return render_template(
            'edit_producer.html',
            producer=current_user,
            current_user=current_user,
            meta_description=meta_description
        )
    else:
        return redirect(url_for('index'))


@app.route('/producer/<int:producer_id>/orders')
def producer_orders(producer_id):
    if current_user.is_authenticated and current_user.id == producer_id and current_user.entity == 'producer':
        orders = Order.query.filter_by(producer_id=producer_id).all()
        meta_description = 'Заказы производителя Маркетплейс'
        products = {}
        for order in orders:
            products[order.id] = order_utils.get_products_by_order_id(order.id)
        return render_template(
            'producer_orders.html',
            current_user=current_user,
            orders=orders,
            products=products,
            meta_description=meta_description
        )
    else:
        return redirect(url_for('index'))


# о нас и помощь
@app.route('/about_us')
def about_us():
    meta_description = 'О нас - Маркетплейс фермерских товаров'
    return render_template('about_us.html', meta_description=meta_description)


@app.route('/consumer_help')
def consumer_help():
    meta_description = 'Помощь для покупателей - Маркетплейс фермерских товаров'
    return render_template('consumer_help.html', meta_description=meta_description)


@app.route('/producer_help')
def producer_help():
    meta_description = 'Помощь для производителей - Маркетплейс фермерских товаров'
    return render_template('producer_help.html', meta_description=meta_description)


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
    meta_description = 'Сброс пароля - Маркетплейс фермерских товаров'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    return render_template(
        'reset_password.html',
        form=form,
        meta_description=meta_description
    )


@app.route('/search')
def global_search():
    meta_description = 'Поиск по каталогу - Маркетплейс фермерских товаров'
    products = product_utils.search_by_keyword(request.args.get('find'))
    return render_template(
        'global_search_results.html',
        products=products,
        meta_description=meta_description
    )


@app.route('/review')
def review():
    if not current_user.is_authenticated:
        return abort(404)
    order_id = request.args.get('order_id')
    try:
        order = order_utils.get_order_by_id(int(order_id))
    except TypeError:
        return abort(404)
    if not order:
        return abort(404)
    current_user_id = current_user.id
    # Если пользователь пытается оставить отзыв на чужой заказ
    if current_user_id != order.consumer_id:
        return abort(404)

    # Если пользователь вновь пытается оставить отзыв на тот же заказ
    if order.reviewed:
        return abort(404)

    products = product_utils.get_products_by_order_id(order_id)
    number_of_products = len(products)
    meta_description = 'Оставить отзыв - Маркетплейс фермерских товаров'
    return render_template(
        'review.html',
        order=order,
        products=products,
        number_of_products=number_of_products,
        meta_description=meta_description
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 503


if __name__ == '__main__':
    app.run(port=8000)
