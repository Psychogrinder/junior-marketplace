import os
import sys
import urllib.request
import json
from random import choice

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(os.path.realpath(dir_path))
sys.path.insert(0, dir_path)
from models import *

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

with urllib.request.urlopen("https://randomuser.me/api/?results=100") as response:
    data = response.read()
    data = json.loads(data)
    for company in data["results"]:
        consumer = Consumer(company['email'], company['login']['password'], company['name']['first'],
                            company['name']['last'], company['phone'], company['location']['street'])
        db.session.add(consumer)

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
    cat.id = i+1

prices = range(50, 1000)
quantity = range(100, 500)
producer_ids = range(1, len(producer_names)+1)
measurement_units = ['кг', 'литры', 'штуки']
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
        "яблоки": ["Дыни Совхозные", "Дыни Колхозные", "Дыни Городские"]
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
            category_id = Category.query.filter_by(name=subcat_name).first().id
            product = Product(choice(prices), product_name, choice(quantity), choice(producer_ids), category_id, choice(measurement_units), choice(weights), choice(product_descriptions))
            db.session.add(product)

db.session.commit()
