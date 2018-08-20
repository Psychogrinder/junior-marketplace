#import sys
#sys.path.insert(0, '/home/elama/dev-tools/Projects/junior-marketplace/marketplace.app/marketplace')

import unittest
from urllib.request import Request, urlopen
from selenium import webdriver

#browser = webdriver.Firefox()
#browser.get('http://127.0.0.1:5000')

#подменяет '<name_category>' на имя существующей категории для домтупа по ссылке
def addCategoryLinks(link, category):
    return link.replace('<name_category>', category)

def addIdLinks(link, id):
    return link.replace('<id>', str(id))


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
        #for k, v in self.links.items():
        #    testUrl = self.url + v
            #print(testUrl)
        link = addCategoryLinks('/category/<name_category>', 'bird')
        link = self.url + link

        self.assertEqual(200, (urlopen(link).getcode()))

    #def testPageTitle(self):
    #    self.browser.get(self.url)
    #    self.assertIn(self.title, self.browser.title)

    def testRoutes(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
