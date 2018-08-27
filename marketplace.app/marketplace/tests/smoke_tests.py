from path_file import *

#from marketplace import db
from marketplace.models import Category
import unittest
from urllib.request import Request, urlopen
from selenium import webdriver

def parseApiRoutesFromFile():
    file = '../api_routes.py'
    with open(file) as f:
        routes = {}
        for s in f:
            if 'api.add_resource' in s:

                """ parsing classes of routes (keys) and routes:
                seek first, last symbols in strings"""
                key_f, key_l, route_f, route_l = s.find('('), s.rfind(','), s.find('/'), s.rfind('\'')
                key, route = s[key_f+1 : key_l], s[route_f : route_l]
                routes[key] = [route]

    routes = {k: str(v[0]) for k, v in routes.items()} #list to string
    return routes

def getAllCategoryIdFromDB():
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
        self.routes = parseApiRoutesFromFile()
        self.id_user = 5
        self.category_ids = getAllCategoryIdFromDB()

    def testConnection(self):
        self.assertEqual(200, (urlopen(self.url).getcode()))

    def testRoutes(self):
        for key, route in self.routes.items():

            #link = addIdLinks(route, self.id_user)
            test_url = self.url + route

            """преобразованные ссылки"""
            if '<' not in test_url:
                print(test_url)

                self.assertEqual(200, (urlopen(test_url).getcode()))

        print(self.category_ids)

    def tearDown(self):
        pass

if __name__ == '__main__':
   unittest.main()