import os
import urllib.request
import json
from models import db, Consumer, Producer, Order, Product, Category

# <editor-fold desc='DATA'>

# <editor-fold desc="Producer">
producer_names = ['безбрежный', 'бездонный', 'безмятежный', 'белоснежный', 'беспредельный', 'колоссальный',
                  'мировой', 'неиссякаемый', 'щедрый']

file = open('data/producer-description.txt', 'r')
description = file.read()
file.close()

with urllib.request.urlopen(f"https://randomuser.me/api/?results={len(producer_names)}") as response:
    data = response.read()
    data = json.loads(data)
    for company in data["results"]:
        producer = Producer(company['email'], 'Совхоз ' + producer_names.pop().title(), company['login']['password'],
                            company['phone'], company['location']['street'],
                            f"{company['name']['first']} {company['name']['last']}", description)
        db.session.add(producer)
    # </editor-fold>

# <editor-fold desc="Consumer">
with urllib.request.urlopen("https://randomuser.me/api/?results=100") as response:
    data = response.read()
    data = json.loads(data)
    for company in data["results"]:
        consumer = Consumer(company['email'], company['login']['password'], company['name']['first'],
                            company['name']['last'], company['phone'], company['location']['street'])
        db.session.add(consumer)
# </editor-fold>

# <editor-fold desc="Category">
category_data = {}
# with open(os.path.join(dir_path, 'data/categories.txt'), 'r') as f:
with open('data/categories.txt', 'r') as f:
    cat = None
    sub_cats = None
    for i, line in enumerate(f.readlines()):
        if i % 2 == 0:
            cat = line.strip()
        else:
            sub_cats = [item.rstrip('\n') for item in line.split(', ')]
category_data[cat] = sub_cats

i = 0
subcategory_ids = []
for category_name in category_data:
    i += 1
    current_base_category_id = i
    category = Category(category_name)
    db.session.add(category)
    for subcategory_name in category_data[category_name]:
        i += 1
        subcategory_ids.append(id)
        category = Category(subcategory_name, parent_id=current_base_category_id)
        db.session.add(category)
# </editor-fold>

# # <editor-fold desc="Product">
# prices = range(50, 1000)
# quantity = range(100, 500)
# producer_ids = (1, len(producer_names)+1)
# #subcategory_ids
# measurement_units = ['кг', 'литры', 'штуки']
# weights = range(5, 50)
# # </editor-fold>


# </editor-fold>

db.session.commit()