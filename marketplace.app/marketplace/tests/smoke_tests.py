#from ..api_folder import category_api

import unittest
from urllib.request import Request, urlopen
from selenium import webdriver


def addCategoryLinks(link, category):
    """заменяет '<name_category>' на имя корректное категории
    для проверки респонса"""
    return link.replace('<name_category>', category)

def addIdLinks(link, id):
    """ --/-- <id>"""
    return link.replace('<id>', str(id))

class TestSmoke(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.title = 'Маркетплейс'
        self.categories = ['poultry',
                           'eggs', 'fish', 'fruits',
                           'honey', 'meat', 'milk', 'vegetables'
                           ]
        self.links = {'my_orders': '/order_history/<id>', # consumer orders
                      'orders': '/producer/<id>/orders', # producer orders
                      'products': '/producer/<id>/products',
                      'category': '/category/<name_category>',
                      #'add_product': '/producer/<id>/create_product',
                      'product': '/category/<name_category>',
                      'profile': '/user/<id>',
                      'confirm_order': '/cart/<id>/order_registration/'
                      }
        self.id_user = 5

    def testConnection(self):
        """проверка подключения"""
        self.assertEqual(200, (urlopen(self.url).getcode()))

    def testRoutes(self):
        """проверка роутов"""
        for category in range(len(self.categories)):
            for key, value in self.links.items():
                link = addCategoryLinks(value, self.categories[category])
                link = addIdLinks(link, self.id_user)
                test_url = self.url + link
                print(test_url)
                self.assertEqual(200, (urlopen(test_url).getcode()))

    def tearDown(self):
        pass

if __name__ == '__main__':
   unittest.main()