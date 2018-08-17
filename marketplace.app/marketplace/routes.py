from marketplace import app
from marketplace.models import Consumer


@app.route('/')
def hello_world():
    # a = Consumer(email='addыыasd', password='cadsaвывфыsdd', first_name='Egor', last_name='Galkin')
    print([cons.get_full_name() for cons in Consumer.query.all()])



if __name__ == '__main__':
    app.run()
