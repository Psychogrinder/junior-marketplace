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
    category = Category.query.filter_by(slug=category_name).first()
    products = Product.query.filter_by(category_id=category.id).all()
    return render_template('category.html', products=products)



@app.route('/category/<category_name>/<product_id>')
def product_card(category_name, product_id):
    product = Product.query.filter_by(id=product_id).first()
    return render_template('product_card.html', product=product)


# товары производителя
@app.route('/producer/<producer_id>/products')
def producer_products(producer_id):
    products = Product.query.filter_by(producer_id=producer_id).all()
    return render_template('producer_products.html', products=products)

@app.route('/producer/<producer_id>/products/<product_id>/edit')
def edit_product(producer_id, product_id):
    return render_template('edit_product.html')


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


if __name__ == '__main__':
    app.run(port=8000)
