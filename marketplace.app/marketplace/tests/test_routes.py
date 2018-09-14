from path_file import *
from testing_utils import parseRoutes, get_route_by_name, getCategorySlugs,  getProductIds, getUserIds, \
    replaceCategoryName, replaceUserId, replaceProductId

import unittest
from urllib.request import urlopen
import requests
import json

class TestSmoke(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/v1'
        self.routes = parseRoutes()
        self.category_slugs = getCategorySlugs(1)
        self.user_ids = getUserIds()
        self.product_ids = getProductIds()


    def test_01_connection(self):
        self.assertEqual(200, urlopen('http://127.0.0.1:8000').getcode())
        print('Connection is OK\n')


    def test_02_login(self):
        routes = self.routes['Authorization']
        url = self.url + get_route_by_name(routes, 'login')

        login_data = {'emails': ['15mail.ru', '50mail.ru', 'melissa.clark@example.com'],
                      'password': 123123,
                      }

        for email in login_data['emails']:
            response = requests.post(url, data={'email': email, 'password': login_data['password']})
            self.assertEqual(201, response.status_code)
        print('login is OK')

    def test_03_logout(self):
        routes = self.routes['Authorization']
        url = self.url + get_route_by_name(routes, 'logout')

        response = requests.get(url)
        content = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertIn('logout', content.lower())
        print('logout is OK')


    def test_04_basic_routes(self):

        routes = self.routes
        print(routes.keys())
        url = self.url + get_route_by_name(routes, 'logout')




        # for route in self.routes:
        #     test_url = self.url + route
        #
        #
        #     if '<category_name>' in route:
        #         for category_slug in self.category_slugs:
        #             test_url = replaceCategoryName(self.url + route, category_slug)
        #
        #     elif '<producer_id>' in route:
        #         test_url = replaceUserId(test_url, self.user_ids['producer_ids'][0])
        #
        #     elif '<product_id>' in route:
        #         test_url = replaceProductId(test_url, self.product_ids[0])
        #
        #     print(test_url)
        #     self.assertEqual(200, (urlopen(test_url).getcode()))
        # print('Base routes are OK.\n')





if __name__ == '__main__':
   unittest.TestLoader.sortTestMethodsUsing = None
   suite = unittest.TestLoader().loadTestsFromTestCase(TestSmoke)
   unittest.TextTestRunner(verbosity=2).run(suite)