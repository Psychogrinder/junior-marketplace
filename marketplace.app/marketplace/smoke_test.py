#import sys
#sys.path.insert(0, '/home/elama/dev-tools/Projects/junior-marketplace/marketplace.app/marketplace')

import unittest
from urllib.request import Request, urlopen
from selenium import webdriver

#browser = webdriver.Firefox()
#browser.get('http://127.0.0.1:5000')

def rightLinks(link, category, id):
    pass

class TestSmoke(unittest.TestCase):

    def setUp(self):
        #self.browser = webdriver.Firefox()
        #self.addCleanup(self.browser.quit)
        self.url = 'http://127.0.0.1:5000'
        self.title = 'Маркетплейс'
        self.categories = ['bird', 'eggs', 'fish', 'fruits',
                           'honey', 'meat', 'milk', 'vegetables'
                           ]
        self.links = {'orders': '/producer/<id>/orders/', # producer orders
                      'products': '/producer/<id>/products/',
                      'category': '/category/<name_category>',
                      'profile': '/user/<id>',
                      'cart': '/cart/<id>/',
                      'my_orders': '/order_history/<id>' # consumer orders
                      }

    def testConnection(self):
        self.assertEqual(200, (urlopen(self.url).getcode()))
        for k, v in self.links.items():
            testUrl = self.url + v

            print(testUrl)
            self.assertEqual(200, (urlopen(testUrl).getcode()))

    #def testPageTitle(self):
    #    self.browser.get(self.url)
    #    self.assertIn(self.title, self.browser.title)

    def testRoutes(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
