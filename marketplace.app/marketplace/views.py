from flask import render_template, jsonify, redirect, url_for, flash, abort
from flask_restful import reqparse
from marketplace import app, email, db
from marketplace.models import Category, Product, Producer, Consumer, Order, User
import marketplace.api_folder.api_utils as utils
from flask_login import current_user, login_user, logout_user
import os


# каталог
@app.route('/')
def index():
    categories = Category.query.filter_by(parent_id=0).all()
    popular_products = Product.query.order_by(Product.times_ordered.desc()).limit(12).all()
    return render_template(
        'index.html',
        categories=categories,
        popular_products=popular_products
    )


@app.route('/category/<category_name>')
def category(category_name):
    category = utils.get_category_by_name(category_name)
    subcategories = utils.get_subcategories_by_category_id(category.id)
    category_name = category.name.title()
    producers = utils.get_all_producers()
    products = utils.get_products_by_category_id(category.id)
    return render_template('category.html', products=products, subcategories=subcategories, category=category,
                           category_name=category_name, producers=producers)


@app.route('/products/<product_id>')
def product_card(product_id):
    product = utils.get_product_by_id(product_id)
    category = utils.get_category_by_id(product.category_id)
    producer = utils.get_producer_by_id(product.producer_id)
    return render_template('product_card.html', category_name=category.name.title(), product=product,
                           producer_name=producer.name.title(), category=category)


# товары производителя
@app.route('/producer/<producer_id>/products')
def producer_products(producer_id):
    products = utils.get_products_by_producer_id(producer_id)
    return render_template('producer_products.html', products=products)

# Продумать что делать с неиспользованными id в методах

@app.route('/producer/<producer_id>/products/<product_id>/edit')
def edit_product(producer_id, product_id):
    product = utils.get_product_by_id(product_id)
    base_categories = utils.get_all_base_categories()
    category = utils.get_category_by_id(product.category_id)
    parent_category = utils.get_category_by_id(category.parent_id)
    all_categories = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/content/data/categories.txt', 'r') as f:
        cat = None
        sub_cats = None
        for i, line in enumerate(f.readlines()):
            if i % 2 == 0:
                cat = line.strip()
            else:
                sub_cats = [item.rstrip('\n') for item in line.split(', ')]
                all_categories[cat] = sub_cats

    eng_cats = []
    with open(dir_path + '/content/data/categories_eng.txt', 'r') as f:
        for line in f.readlines():
            eng_cats += [word.strip('\n') for word in line.split(',')]

    rus_cats = []
    for k, v in all_categories.items():
        rus_cats += [k] + v

    eng_rus_cats = {}
    for i, rus_cat in enumerate(rus_cats):
        eng_rus_cats[rus_cat] = eng_cats[i]

    measurement_units = ['кг', 'литры', 'штуки']

    return render_template('edit_product.html', product=product, category=category, category_name=category.name,
                           base_categories=base_categories, parent_category_name=parent_category.name,
                           all_categories=all_categories, eng_rus_cats=eng_rus_cats,
                           measurement_units=measurement_units)


@app.route('/producer/<producer_id>/create_product')
def create_product(producer_id):
    return render_template('create_product.html')


# корзина
@app.route('/cart/<user_id>')
def cart(user_id):
    user = Consumer.query.filter_by(id=user_id).first()
    return render_template('cart.html', user=user)


@app.route('/cart/<user_id>/order_registration/')
def order_registration(user_id):
    return render_template('order_registration.html')


# покупатель
@app.route('/user/<user_id>')
def customer_profile(user_id):
    user = Consumer.query.filter_by(id=user_id).first()
    return render_template('customer_profile.html', user=user)


@app.route('/user/edit/<user_id>')
def edit_customer(user_id):
    user = Consumer.query.filter_by(id=user_id).first()
    return render_template('edit_customer.html', user=user)


@app.route('/order_history/<user_id>')
def order_history(user_id):
    orders = Order.query.filter_by(consumer_id=user_id)
    return render_template('order_history.html', orders=orders)


# производитель
@app.route('/producer/<producer_id>')
def producer_profile(producer_id):
    producer = Producer.query.filter_by(id=producer_id).first()
    return render_template('producer_profile.html', producer=producer)


@app.route('/producer/<producer_id>/edit')
def edit_producer(producer_id):
    producer = Producer.query.filter_by(id=producer_id).first()
    return render_template('edit_producer.html', producer=producer)


@app.route('/producer/<producer_id>/orders')
def producer_orders(producer_id):
    return render_template('producer_orders.html')


# о нас и помощь
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/customer_help')
def customer_help():
    return render_template('customer_help.html')


@app.route('/producer_help')
def producer_help():
    return render_template('producer_help.html')


@app.route('/version')
def version():
    return jsonify(version=1.0)


# Login and Logout

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    parser = reqparse.RequestParser()
    parser.add_argument('email')
    parser.add_argument('password')
    args = parser.parse_args()
    if args is not None:
        user = User.query.filter_by(email=args['email']).first()
        if user is None or not user.check_password(args['password']):
            return 'Invalid email or password'
        login_user(user, True)
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/email_confirm/<token>')
def email_confirm(token):
    user_email = email.confirm_token(token)
    if user_email is None:
        # TODO перенаправить на красивую страничку для ошибок
        return abort(404)
    user = User.query.filter_by(email=user_email).first()
    if user is None:
        # TODO перенаправить на красивую страничку для ошибок
        return abort(404)
    user.verify_email()
    db.session.add(user)
    db.session.commit()
    flash('Адрес электронной почты подтвержден', category='info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=8000)
