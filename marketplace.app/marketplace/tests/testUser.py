from path_file import *

import requests, json
import unittest
from mock import Mock
from smoke_tests import parseApiRoutes, replaceUserId, getResponseCode
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
        self.user.first_name = 'Abra'
        self.user.last_name = 'Cadabra'
        self.user.email = 'annabelle.denys@example.com'
        self.user.pw = '123123'
        self.user.phone_number = '81212121'

        self.base_url = 'http://127.0.0.1:8000'
        self.login_url = 'http://127.0.0.1:8000/api/v1/login'


    def testLogin(self):
        cookie, response = get_cookie(self.login_url, self.user.email, self.user.pw)

        self.assertEqual(201, response.status_code)
        self.assertIn('remember_token', cookie)


    def testLogout(self):
        logout_url = 'http://127.0.0.1:8000/api/v1/logout'
        response = requests.Session().get(logout_url)

        self.assertEqual(201, response.status_code)
        self.assertNotIn('session', response.cookies)


    def testGetAuthPages(self):
        s = requests.Session()
        cookie, response = get_cookie(self.login_url, self.user.email, self.user.pw)

        user = json.loads(response.content)
        user_id, user_entity = user['id'], user['entity']

        #r = s.post(url, cookie)
        routes = parseApiRoutes()
        for route in routes['auth']:

            if user_entity == 'producer' and '<producer_id>' in route:
                """TODO: get method with session data"""

                test_url = replaceUserId(self.base_url + route, user_id)
                print(test_url)
                #self.assertEqual(200, getResponseCode(test_url))
                print(getResponseCode(test_url))
            elif user_entity == 'consumer' and '<user_id>' in route:
                pass


if __name__ == '__main__':
    unittest.main()