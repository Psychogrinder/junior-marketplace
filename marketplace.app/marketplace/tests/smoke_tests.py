#import sys
#sys.path.insert(0, '/home/elama/dev-tools/Projects/junior-marketplace/marketplace.app/marketplace')

import unittest
from urllib.request import Request, urlopen
from selenium import webdriver


#подменяет '<name_category>' на имя существующей категории для домтупа по ссылке
def addCategoryLinks(link, category):
    return link.replace('<name_category>', category)

# --/-- <id> с базы данных
def addIdLinks(link, id):
    return link.replace('<id>', str(id))


class TestSmoke(unittest.TestCase):

    def setUp(self):
        #self.browser = webdriver.Firefox()
        #self.addCleanup(self.browser.quit)

        self.url = 'http://127.0.0.1:5000'
        self.title = 'Маркетплейс'
        self.categories = [#'poultry',
                           'eggs', 'fish', 'fruits',
                           'honey', 'meat', 'milk', 'vegetables'
                           ]
        self.links = {'my_orders': '/order_history/<id>', # consumer orders
                      'orders': '/producer/<id>/orders', # producer orders
                      'products': '/producer/<id>/products',
                      'category': '/category/<name_category>',
                      'add_product': '/producer/<id>/create_product',
                      'product': '/category/<name_category>/<id>',
                      'profile': '/user/<id>',
                      'confirm_order': '/cart/<id>/order_registration/'
                      }
        self.id_user = 17


    def testConnection(self):
        self.assertEqual(200, (urlopen(self.url).getcode()))


        #проверяет корректность категорий по ссылке
        for category in range(len(self.categories)):
            for key, value in self.links.items():

                link = addCategoryLinks(value, self.categories[category])
                link = addIdLinks(link, self.id_user)
                test_url = self.url + link
                print(test_url)

                self.assertEqual(200, (urlopen(test_url).getcode()))

    #def testPageTitle(self):
    #    self.browser.get(self.url)
    #    self.assertIn(self.title, self.browser.title)

    def tearDown(self):
        pass

if __name__ == '__main__':
   unittest.main()