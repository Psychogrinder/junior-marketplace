from path_file import *

#from marketplace import db
from marketplace.models import Category
import unittest
from urllib.request import Request, urlopen
from selenium import webdriver

def parseApiRoutes():
    file = '../views.py'
    routes = []
    with open(file) as f:
        for s in f:
            if '@app.route' in s:

                """ parsing classes of routes (keys) and routes:
                seek first, last symbols in strings"""
                first_symbol, last_symblol = s.find('/'), s.rfind('\'')
                route = s[first_symbol: last_symblol]
                routes.append(route)
    return routes

def getCategorySlug():
    category_slugs = []
    for category in Category.query.all():
        category_slugs.append(category.slug)

    return category_slugs

def replaceCategoryName(url, category_slug):
    if '<category_name>' in url:
        return url.replace('<category_name>', category_slug)

class TestSmoke(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.routes = parseApiRoutes()
        self.id_user = 5
        self.category_slugs = getCategorySlug()

    def testConnection(self):
        self.assertEqual(200, (urlopen(self.url).getcode()))

    def testBaseRoutes(self):
        for route in self.routes:
            test_url = self.url + route
            if '<' not in test_url:
                self.assertEqual(200, (urlopen(test_url).getcode()))
            else:
                print(test_url)

    def testCategoryRoutes(self):
        matching = [route for route in self.routes if '<category_name>' in route]

        for category_slug in self.category_slugs:
            test_url = replaceCategoryName(self.url + matching[0], category_slug)
            self.assertEqual(200, (urlopen(test_url).getcode()))

    def tearDown(self):
        pass

if __name__ == '__main__':
   unittest.main()