from path_file import *

from testMethods import getCookie, getUserIdAndEntity, getResponseCode, parseApiRoutes, \
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
    posted_user_id = None

    def setUp(self):
        self.user = Mock()
        self.producer = Mock()

        #login data
        self.user.email = 'berenice.cavalcanti@example.com'
        self.producer.email = 'annabelle.denys@example.com'
        self.pw = '123123'

        self.product_id = 3

        #edit profile
        self.user_email = 'ramadanm@ra.ru'
        self.user.first_name = 'Abra'
        self.user.last_name = 'Cadabra'
        self.user.patronymic = 'Redisovic'
        self.user.phone_number = '81212121'

        self.base_url = 'http://127.0.0.1:8000'
        self.login_url = self.base_url + '/api/v1/login'


    def test_01_Login(self):
        cookie, response = getCookie(self.login_url, self.user.email, self.pw)

        self.assertEqual(201, response.status_code)
        self.assertIn('remember_token', cookie)
        self.assertIn('session', cookie)
        #print('Test Login is OK.')

    def test_02_Logout(self):
        logout_url = self.base_url + '/api/v1/logout'
        response = requests.Session().get(logout_url)

        self.assertEqual(201, response.status_code)
        self.assertNotIn('session', response.cookies)

        #print('Test Logout is OK.')

    def test_03_ResponseAuthPages(self):
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
        #print('Test Auth user pages is OK.')

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
            print('Delete existing user')

        self.assertIn(post_consumer(args), get_all_consumers())
        print('Posted user')

    def test_05_get_user_by_email(self):
        user = get_user_by_email(self.user_email)
        self.assertEqual(user.email, self.user_email)


    def test_06_get_consumer_by_id(self):
        user = get_user_by_email(self.user_email)

        consumer = get_consumer_by_id(user.id)
        self.assertEqual(consumer.id, user.id)


    @unittest.skip
    def test_07_put_consumer(self):
        pass


    def test_08_delete_consumer_by_id(self):
        user = get_user_by_email(self.user_email)
        consumer = get_consumer_by_id(user.id)
        self.assertIn(consumer, get_all_consumers())

        delete_consumer_by_id(user.id)
        self.assertNotIn(consumer, get_all_consumers())
        print('Deleted consumer', user.id)

    @unittest.skip
    def test_07_UserEdit(self):
        user_id = 10
        consumer = get_consumer_by_id(user_id)
        print(consumer.email)

        args = {'email': 'a@ma.ru'}

        consumer = put_consumer(args, user_id)
        print(consumer.email)

        args = {'email': 'berenice.cavalcanti@example.com'}
        consumer = put_consumer(args, user_id)
        print(consumer.email)


    def test_get_all_consumers(self):
        all_users = len(User.query.all())
        producers = len(User.query.filter_by(entity='producer').all())
        consumers = len(get_all_consumers())

        self.assertEqual(all_users - producers, consumers)


if __name__ == '__main__':
    unittest.main()