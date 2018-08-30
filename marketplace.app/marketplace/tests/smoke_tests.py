from path_file import *

from marketplace.models import Category, User, Product, Producer
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError

def parseApiRoutes():
    file = '../views.py'
    routes = {'auth': [],
              'not_auth': ['/category/<category_name>',
                           '/products/<product_id>',
                           '/producer/<producer_id>'
                           ]
              }

    with open(file) as f:
        for s in f:
            """ parsing classes of routes (keys) and routes:
                                seek first, last symbols in strings"""
            if '@app.route' in s:
                first_symbol, last_symblol = s.find('/'), s.rfind('\'')
                route = s[first_symbol:last_symblol]

                if route not in (routes['not_auth'] and routes['not_auth']):
                    if ('<' or '>' or 'products') not in route:
                        routes['not_auth'].append(route)
                    else:
                        routes['auth'].append(route)
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


def getResponseCode(url):
    request = Request(url=url)
    try:
        response = urlopen(request).getcode()
    except HTTPError as e:
        response = e.read()

    return response


class TestSmoke(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.routes = parseApiRoutes()
        self.category_slugs = getCategorySlugs()
        self.user_ids = getUserIds()
        self.product_ids = getProductIds()

    def testConnection(self):
        self.assertEqual(200, (urlopen(self.url).getcode()))
        print(self.url)
        print('Connection is OK\n')

    def testBaseRoutes(self):
        for route in self.routes['not_auth']:
            test_url = self.url + route

            if '<category_name>' in route:
                for category_slug in self.category_slugs:
                    test_url = replaceCategoryName(self.url + route, category_slug)

            elif '<producer_id>' in route:
                test_url = replaceUserId(test_url, self.user_ids['producer_ids'][0])

            elif '<product_id>' in route:
                test_url = replaceProductId(test_url, self.product_ids[0])

            print(test_url)
            self.assertEqual(200, (urlopen(test_url).getcode()))

        print('Base routes are OK.\n')


    def testRoutesAccessRights(self):

        """TODO: Add for all ids and Check token links"""
        for route in self.routes['auth']:

            test_url = self.url + route

            if '<producer_id>' in route:
                test_url = replaceUserId(test_url, self.user_ids['producer_ids'][0])

            elif '<user_id>' in route:
                test_url = replaceUserId(test_url, self.user_ids['user_ids'][0])

            if '<product_id>' in route:
                test_url = replaceProductId(test_url, self.product_ids[0])

            print(test_url)
            self.assertNotEqual(200, getResponseCode(test_url))

        print('Auth routes are OK.\n')

    def tearDown(self):
        pass

if __name__ == '__main__':
   unittest.TestLoader.sortTestMethodsUsing = None

   suite = unittest.TestLoader().loadTestsFromTestCase(TestSmoke)
   unittest.TextTestRunner(verbosity=2).run(suite)