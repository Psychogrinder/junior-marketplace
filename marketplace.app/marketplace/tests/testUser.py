from path_file import *

from marketplace.api_folder.login_api import Login

from marketplace.api_folder.api_utils import login
import flask_login
import requests, json
import unittest

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

        self.first_name = 'Abra'
        self.last_name = 'Cadabra'
        self.base_route = 'http://127.0.0.1:8000/api/v1'
        self.login_url = 'http://127.0.0.1:8000/api/v1/login'
        self.email = 'annabelle.denys@example.com'
        self.pw = '123123'
        self.entity = 'consumer'
        self.phone_number = '81212121'



    def testLogin(self):
        cookie, response = get_cookie(self.login_url, self.email, self.pw)

        self.assertEqual(201, response.status_code)
        self.assertIn('remember_token', cookie)


    def testLogout(self):
        logout_url = 'http://127.0.0.1:8000/api/v1/logout'
        response = requests.Session().get(logout_url)

        self.assertEqual(201, response.status_code)
        self.assertNotIn('session', response.cookies)


    def testAuthPages(self):

        cookie, response = get_cookie(self.login_url, self.email, self.pw)
        r = requests.post(url, cookie)

if __name__ == '__main__':
    unittest.main()