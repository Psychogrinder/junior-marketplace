from path_file import *

import json
from testMethods import getResponse, getCookiesFromResponse, getUserIdAndEntity, getResponseCode, parseApiRoutes, \
    replaceUserId, replaceProductId, getResponseCode

from marketplace.api_folder.utils.user_utils import get_user_by_email

from marketplace.api_folder.utils.consumer_utils import get_consumer_by_id, get_all_consumers, \
    post_consumer, put_consumer, delete_consumer_by_id, upload_consumer_image, get_all_consumers

from marketplace.models import Consumer, User
import requests
import unittest
from mock import Mock


class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None
    
    def setUp(self):
        self.user = Mock()
        self.producer = Mock()
        self.edit = Mock()

        # login data
        self.user.email = 'berenice.cavalcanti@example.com'
        self.producer.email = 'annabelle.denys@example.com'
        self.pw = '123123'

        self.product_id = 3

        # edit profile
        self.user_email = 'sd@kn.ru'

        self.base_url = 'http://127.0.0.1:8000'
        self.login_url = self.base_url + '/api/v1/login'

    def test_01_Login(self):

        for email in self.producer.email, self.user.email:
            response = getResponse(self.login_url, email, self.pw)
            cookie = getCookiesFromResponse(response)

            self.assertEqual(201, response.status_code)
            self.assertIn('remember_token', cookie)
            self.assertIn('session', cookie)

        # print('Test Login is OK.')

    def test_02_Logout(self):
        logout_url = self.base_url + '/api/v1/logout'
        response = requests.Session().get(logout_url)

        self.assertEqual(201, response.status_code)
        self.assertNotIn('session', response.cookies)

        # print('Test Logout is OK.')

    def test_03_ResponseAuthPages(self):
        # (remember_token and session in cookie) and response status_code
        response = getResponse(self.login_url, self.user.email, self.pw)
        cookie = getCookiesFromResponse(response)

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
        # print('Test Auth user pages is OK.')

        """TODO: add test /email_confirm/<token>"""


    def test_04_post_consumer(self):
        args = {'email': self.user_email,
                'password': self.pw,
                'first_name': 'Abdullah',
                'last_name': 'Azamat',
                'phone_number': '21212121',
                'address': 'pushkin 82',
                }

        user = get_user_by_email(args['email'])
        if user:
            print('Consumer already exists')
            delete_consumer_by_id(user.id)
            print('Delete consumer')

        self.assertIn(post_consumer(args), get_all_consumers())

        print('Posted consumer')

    def test_05_get_user_by_email(self):
        user = get_user_by_email(self.user_email)
        self.assertEqual(user.email, self.user_email)

    def test_06_get_consumer_by_id(self):
        user = get_user_by_email(self.user_email)

        consumer = get_consumer_by_id(user.id)
        self.assertEqual(consumer.id, user.id)

    def test_07_put_consumer(self):
        url = 'http://127.0.0.1:8000/api/v1/consumers/'
        user = get_user_by_email(self.user_email)

        load_args = {
            'last_name': 'Bawbara',
            'first_name': 'JNf',
            'patronymic': 'Львоer',
            'phone_number': '32222222',
            'address': 'Мойя1 Улиця 17@1#1',
        }

        response = requests.Session().put(url + str(user.id), data=load_args)
        data = json.loads(response.content)

        for i in load_args:
            self.assertEqual(load_args[i], data[i])


    def test_08_delete_consumer_by_id(self):
        user = get_user_by_email(self.user_email)
        consumer = get_consumer_by_id(user.id)
        self.assertIn(consumer, get_all_consumers())

        delete_consumer_by_id(user.id)
        self.assertNotIn(consumer, get_all_consumers())

    def test_09_get_all_consumers(self):
        all_users = len(User.query.all())
        producers = len(User.query.filter_by(entity='producer').all())
        consumers = len(get_all_consumers())

        self.assertEqual(all_users - producers, consumers)

    # test_10_upload_consumer_image



if __name__ == '__main__':
    unittest.main()
