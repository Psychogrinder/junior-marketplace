import os
import sys
import ssl
import urllib.request
import json
from random import choice

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(os.path.realpath(dir_path))
sys.path.insert(0, dir_path)
from models import *

context = ssl._create_unverified_context()

producer_names = ['безбрежный', 'бездонный', 'безмятежный', 'белоснежный', 'беспредельный', 'колоссальный',
                  'мировой', 'неиссякаемый', 'щедрый']

number_of_producers = len(producer_names)

file = open('data/producer-description.txt', 'r')
description = file.read()
file.close()

with urllib.request.urlopen("https://randomuser.me/api/?results={}".format(len(producer_names)),
                            context=context) as response:
    data = response.read()
    data = json.loads(data)
    for i, company in enumerate(data["results"]):
        producer = Producer('123123', f'pro{i+1}.ru', 'Совхоз ' + producer_names.pop().title(),
                            company['phone'], company['location']['street'],
                            "{} {}".format(company['name']['first'], company['name']['last']), description)
        db.session.add(producer)

for i, producer in enumerate(Producer.query.all()):
    producer.id = i + 1

with urllib.request.urlopen("https://randomuser.me/api/?results=100", context=context) as response:
    data = response.read()
    data = json.loads(data)
    email_counter = 1
    for person in data["results"]:
        consumer = Consumer('{}mail.ru'.format(email_counter), '123123', person['name']['first'],
                            person['name']['last'], person['phone'], person['location']['street'])
        db.session.add(consumer)
        email_counter += 1

category_data = {}

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
for category_name in category_data:
    i += 1
    current_base_category_id = i
    category = Category(category_name)
    db.session.add(category)
    for subcategory_name in category_data[category_name]:
        i += 1
        category = Category(subcategory_name, parent_id=current_base_category_id)
        db.session.add(category)

for i, cat in enumerate(Category.query.all()):
    cat.id = i + 1

category_eng_names = []

with open('data/categories_eng.txt', 'r') as f:
    for line in f.readlines():
        category_eng_names += [word.strip() for word in line.split(',')]

for i, cat in enumerate(Category.query.all()):
    cat.slug = category_eng_names[i]

prices = range(50, 1000)
quantity = range(100, 500)
producer_ids = range(1, number_of_producers + 1)
measurement_units = ['кг', 'л', 'шт']
weights = range(5, 50)
product_descriptions = ['Очень вкусный продукт', 'Самый вкусный продукт']

product_names = {"птица": {
    "курятина": ["Голень курицы", "Бедро курицы", "Тушка курицы"],
    "гусятина": ["Голень гуся", "Бедро гуся", "Тушка гуся"],
    "индюшатина": ["Голень индюшки", "Бедро индюшки", "Тушка индюшки"]
},
    "яйца": {
        "куриные": ["Яйца куриные Совхозные", "Яйца куриные Куриные Колхозные", "Яйца куриные Городские"],
        "гусиные": ["Яйца гусиные Совхозные", "Яйца гусиные Колхозные", "Яйца гусиные Городские"],
        "перепелиные": ["Яйца перепелиные Совхозные", "Яйца перепелиные Колхозные", "Яйца перепелиные Городские"]
    },
    "рыба": {
        "горбуша": ["Горбуша Совхозная", "Горбуша Колхозная", "Горбуша Городская"],
        "окунь": ["Окунь Совхозный", "Окунь Колхозный", "Окунь Городскый"],
        "треска": ["Треска Совхозная", "Треска Колхозная", "Треска Городская"]
    },
    "фрукты": {
        "груши": ["Груши Совхозные", "Груши Колхозные", "Груши Городские"],
        "дыни": ["Дыни Совхозные", "Дыни Колхозные", "Дыни Городские"],
        "яблоки": ["Яблоки Совхозные", "Яблоки Колхозные", "Яблоки Городские"]
    },
    "мёд": {
        "гречишный": ["Мёд гречишный Совхозный", "Мёд гречишный Колхозный", "Мёд гречишный Городскый"],
        "липовый": ["Мёд липовый Совхозный", "Мёд липовый Колхозный", "Мёд липовый Городскый"],
        "кленовый": ["Мёд кленовый Совхозный", "Мёд кленовый Колхозный", "Мёд кленовый Городскый"],
    },
    "мясо": {
        "говядина": ["Говядина Совхозная", "Говядина Колхозная", "Говядина Городская"],
        "свинина": ["Свинина Совхозная", "Свинина Колхозная", "Свинина Городская"],
        "баранина": ["Баранина Совхозная", "Баранина Колхозная", "Баранина Городская"],
    },
    "молочные продукты": {
        "молоко": ["Молоко Совхозное", "Молоко Колхозное", "Молоко Городское"],
        "сыр": ["Сыр Совхозный", "Сыр Колхозный", "Сыр Городской"],
        "творог": ["Творог Совхозный", "Творог Колхозный", "Творог Городской"]
    },
    "овощи": {
        "картофель": ["Картофель Совхозный", "Картофель Колхозный", "Картофель Городской"],
        "морковь": ["Морковь Совхозная", "Морковь Колхозная", "Морковь Городская"],
        "капуста": ["Капуста Совхозная", "Капуста Колхозная", "Капуста Городская"],
    }
}

for cat, subcats in product_names.items():
    for subcat_name, products in subcats.items():
        for product_name in products:
            category = Category.query.filter_by(name=subcat_name).first()
            producer_id = choice(producer_ids)
            producer = Producer.query.filter_by(id=producer_id).first()
            product = Product(choice(prices), product_name, choice(quantity), producer_id, category.id,
                              choice(measurement_units), choice(weights), choice(product_descriptions))
            db.session.add(product)
            producer.categories.append(category)
            parent_category = Category.query.filter_by(id=category.parent_id).first()
            producer.categories.append(parent_category)

for i in range(200):
    db.session.add(Product(100, f'Product{i}', 5, 1, 2, 'кг', 12, 'whaaaat'))

for i, cat in enumerate(Category.query.all()):
    cat.name = cat.name.title()

marketplace_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
for i in range(1, 10):
    try:
        os.mkdir(os.path.join(marketplace_dir, f'static/img/user_images/{i}/'))
    except FileExistsError:
        pass

comments = ['GOOOOOOD', 'GREAAAT', 'Maaaah nigga, its fucking aaawesome', 'I want more', "Where do they do that at?"]

for i, comment in enumerate(comments):
    new_comment = Comment(1, i + 10, comment, 3, consumer_name='Покупатель')
    db.session.add(new_comment)

for _ in range(100):
    db.session.add(Order(500, {'1': 5}, 'Самовывоз', 'Baker Street', '911585456', '10mail.ru',
                         11, 5, status='Не обработан', first_name=':jgf', last_name='Li'))

db.session.commit()
