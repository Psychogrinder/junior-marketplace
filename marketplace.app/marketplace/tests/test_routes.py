from path_file import *
from testing_utils import login, logout, parseRoutes, get_route_by_name, getCategorySlugs,  getProductIds, getUserIds, \
    replaceCategoryName, replaceUserId, replaceProductId, getCookiesFromResponse, getLoginResponse

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

        #login data
        self.admin = {'email': 'ad@min.ru',
                      'password': '123123',
                      }
        self.producer = {'email': 'melissa.clark@example.com',
                         'password': '123123',
                         }
        self.consumer = {'email': '5mail.ru',
                         'password': '123123',
                         }

    def test_01_connection(self):
        self.assertEqual(200, urlopen('http://127.0.0.1:8000').getcode(), 'Website doesn\'t response')


    def test_02_login(self):
        routes = self.routes['Authorization']
        url = self.url + get_route_by_name(routes, 'login')

        login_data = {'emails': ['15mail.ru', '50mail.ru', 'melissa.clark@example.com'],
                      'password': 123123,
                      }

        for email in login_data['emails']:
            response = requests.post(url, data={'email': email, 'password': login_data['password']})
            self.assertEqual(201, response.status_code)


    def test_03_logout(self):
        routes = self.routes['Authorization']
        url = self.url + get_route_by_name(routes, 'logout')

        response = requests.get(url)
        content = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertIn('logout', content.lower())


    def test_04_global_orders(self):
        """only admin has permission to get global orders"""
        routes = self.routes['Orders']
        url = self.url + get_route_by_name(routes, '/orders')

        users = [self.admin, self.consumer, self.producer]
        for user in users:
            response_login = login(email=user['email'], password=user['password'])
            cookie = getCookiesFromResponse(response_login)
            content = json.loads(response_login.text)

            response = requests.session().get(url, cookies=cookie)
            if content['entity'] == 'admin':
                self.assertNotIn('reject access', response.text.lower())
            else:
                self.assertIn('reject access', response.text.lower())

        logout()
        response = requests.get(url)
        self.assertNotEqual(200, response.status_code)
        self.assertIn('reject access', response.text.lower())


        """POST order"""
        args = {'total_cost': '1 730.00 ₽',
                'order_items_json': {'58': 10},
                'delivery_method': 'Самовывоз',
                'delivery_address': 'политехническая',
                'consumer_phone': '72231224242',
                'consumer_email': '15mail.ru',
                'consumer_id': 24,
                'producer_id': 2,
        }

        login('15mail.ru', '123123')
        response = requests.post(url, data=args)



    def test_05_orders(self):
        routes = self.routes['Orders']
        url = self.url + get_route_by_name(routes, '/orders/<int:order_id>')


        #     if '<category_name>' in route:
        #         for category_slug in self.category_slugs:
        #             test_url = replaceCategoryName(self.url + route, category_slug)



if __name__ == '__main__':
   unittest.TestLoader.sortTestMethodsUsing = None
   suite = unittest.TestLoader().loadTestsFromTestCase(TestSmoke)
   unittest.TextTestRunner(verbosity=2).run(suite)