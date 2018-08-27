from path_file import *

#from marketplace import db
from marketplace.models import Category
import unittest
from urllib.request import Request, urlopen
from selenium import webdriver

def parseApiRoutes():
    file = '../views.py'
    with open(file) as f:
        routes = []
        for s in f:
            if '@app.route' in s:

                """ parsing classes of routes (keys) and routes:
                seek first, last symbols in strings"""
                first_symbol, last_symblol = s.find('/'), s.rfind('\'')
                route = s[first_symbol: last_symblol]
                routes.append(route)

    #routes = {k: str(v[0]) for k, v in routes.items()} #list to string
    return routes

def getCategoryIds():
    categories_id = []
    for category in Category.query.all():
        categories_id.append(category.id)

    return categories_id

def addIdLinks(link, category):
    """преобразование <int:____id> на существующие id"""
    return link.replace('<id>', str(id))

class TestSmoke(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.routes = parseApiRoutes()
        self.id_user = 5
        self.category_ids = getCategoryIds()

    def testConnection(self):
        self.assertEqual(200, (urlopen(self.url).getcode()))

    def testRoutes(self):
        for route in self.routes:
            #link = addIdLinks(route, self.id_user)
            test_url = self.url + route

            """преобразованные ссылки"""
            if '<' not in test_url:
                print(test_url)
                self.assertEqual(200, (urlopen(test_url).getcode()))

    def tearDown(self):
        pass

if __name__ == '__main__':
   unittest.main()