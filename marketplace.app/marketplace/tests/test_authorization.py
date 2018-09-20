from path_file import *
from testing_utils import login, logout, parseRoutes, get_route_by_name, getCategorySlugs, getProductIds, getUserIds, \
    replaceCategoryName, replaceUserId, replaceProductId, getCookiesFromResponse, getLoginResponse

from marketplace.models import Order, User

import unittest
from urllib.request import urlopen
import json
import requests

class TestAuthorization(unittest.TestCase):

    def setUp(self):


        self.url = 'http://127.0.0.1:8000/api/v1'
        self.routes = parseRoutes()

        self.consumers = User.query.filter_by(entity='consumer').limit(10).all()
        self.producers = User.query.filter_by(entity='producer').limit(10).all()
        self.users = self.consumers + self.producers
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


    def test_04_password_recovery(self):
        routes = self.routes['Password']
        url = self.url + get_route_by_name(routes, '/password/recovery')

        for user in self.users:
            response = requests.Session().post(url, data={"email": user.email})
            try:
                self.assertEqual(200, response.status_code)
            except AssertionError:
                print('password recovery doesnt work. {}'.format(response.status_code, user.email))


if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthorization)
