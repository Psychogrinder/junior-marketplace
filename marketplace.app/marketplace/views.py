from flask import render_template, jsonify
from marketplace import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')


# каталог и товары
@app.route('/category/<category_name>')
def category(category_name):
    return render_template('category.html')

@app.route('/category/<category_name>/<product_id>')
def product_card(category_name, product_id):
    return render_template('product_card.html')


# покупатель
@app.route('/user/<user_id>')
def customer_profile(user_id):
    return render_template('customer_profile.html')

@app.route('/user/<user_id>/edit')
def edit_customer(user_id):
    return render_template('edit_customer.html')


# производитель
@app.route('/producer/<producer_id>')
def producer_profile(producer_id):
    return render_template('producer_profile.html')

@app.route('/producer/<producer_id>/edit')
def edit_producer(producer_id):
    return render_template('edit_producer.html')


@app.route('/version')
def version():
    return jsonify(version=1.0)


if __name__ == '__main__':
    app.run(port=8000)
