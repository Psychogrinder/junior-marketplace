from path_file import *
from testMethods import parseApiRoutes, getCategorySlugs,  getProductIds,  getResponseCode, getUserIds, \
    replaceCategoryName, replaceUserId, replaceProductId
import unittest
from urllib.request import urlopen


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