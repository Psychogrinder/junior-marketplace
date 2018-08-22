import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(os.path.realpath(dir_path))
sys.path.insert(0, dir_path)
from models import *

categories = Category.query.all()
for category in categories:
    category.producers = []
    db.session.commit()

for model in [Consumer, Producer, Category, Order, Product]:
    db.session.query(model).delete()
db.session.commit()



sys.exit()
