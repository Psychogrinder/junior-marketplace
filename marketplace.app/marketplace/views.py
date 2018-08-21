import os
from flask import render_template, jsonify
from marketplace import app
from marketplace.models import Category, Product, Producer, Consumer, Order
import marketplace.api_folder.api_utils as utils


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
    category = Category.query.filter_by(slug=category_name).first()
    subcategories = Category.query.filter_by(parent_id=category.id).all()
    category_name = category.name.title()
    producers = Producer.query.filter_by(entity='producer').all()
    products = utils.get_products_by_category_id(category.id)
    return render_template('category.html', products=products, subcategories=subcategories, category=category,
                           category_name=category_name, producers=producers)


@app.route('/products/<product_id>')
def product_card(product_id):
    product = Product.query.filter_by(id=product_id).first()
    category = utils.get_category_by_id(product.category_id)
    category_name = utils.get_category_by_id(product.category_id).name.title()
    producer_name = utils.get_producer_by_id(product.producer_id).name.title()
    return render_template('product_card.html', category_name=category_name, product=product,
                           producer_name=producer_name, category=category)


# товары производителя
@app.route('/producer/<producer_id>/products')
def producer_products(producer_id):
    products = Product.query.filter_by(producer_id=producer_id).all()
    return render_template('producer_products.html', products=products)


@app.route('/producer/<producer_id>/products/<product_id>/edit')
def edit_product(producer_id, product_id):
    product = Product.query.filter_by(id=product_id).first()
    base_categories = Category.query.filter_by(parent_id=0).all()
    category = utils.get_category_by_id(product.category_id)
    category_name = utils.get_category_by_id(product.category_id).name
    parent_category_name = Category.query.filter_by(id=category.parent_id).first().name
    all_categories = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path+'/content/data/categories.txt', 'r') as f:
        cat = None
        sub_cats = None
        for i, line in enumerate(f.readlines()):
            if i % 2 == 0:
                cat = line.strip()
            else:
                sub_cats = [item.rstrip('\n') for item in line.split(', ')]
                all_categories[cat] = sub_cats

    return render_template('edit_product.html', product=product, category=category, category_name=category_name,
                           base_categories=base_categories, parent_category_name=parent_category_name, all_categories=all_categories)


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


@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))

    return dict(mdebug=print_in_console)


if __name__ == '__main__':
    app.run(port=8000)
