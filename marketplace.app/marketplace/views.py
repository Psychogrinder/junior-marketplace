from flask import render_template, jsonify
from marketplace import app
from marketplace.models import Category, Product, Producer, Consumer, Order


# каталог
@app.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)


@app.route('/category/<category_name>')
def category(category_name):
    category = Category.query.filter_by(slug=category_name)
    products = Product.query.filter_by(category_id=category.id)
    return render_template('category.html', products=products)


@app.route('/category/<category_name>/<product_id>')
def product_card(category_id, product_id):
    return render_template('product_card.html')


# товары производителя
@app.route('/producer/<producer_id>/products')
def producer_products(producer_id):
    products = Product.query.filter_by(producer_id=producer_id).all()
    return render_template('producer_products.html', products=products)


# корзина
@app.route('/cart/<user_id>')
def cart(user_id):
    user = Consumer.query.filter_by(id=user_id).first()
    return render_template('cart.html', user=user)


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


@app.route('/version')
def version():
    return jsonify(version=1.0)


if __name__ == '__main__':
    app.run(port=8000)
