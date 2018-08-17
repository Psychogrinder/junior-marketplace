from flask import render_template, jsonify
from marketplace import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category/<category_name>')
def category(category_name):
    return render_template('category.html')

@app.route('/category/<category_name>/<product_id>')
def product_card(category_name, product_id):
    return render_template('product_card.html')

@app.route('/version')
def version():
    return jsonify(version=1.0)


if __name__ == '__main__':
    app.run(port=8000)
