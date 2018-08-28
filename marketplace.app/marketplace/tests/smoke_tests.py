from path_file import *

from marketplace.models import Category, User, Product
import unittest
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def parseApiRoutes():
    file = '../views.py'
    routes = []
    with open(file) as f:
        for s in f:
            """ parsing classes of routes (keys) and routes:
                                seek first, last symbols in strings"""
            if '@app.route' in s:
                first_symbol, last_symblol = s.find('/'), s.rfind('\'')
                route = s[first_symbol: last_symblol]
                routes.append(route)
    return routes

def getCategorySlugs():
    category_slugs = []

    for category in Category.query.all():
        category_slugs.append(category.slug)

    return category_slugs

def replaceCategoryName(url, category_slug):
    if '<category_name>' in url:
        return url.replace('<category_name>', category_slug)

def getUserIds():
    user_ids = {'producer_ids': [], 'user_ids': [], 'count': 0}

    for user in User.query.all():
        if user.entity == 'producer':
            user_ids['producer_ids'].append(user.id)
        else:
            user_ids['user_ids'].append(user.id)
        user_ids['count'] += 1

    return user_ids #return dict with user ids

def replaceUserId(url, user_id):
    if '<producer_id>' in url:
        return url.replace('<producer_id>', str(user_id))
    elif '<user_id>' in url:
        return url.replace('<user_id>', str(user_id))

def getProductIds():
    product_ids = []

    for product_id in Product.query.all():
        product_ids.append(product_id.id)

    return product_ids

def replaceProductId(url, product_id):
    if '<product_id>' in url:
        return url.replace('<product_id>', str(product_id))

class TestSmoke(unittest.TestCase):

    def setUp(self):

        self.url = 'http://127.0.0.1:8000'
        self.routes = parseApiRoutes()
        self.category_slugs = getCategorySlugs()

    def testConnection(self):
        self.assertEqual(200, (urlopen(self.url).getcode()))

    def testBaseRoutes(self):
        for route in self.routes:
            test_url = self.url + route
            if '<' not in test_url:
                self.assertEqual(200, (urlopen(test_url).getcode()))


    def testCategoryRoutes(self):
        matching = [route for route in self.routes if '<category_name>' in route]

        for category_slug in self.category_slugs:
            test_url = replaceCategoryName(self.url + matching[0], category_slug)
            self.assertEqual(200, (urlopen(test_url).getcode()))

    def testUserRoutes(self):
        user_ids = getUserIds()
        product_ids = getProductIds()

        """TODO: Add for all ids"""
        for route in self.routes:
            test_url = self.url + route

            if '<producer_id>' in route:
                test_url = replaceUserId(test_url, user_ids['producer_ids'][0])
                if '<product_id>' not in route:
                    print(test_url)

            elif '<user_id>' in route:
                test_url = replaceUserId(test_url, user_ids['user_ids'][0])
                print(test_url)

            if '<product_id>' in route:
                test_url = replaceProductId(test_url, product_ids[0])
                print(test_url)

    def testToken(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
   unittest.main()