from marketplace import app

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/version')
def version():
    return jsonify(version=1.0)


if __name__ == '__main__':
    app.run(port=8000)
