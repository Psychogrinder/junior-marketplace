from path_file import *

from testMethods import getCookie, getUserIdAndEntity, getResponseCode, parseApiRoutes, \
    replaceUserId, replaceProductId, getResponseCode

import requests
import unittest
from mock import Mock



class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None
    def setUp(self):

        self.user = Mock()
        self.producer = Mock()

        #login data
        self.user.email = 'berenice.cavalcanti@example.com'
        self.producer.email = 'annabelle.denys@example.com'
        self.pw = '123123'

        self.product_id = 3

        #edit profile
        self.user.first_name = 'Abra'
        self.user.last_name = 'Cadabra'
        self.user.patronymic = 'Redisovic'
        self.user.phone_number = '81212121'

        self.base_url = 'http://127.0.0.1:8000'
        self.login_url = self.base_url + '/api/v1/login'


    def testLogin(self):

        cookie, response = getCookie(self.login_url, self.user.email, self.pw)

        self.assertEqual(201, response.status_code)
        self.assertIn('remember_token', cookie)
        self.assertIn('session', cookie)

        print('Test Login is OK.\n')

    def testLogout(self):
        logout_url = self.base_url + '/api/v1/logout'
        response = requests.Session().get(logout_url)

        self.assertEqual(201, response.status_code)
        self.assertNotIn('session', response.cookies)

        print('Test Logout is OK.\n')

    def testResponseAuthPages(self):

        #(remember_token and session in cookie) and response status_code
        cookie, response = getCookie(self.login_url, self.user.email, self.pw)
        user_id, user_entity = getUserIdAndEntity(response)

        routes = parseApiRoutes()
        for route in routes['auth']:

            if user_entity == 'producer' and '<producer_id>' in route:
                test_url = replaceUserId(self.base_url + route, user_id)
                test_url = replaceProductId(test_url, self.product_id)
                req = requests.session().get(test_url, cookies=cookie)
                self.assertEqual(200, req.status_code)

            elif user_entity == 'consumer' and '<user_id>' in route:
                test_url = replaceUserId(self.base_url + route, user_id)
                req = requests.session().get(test_url, cookies=cookie)
                self.assertEqual(200, req.status_code)
        print('Test Auth user pages is OK.\n')

        """TODO: add test /email_confirm/<token>"""

    def testUserEdit(self):
        pass
        #cookie, response = get_cookie(self.login_url, self.user.email, self.pw)

        #user = json.loads(response.content)
        #user_id, user_entity = getUserIdFromCookie(user)



if __name__ == '__main__':

    unittest.main()