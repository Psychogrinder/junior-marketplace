#from path_for_smoke_tests import *
#import db
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
                seek first, last symbols in strings
                Example: Class, /example/route/<id> """
                key_f, key_l, route_f, route_l = s.find('('), s.rfind(','), s.find('/'), s.rfind('\'')
                key, route = s[key_f+1 : key_l], s[route_f : route_l]
                routes[key] = [route]

    routes = {k: str(v[0]) for k, v in routes.items()} #list to string
    return routes

print(parseApiRoutesFromFile())

def addIdLinks(link, category):
    """преобразование <int:____id> на существующие id"""
    return link.replace('<id>', str(id))

class TestSmoke(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.routes = parseApiRoutesFromFile()
        self.id_user = 5

    def testConnection(self):
        self.assertEqual(200, (urlopen(self.url).getcode()))

    def testRoutes(self):
        for key, value in self.routes.items():

            link = addIdLinks(value, self.id_user)
            test_url = self.url + link
            print(test_url)

            #self.assertEqual(200, (urlopen(test_url).getcode()))

    def tearDown(self):
        pass

if __name__ == '__main__':
   unittest.main()