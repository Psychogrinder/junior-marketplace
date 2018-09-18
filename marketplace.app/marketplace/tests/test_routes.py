
from path_file import *
from testing_utils import login, logout, parseRoutes, get_route_by_name, getCategorySlugs,  getProductIds, getUserIds, \
    replaceCategoryName, replaceUserId, replaceProductId, getCookiesFromResponse, getLoginResponse

from marketplace.models import Order, User

import unittest
from urllib.request import urlopen
import requests
import json

class TestSmoke(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/v1'
        self.routes = parseRoutes()

        self.consumers = User.query.filter_by(entity='consumer').limit(5).all()
        self.producers = User.query.filter_by(entity='producer').limit(5).all()
        self.admin = User.query.filter_by(entity='admin').limit(1).all()
        self.users = self.consumers + self.producers + self.admin

        self.password = '123123'

    def test_01_connection(self):
        self.assertEqual(200, urlopen('http://127.0.0.1:8000').getcode(),
                         'Website does not response')


    def test_02_login(self):
        for user in self.users:
            response = login(user.email, self.password)
            self.assertEqual(201, response.status_code,
                             'unexpected status code after login')


    def test_03_logout(self):
        response = logout()
        content = json.loads(response.content)
        self.assertEqual(201, response.status_code,
                         'unexpected status code after logout')
        self.assertIn('logout', content.lower())


    def test_04_get_global_orders(self):
        """only admin has permission to get global orders"""
        routes = self.routes['Orders']
        url = self.url + get_route_by_name(routes, '/orders')

        for user in self.users:
            response_login = login(email=user.email, password=self.password)
            cookie = getCookiesFromResponse(response_login)
            content = json.loads(response_login.text)

            response = requests.session().get(url, cookies=cookie)

            if content['entity'] == 'admin':
                self.assertNotIn('reject access', response.text.lower(),
                                 '{} can not GET global order'.format(content['entity']))
            else:
                self.assertIn('reject access', response.text.lower(),
                              '{} can GET global order'.format(content['entity']))
        logout()
        response = requests.get(url)
        self.assertNotEqual(200, response.status_code)
        self.assertIn('reject access', response.text.lower(),
                      'unauthorized user can GET global order')

    
    def test_05_post_global_orders(self):
        routes = self.routes['Orders']
        url = self.url + get_route_by_name(routes, '/orders')

        post_args = {'orders': '[{"producer_id": "21", "delivery_method": "Самовывоз"}]',
                     'delivery_address': 'new address',
                     'phone': '+7(123)123-23-21',
                     'email': None,
                     'consumer_id': None,
                     'status': None,
                     'total_cost': '9 999.00 ₽',
                     'first_name': 'sasas',
                     'last_name': 'smara'}

        for user in self.users:
            response_login = login(email=user.email, password=self.password)
            cookie = getCookiesFromResponse(response_login)
            content = json.loads(response_login.text)

            post_args['email'] = user.email
            post_args['consumer_id'] = content['id']

            response_post = requests.Session().post(url, data=post_args, cookies=cookie)
            if content['entity'] == 'consumer':
                self.assertEqual(201, response_post.status_code,
                                 '{} should POST to global order'.format(content['entity']))
            else:
                self.assertEqual(404, response_post.status_code,
                                 '{} should not POST to global order'.format(content['entity']))
        logout()
        response_logout = requests.post(url, data=post_args)
        self.assertNotEqual(201, response_logout.status_code,
                            'unauthorized user can POST to global order')


    def test_06_get_orders(self):
        routes = self.routes['Orders']
        url_route = self.url + get_route_by_name(routes, '/orders/<int:order_id>')

        orders = Order.query.limit(5).all()
        for order in orders:
            url = url_route.replace('<int:order_id>', str(order.id))

            for user in self.users:
                response_login = login(email=user.email, password=self.password)
                cookie = getCookiesFromResponse(response_login)
                content = json.loads(response_login.text)

                response_get = requests.Session().get(url, cookies=cookie)
                if user.id == order.consumer_id:
                    self.assertEqual(user.email, order.consumer_email,
                                    'order №{} (consumer_id: {}) should see consumer with id {}'
                                     .format(order.id, order.consumer_id, user.id))
                    self.assertEqual(content['id'], order.consumer_id)
                else:
                    self.assertIn('reject access', response_get.text.lower(),
                                  'order №{} with consumer_id: {} should not see consumer with id {}'
                                  .format(order.id, order.consumer_id, content['id']))
                    self.assertNotEqual(user.email, order.consumer_email)
                    self.assertNotEqual(content['id'], order.consumer_id)

            logout()
            response = requests.get(url)
            self.assertIn('reject access', response.text.lower(),
                          'unauthorized user should not see order №{}'.format(order.id))


if __name__ == '__main__':
   unittest.TestLoader.sortTestMethodsUsing = None
   suite = unittest.TestLoader().loadTestsFromTestCase(TestSmoke)
   unittest.TextTestRunner(verbosity=2).run(suite)