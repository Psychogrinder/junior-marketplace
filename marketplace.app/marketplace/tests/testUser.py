from path_file import *

import requests, json
import unittest
from mock import Mock
from smoke_tests import parseApiRoutes, replaceUserId, replaceProductId, getResponseCode
from urllib.request import Request, urlopen

def get_cookie(login_url, email, password):
    payload = {
        'email': email,
        'password': password
    }
    s = requests.Session()
    response = s.post(login_url, data=payload, allow_redirects=False)

    return response.cookies.get_dict(), response


class TestCase(unittest.TestCase):

    def setUp(self):

        self.user = Mock()
        self.producer = Mock()

        #logging data
        self.user.email = 'berenice.cavalcanti@example.com'
        self.producer.email = 'annabelle.denys@example.com'
        self.pw = '123123'

        self.product_id = 3

        #data for edit profile
        self.user.first_name = 'Abra'
        self.user.last_name = 'Cadabra'
        self.user.phone_number = '81212121'

        self.base_url = 'http://127.0.0.1:8000'
        self.login_url = self.base_url + '/api/v1/login'


    def testLogin(self):

        cookie, response = get_cookie(self.login_url, self.user.email, self.pw)

        self.assertEqual(201, response.status_code)
        self.assertIn('remember_token', cookie)
        self.assertIn('session', cookie)


    def testLogout(self):
        logout_url = self.base_url + '/api/v1/logout'
        response = requests.Session().get(logout_url)

        self.assertEqual(201, response.status_code)
        self.assertNotIn('session', response.cookies)


    def testGetAuthPages(self):

        #(remember_token and session in cookie) and response status_code
        cookie, response = get_cookie(self.login_url, self.user.email, self.pw)

        user = json.loads(response.content)
        user_id, user_entity = user['id'], user['entity']

        routes = parseApiRoutes()
        for route in routes['auth']:

            test_url = self.base_url + route

            if user_entity == 'producer' and '<producer_id>' in route:
                test_url = replaceUserId(test_url, user_id)
                test_url = replaceProductId(test_url, self.product_id)
                req = requests.session().get(test_url, cookies=cookie)
                self.assertEqual(200, req.status_code)

            elif user_entity == 'consumer' and '<user_id>' in route:
                test_url = replaceUserId(self.base_url + route, user_id)
                req = requests.session().get(test_url, cookies=cookie)
                self.assertEqual(200, req.status_code)

            """TODO: add test /email_confirm/<token>"""


if __name__ == '__main__':
    unittest.main()