from testing_utils import login, logout, parseRoutes, get_route_by_name, getCategorySlugs, getProductIds, getUserIds, \
    replaceCategoryName, replaceUserId, replaceProductId, getCookiesFromResponse, getLoginResponse

from marketplace.models import Order, User

import unittest
from urllib.request import urlopen
import json


class TestAuthorization(unittest.TestCase):

    def setUp(self):

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


if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthorization)
