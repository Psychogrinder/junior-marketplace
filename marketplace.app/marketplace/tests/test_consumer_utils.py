from path_file import *

import json
from testing_utils import getResponse, getCookiesFromResponse, parseApiRoutes, replaceUserId

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
        self.consumer = Mock()
        self.producer = Mock()

        # login data
        self.consumer.email = '10mail.ru'
        self.producer.email = 'jessica.wood@example.com'
        self.pw = '123123'

        self.product_id = 3

        # edit profile
        self.user_email = 'sd@kn.ru'

        self.base_url = 'http://127.0.0.1:8000'
        self.login_url = self.base_url + '/api/v1/login'

    def test_01_login(self):

        for email in self.producer.email, self.consumer.email:
            response = getResponse(self.login_url, email, self.pw)
            cookie = getCookiesFromResponse(response)

            self.assertEqual(201, response.status_code)
            self.assertIn('remember_token', cookie)
            self.assertIn('session', cookie)


    def test_02_logout(self):
        logout_url = self.base_url + '/api/v1/logout'
        response = requests.Session().get(logout_url)

        self.assertEqual(201, response.status_code)
        self.assertNotIn('session', response.cookies)


    def test_03_response_auth_pages(self):

        login_url = 'http://127.0.0.1:8000/api/v1/login?email=10mail.ru&password=123123'
        s = requests.Session()

        data = json.loads(s.post(login_url).content)
        user_id, entity = data['id'], data['entity']

        response = getResponse(self.login_url, self.consumer.email, self.pw)
        cookie = getCookiesFromResponse(response)

        routes = parseApiRoutes()

        for route in routes['auth']:

            if 'order_registration' in route:
                continue

            if entity == 'producer' and '<producer_id>' in route:
                test_url = replaceUserId(self.base_url + route, user_id)
                test_url = replaceProductId(test_url, self.product_id)
                req = requests.session().get(test_url, cookies=cookie)
                self.assertEqual(200, req.status_code,
                                 'Page not available for auth producer: {}'.format(test_url))

            elif entity == 'consumer' and '<user_id>' in route:
                test_url = replaceUserId(self.base_url + route, user_id)
                req = requests.session().get(test_url, cookies=cookie)
                self.assertEqual(200, req.status_code,
                                 'Page not available for auth consumer: {}'.format(test_url))

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
            delete_consumer_by_id(user.id)
            print('Re-posted consumer')

        self.assertIn(post_consumer(args), get_all_consumers())


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
            'phone_number': '71111111111',
            'address': 'Мойя1 Улиця 17@1#1',
            #'email': 'asadnj@rer.ru'
        }

        response = requests.Session().put(url + str(user.id), data=load_args)
        data = json.loads(response.content)

        for i in load_args:
            print(data)
            self.assertEqual(load_args[i], data[i])


    def test_08_delete_consumer_by_id(self):
        user = get_user_by_email(self.user_email)
        consumer = get_consumer_by_id(user.id)
        self.assertIn(consumer, get_all_consumers())

        delete_consumer_by_id(user.id)
        self.assertNotIn(consumer, get_all_consumers())


    def test_09_get_all_consumers(self):

        self.assertEqual(len(User.query.filter_by(entity='consumer').all()),
                         len(get_all_consumers()))


    # test_10_upload_consumer_image
    #   pass



if __name__ == '__main__':
    unittest.main()